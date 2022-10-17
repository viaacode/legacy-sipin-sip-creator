#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import functools
import re
import threading

import pika.exceptions
from cloudevents.events import (
    Event,
    EventOutcome,
    EventAttributes,
)
from requests.exceptions import ConnectionError, RetryError
from urllib3.exceptions import MaxRetryError
from viaa.configuration import ConfigParser
from viaa.observability import logging

from app.services.org_api import OrgApiClient
from app.services.pulsar import PulsarClient, PRODUCER_TOPIC
from app.services import rabbit
from app.helpers.bag import Bag
from app.helpers.sidecar import InvalidSidecarException, Sidecar
from app.helpers.events import WatchfolderMessage, InvalidMessageException

APP_NAME = "sipin-sip-creator"


class EventListener:
    def __init__(self):
        configParser = ConfigParser()
        self.log = logging.get_logger(__name__, config=configParser)
        self.config = configParser.app_cfg
        self.threads = []
        # Init RabbitMQ client
        try:
            self.rabbit_client = rabbit.RabbitClient()
        except pika.exceptions.AMQPConnectionError as error:
            self.log.error("Connection to RabbitMQ failed.")
            raise error
        # Init Pusar client
        self.pulsar_client = PulsarClient()
        # Init org API client
        self.org_api_client = OrgApiClient()

    def ack_message(self, channel, delivery_tag):
        if channel.is_open:
            channel.basic_ack(delivery_tag)
        else:
            # Channel is already closed, so we can't ACK this message
            # TODO: handle properly
            pass

    def send_ack_message(self, channel, delivery_tag):
        cb_ack = functools.partial(self.ack_message, channel, delivery_tag)
        self.rabbit_client.connection.add_callback_threadsafe(cb_ack)

    def nack_message(self, channel, delivery_tag, requeue=False):
        if channel.is_open:
            channel.basic_nack(delivery_tag, requeue=requeue)
        else:
            # Channel is already closed, so we can't NACK this message
            # TODO: handle properly
            pass

    def send_nack_message(self, channel, delivery_tag, requeue=False):
        cb_nack = functools.partial(
            self.nack_message, channel, delivery_tag, requeue=requeue
        )
        self.rabbit_client.connection.add_callback_threadsafe(cb_nack)

    def send_pulsar_message(self, attributes: dict, data: dict) -> Event:
        outgoing_event = Event(attributes, data)
        self.pulsar_client.produce_event(outgoing_event)
        return outgoing_event

    def send_failed_pulsar_message(
        self, attributes: dict, data: dict, message: str
    ) -> Event:
        data["outcome"] = EventOutcome.FAIL.to_str()
        data["message"] = message
        outgoing_event = self.send_pulsar_message(attributes, data)
        self.log.info("SIP-creation failed event sent.")
        return outgoing_event

    def do_work(self, channel, delivery_tag, properties, body):
        """Worker method:

        - Parse the message.
        - Create the SIP.
        - Make a bag of the SIP.
        - Send a cloudevent to a Pulsar topic.
        """
        try:
            # Parse watchfolder
            message = WatchfolderMessage(body)
        except InvalidMessageException as e:
            self.log.error(e)
            self.send_nack_message(channel, delivery_tag)
            return

        essence_path = message.get_essence_path()
        xml_path = message.get_xml_path()

        # Check if essence and XML file exist
        if not essence_path.exists() or not xml_path.exists():
            self.log.error(
                f"Essence ({essence_path}) and/or sidecar ({xml_path}) not found."
            )
            self.send_nack_message(channel, delivery_tag)
            return

        # filesize of essence. Essence is moved when creating the bag.
        essence_filesize = essence_path.stat().st_size

        # Build Pulsar attributes/data
        attributes = EventAttributes(
            type=PRODUCER_TOPIC,
            source=APP_NAME,
            subject=essence_path.stem,
            outcome=EventOutcome.SUCCESS,
        )

        data = {
            "host": self.config["host"],
            "essence_filename": essence_path.name,
            "cp_id": message.flow_id,
            "essence_filesize": essence_filesize,
        }

        # Parse sidecar
        try:
            sidecar = Sidecar(xml_path)
        except InvalidSidecarException as e:
            self.log.error(f"Could not create SIP because sidecar was invalid. {e}")
            # Create and send cloudevent
            self.send_failed_pulsar_message(attributes, data, f"Sidecar not valid. {e}")
            self.send_nack_message(channel, delivery_tag)
            return

        # Create bag
        try:
            bag_path, bag = Bag(message, sidecar, self.org_api_client).create_sip_bag()
        except (ConnectionError, MaxRetryError, RetryError):
            self.send_nack_message(channel, delivery_tag, requeue=True)
            return

        # Regex to match essence paths in bag to fetch md5
        regex = re.compile("data/representations/.*/data/.*")

        for filepath, fixity in bag.entries.items():
            if regex.match(filepath):
                md5_hash_essence_manifest = fixity["md5"]

        # Add sidecar info to data payload of event
        # Add batch ID if available
        if sidecar.batch_id:
            data["batch_id"] = sidecar.batch_id
        # Add local ID if available
        if sidecar.local_id:
            data["local_id"] = sidecar.local_id
        data["md5_hash_essence_sidecar"] = sidecar.md5

        # Add bag info to data payload of event
        data["path"] = str(bag_path)
        data["bag_filesize"] = bag_path.stat().st_size
        data["md5_hash_essence_manifest"] = md5_hash_essence_manifest

        # Check if calculated md5 is the same as the supplied md5
        if md5_hash_essence_manifest != sidecar.md5.lower():
            self.log.error(
                "Supplied MD5 differs from the calculated MD5.",
                sidecar_md5=sidecar.md5.lower(),
                manifest_md5=md5_hash_essence_manifest,
            )
            self.send_failed_pulsar_message(
                attributes, data, "Supplied MD5 differs from the calculated MD5."
            )
            self.send_nack_message(channel, delivery_tag)
            return

        data["outcome"] = EventOutcome.SUCCESS.to_str()
        data["message"] = f"SIP created: '{bag_path}'"

        # Create and send cloudevent
        self.send_pulsar_message(attributes, data)

        self.log.info("SIP created event sent.")

        # Send RabbitMQ ack
        self.send_ack_message(channel, delivery_tag)

    def handle_message(self, channel, method, properties, body):
        """Main method that will handle the incoming messages.

        Creating the SIP potentially takes a long time to finish. As this is
        blocking the RabbitMQ I/O loop, this might result in a heartbeat
        timeout and the rabbit broker closing the connection on its end.

        So, we run the SIP creation in a separate thread making sure the
        RabbitMQ I/O loop is not blocked.

        That thread will be appended to a list, in order to be able to wait
        for all threads to finish in the case consuming is stopped.
        """

        self.log.debug(f"Incoming message: {body}")
        # Clean up the list of threads, so it doesn't keep appending
        for t in self.threads:
            if not t.is_alive():
                t.handled = True
        self.threads = [t for t in self.threads if not t.handled]

        thread = threading.Thread(
            target=self.do_work, args=(channel, method.delivery_tag, properties, body)
        )
        thread.handled = False
        thread.start()
        self.threads.append(thread)

    def exit_gracefully(self, signum, frame):
        """Stop consuming queue but finish current tasks/messages."""
        self.log.info(
            "Received SIGTERM. Waiting for last SIP creation to finish and then stops."
        )
        self.rabbit_client.stop_consuming()

    def start(self):
        # Start listening for incoming messages
        self.log.info("Start to listen for messages...")
        self.rabbit_client.listen(self.handle_message)
        # Wait for remaining threads to join after consuming.
        for thread in self.threads:
            thread.join()
        # Ensure callback (n)acks are send
        self.rabbit_client.connection.process_data_events()

        # Close the RabbitMQ connection
        self.rabbit_client.connection.close()
        self.pulsar_client.close()
