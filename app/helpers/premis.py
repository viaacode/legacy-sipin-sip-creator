#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum
from typing import List

from lxml import etree

from app.helpers.xml_utils import qname_text


NSMAP = {
    "premis": "http://www.loc.gov/premis/v3",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "schema": "http://schema.org/",
}


class ObjectCategoryType(Enum):
    IE = "intellectual entity"
    FILE = "file"
    REPRESENTATION = "representation"


class RelationshipSubtype(Enum):
    INCLUDES = "includes"
    REPRESENTED_BY = "is represented by"
    REPRESENTS = "represents"
    INCLUDED_IN = "is included in"


class ObjectType(Enum):
    IE = "intellectualEntity"
    FILE = "file"
    REPRESENTATION = "representation"


class OriginalName:
    """Class representing a originalName node.

    Args:
        name: The original name."""

    def __init__(self, name: str):
        self.name = name

    def to_element(self):
        """Returns the originalName node as an lxml element.

        Returns:
            The originalName element."""

        # Premis original name
        original_name_element = etree.Element(
            qname_text(NSMAP, "premis", "originalName")
        )
        original_name_element.text = self.name

        return original_name_element


class ObjectIdentifier:
    """Class representing a objectIdentifier node.

    Args:
        type: The type of the object identifier.
        value: The value of the object identifier."""

    def __init__(self, type: str, value: str):
        self.type = type
        self.value = value

    def to_element(self):
        """Returns the objectIdentifier node as an lxml element.

        Returns:
            The objectIdentifier element."""

        # Premis object identifier
        object_identifier_element = etree.Element(
            qname_text(NSMAP, "premis", "objectIdentifier")
        )
        # Premis object identifier type
        etree.SubElement(
            object_identifier_element,
            qname_text(NSMAP, "premis", "objectIdentifierType"),
        ).text = self.type
        # Premis object identifier value
        etree.SubElement(
            object_identifier_element,
            qname_text(NSMAP, "premis", "objectIdentifierValue"),
        ).text = self.value

        return object_identifier_element


class RelatedObjectIdentifier:
    """Class representing a relatedObjectIdentifier node.

    Args:
        uuid: The uuid."""

    def __init__(self, uuid: str):
        self.uuid = uuid

    def to_element(self):
        """Returns the relatedObjectIdentifier node as an lxml element.

        Returns:
            The relatedObjectIdentifier element."""

        # Premis related object identifier
        object_identifier_element = etree.Element(
            qname_text(NSMAP, "premis", "relatedObjectIdentifier")
        )
        # Premis related object identifier type
        etree.SubElement(
            object_identifier_element,
            qname_text(NSMAP, "premis", "relatedObjectIdentifierType"),
        ).text = "UUID"
        # Premis related object identifier value
        etree.SubElement(
            object_identifier_element,
            qname_text(NSMAP, "premis", "relatedObjectIdentifierValue"),
        ).text = self.uuid

        return object_identifier_element


class Relationship:
    """Class representing a relationship node.

    Args:
        subtype: The subtype of the relationship.
        uuid: The uuid.
    """

    TYPE_URI_MAP = {
        RelationshipSubtype.INCLUDES: "inc",
        RelationshipSubtype.REPRESENTED_BY: "isr",
        RelationshipSubtype.REPRESENTS: "rep",
        RelationshipSubtype.INCLUDED_IN: "isi",
    }

    def __init__(self, subtype: RelationshipSubtype, uuid: str):
        self.subtype = subtype
        self.uuid = uuid

    def to_element(self):
        """Returns the relationship node as an lxml element.

        Returns:
            The relationship element."""

        # Premis relationship
        relationship_element = etree.Element(
            qname_text(NSMAP, "premis", "relationship")
        )
        # type
        relationship_type_attributes = {
            "authority": "relationshipType",
            "authorityURI": "http://id.loc.gov/vocabulary/preservation/relationshipType",
            "valueURI": "http://id.loc.gov/vocabulary/preservation/relationshipType/str",
        }
        etree.SubElement(
            relationship_element,
            qname_text(NSMAP, "premis", "relationshipType"),
            attrib=relationship_type_attributes,
        ).text = "structural"

        # Subtype
        relationship_subtype_attributes = {
            "authority": "relationshipSubType",
            "authorityURI": "http://id.loc.gov/vocabulary/preservation/relationshipSubType",
            "valueURI": f"http://id.loc.gov/vocabulary/preservation/relationshipSubType/{self.TYPE_URI_MAP[self.subtype]}",
        }
        etree.SubElement(
            relationship_element,
            qname_text(NSMAP, "premis", "relationshipSubtype"),
            attrib=relationship_subtype_attributes,
        ).text = self.subtype.value

        # Related object identifier
        relationship_element.append(RelatedObjectIdentifier(self.uuid).to_element())

        return relationship_element


class Fixity:
    """Class representing the Fixity information contained in a ObjectCharacteristics node.

    Args:
        md5: The md5.
    """

    def __init__(self, md5: str = None):
        self.md5 = md5

    def to_element(self):
        """Returns the fixity node as an lxml element.

        If the md5 value is empty, the fixity node will be empty.

        Returns:
            The Premis fixity element."""

        # Premis object characteristics
        object_characteristics_element = etree.Element(
            qname_text(NSMAP, "premis", "objectCharacteristics"),
        )
        fixity_element = etree.SubElement(
            object_characteristics_element,
            qname_text(NSMAP, "premis", "fixity"),
        )
        if self.md5:
            etree.SubElement(
                fixity_element,
                qname_text(NSMAP, "premis", "messageDigestAlgorithm"),
                attrib={
                    "authority": "cryptographicHashFunctions",
                    "authorityURI": "http://id.loc.gov/vocabulary/preservation/cryptographicHashFunctions",
                    "valueURI": "http://id.loc.gov/vocabulary/preservation/cryptographicHashFunctions/md5",
                },
            ).text = "MD5"
            etree.SubElement(
                fixity_element,
                qname_text(NSMAP, "premis", "messageDigest"),
            ).text = self.md5

        return object_characteristics_element


class ObjectCategory:
    """Class representing a objectCategory node.

    Args:
        category: The category."""

    def __init__(self, category: ObjectCategoryType):
        self.category = category

    def to_element(self):
        """Returns the objectCategory node as an lxml element.

        Returns:
            The objectCategory element."""

        # Premis object category
        object_category_element = etree.Element(
            qname_text(NSMAP, "premis", "objectCategory"),
        )
        object_category_element.text = self.category.value

        return object_category_element


class Storage:
    """Class representing a storage node.

    Only supports the simple variant with only "storageMedium".

    Args:
        storage_medium: The storage medium.
    """

    def __init__(self, storage_medium: str):
        self.storage_medium = storage_medium

    def to_element(self):
        """Returns the storage node as an lxml element.

        Returns:
            The storage element."""

        # Premis storage
        storage_element = etree.Element(
            qname_text(NSMAP, "premis", "storage"),
        )
        etree.SubElement(
            storage_element,
            qname_text(NSMAP, "premis", "storageMedium"),
        ).text = self.storage_medium

        return storage_element


class Object:
    """Class representing a object node.

    Args:
        type: The object type.
        identifiers: The object identifiers.
        original_name: The original name.
        fixity: The fixity element.
        relationships: The relationships.
        storages: The storages.
    """

    def __init__(
        self,
        type: ObjectType,
        identifiers: List[ObjectIdentifier],
        original_name: OriginalName = None,
        fixity: Fixity = None,
        relationships: List[Relationship] = None,
        storages: List[Storage] = None,
    ):
        self.type: ObjectType = type
        self.identifiers = identifiers
        self.original_name = original_name
        self.fixity = fixity
        self.relationships = relationships if relationships else []
        self.storages = storages if storages else []

    def add_relationship(self, relationship: Relationship):
        self.relationships.append(relationship)

    def add_identifier(self, identifier: ObjectIdentifier):
        self.identifiers.append(identifier)

    def add_storage(self, storage: Storage):
        self.storages.append(storage)

    def to_element(self):
        """Returns the object node as an lxml element.

        Returns:
            The object element."""

        # Premis object
        object_attributes = {
            qname_text(NSMAP, "xsi", "type"): f"premis:{self.type.value}"
        }
        object_element = etree.Element(
            qname_text(NSMAP, "premis", "object"), attrib=object_attributes
        )

        # Premis original name
        if self.original_name:
            object_element.append(self.original_name.to_element())

        # Premis object identifiers
        for identifier in self.identifiers:
            object_element.append(identifier.to_element())

        # Premis fixity
        if self.fixity:
            object_element.append(self.fixity.to_element())

        # Storage
        for storage in self.storages:
            object_element.append(storage.to_element())

        # Premis relationships
        for relationship in self.relationships:
            object_element.append(relationship.to_element())

        return object_element


class AgentIdentifier:
    """Class representing a agentIdentifier node.

    This is a part of the Agent node.

    Args:
        type: The type of the agent identifier.
        value: The value of the agent identifier."""

    def __init__(self, type: str, value: str):
        self.type = type
        self.value = value

    def to_element(self):
        """Returns the agentIdentifier node as an lxml element.

        Returns:
            The agentIdentifier element."""

        # Premis agent identifier
        agent_identifier_element = etree.Element(
            qname_text(NSMAP, "premis", "agentIdentifier")
        )
        # Premis agent identifier type
        etree.SubElement(
            agent_identifier_element,
            qname_text(NSMAP, "premis", "agentIdentifierType"),
        ).text = self.type
        # Premis agent identifier value
        etree.SubElement(
            agent_identifier_element,
            qname_text(NSMAP, "premis", "agentIdentifierValue"),
        ).text = self.value

        return agent_identifier_element


class AgentExtension:
    """Class representing an agent extension.

    This is a part of the Agent node.

    Args:
        model: The model.
        brand_name: The brand name.
        serial_number: The serial number.
    """

    def __init__(
        self,
        model: str = "",
        brand_name: str = "",
        serial_number: str = "",
    ):
        self.model = model
        self.brand_name = brand_name
        self.serial_number = serial_number

    def to_element(self):
        """Returns the agent extension as an lxml element.

        Returns:
            The agent extension element."""

        # Premis agent extension
        agent_extension_element = etree.Element(
            qname_text(NSMAP, "premis", "agentExtension")
        )

        # Premis agent extension model
        if self.model:
            etree.SubElement(
                agent_extension_element,
                qname_text(NSMAP, "schema", "model"),
            ).text = self.model

        # Premis agent extension brand
        if self.brand_name:
            brand_element = etree.SubElement(
                agent_extension_element,
                qname_text(NSMAP, "schema", "brand"),
            )
            etree.SubElement(
                brand_element,
                qname_text(NSMAP, "schema", "name"),
            ).text = self.brand_name

        # Premis agent extension serial number
        if self.serial_number:
            etree.SubElement(
                agent_extension_element,
                qname_text(NSMAP, "schema", "serialNumber"),
            ).text = self.serial_number

        return agent_extension_element


class Agent:
    """Class representing an agent node.

    Args:
        identifiers: The agent identifiers.
        name: The agent name.
        type: The agent type.
    """

    def __init__(
        self,
        identifiers: List[AgentIdentifier],
        type: str = "",
        name: str = "",
        extension: AgentExtension = None,
    ):
        self.identifiers: List[AgentIdentifier] = identifiers
        self.type = type
        self.name = name
        self.extension = extension

    def add_identifier(self, identifier: AgentIdentifier):
        self.identifiers.append(identifier)

    def to_element(self):
        """Returns the agent node as an lxml element.

        Returns:
            The agent element."""

        # Premis agent
        agent_element = etree.Element(qname_text(NSMAP, "premis", "agent"))

        # Premis object identifiers
        for identifier in self.identifiers:
            agent_element.append(identifier.to_element())

        # Premis agent name
        if self.name:
            etree.SubElement(
                agent_element,
                qname_text(NSMAP, "premis", "agentName"),
            ).text = self.name

        # Premis agent type
        if self.type:
            etree.SubElement(
                agent_element,
                qname_text(NSMAP, "premis", "agentType"),
            ).text = self.type

        # Premis agent extension
        if self.extension:
            agent_element.append(self.extension.to_element())

        return agent_element


class EventIdentifier:
    """Class representing a eventIdentifier node.

    This is a part of the Event node.

    Args:
        type: The type of the event identifier.
        value: The value of the event identifier."""

    def __init__(self, type: str, value: str):
        self.type = type
        self.value = value

    def to_element(self):
        """Returns the eventIdentifier node as an lxml element.

        Returns:
            The eventIdentifier element."""

        # Premis event identifier
        event_identifier_element = etree.Element(
            qname_text(NSMAP, "premis", "eventIdentifier")
        )
        # Premis event identifier type
        etree.SubElement(
            event_identifier_element,
            qname_text(NSMAP, "premis", "eventIdentifierType"),
        ).text = self.type
        # Premis event identifier value
        etree.SubElement(
            event_identifier_element,
            qname_text(NSMAP, "premis", "eventIdentifierValue"),
        ).text = self.value

        return event_identifier_element


class EventDetailInformation:
    """Class representing a eventDetailInformation node.

    This is a part of the Event node.

    Args:
        detail: The detail"""

    def __init__(self, detail: str):
        self.detail = detail

    def to_element(self):
        """Returns the eventDetailInformation node as an lxml element.

        Returns:
            The eventDetailInformation element."""

        # Premis event detail information
        event_detail_information_element = etree.Element(
            qname_text(NSMAP, "premis", "eventDetailInformation")
        )
        # Premis event detail
        etree.SubElement(
            event_detail_information_element,
            qname_text(NSMAP, "premis", "eventDetail"),
        ).text = self.detail

        return event_detail_information_element


class Event:
    """Class representing an event node.

    Args:
        identifier: The event identifier.
        type: The event type.
        date_time: The event datetime.
        note: The event note.
    """

    def __init__(
        self,
        identifier: EventIdentifier,
        type: str,
        date_time: str,
        event_detail_informations: List[EventDetailInformation] = None,
    ):
        self.identifier = identifier
        self.type = type
        self.date_time = date_time
        self.event_detail_informations = (
            event_detail_informations if event_detail_informations else []
        )

    def to_element(self):
        """Returns the event node as an lxml element.

        Returns:
            The event element."""

        # Premis event
        event_element = etree.Element(qname_text(NSMAP, "premis", "event"))

        # Premis object identifier
        event_element.append(self.identifier.to_element())

        # Premis event type
        etree.SubElement(
            event_element,
            qname_text(NSMAP, "premis", "eventType"),
        ).text = self.type

        # Premis event datetime
        etree.SubElement(
            event_element,
            qname_text(NSMAP, "premis", "eventDateTime"),
        ).text = self.date_time

        # Premis event detail information (note)
        for event_detail_information in self.event_detail_informations:
            event_element.append(event_detail_information.to_element())

        return event_element


class Premis:
    """Class representing the premis root node."""

    ATTRS = {"version": "3.0"}

    def __init__(self):
        self.objects: List[Object] = []
        self.events: List[Event] = []
        self.agents: List[Agent] = []

    def add_object(self, object: Object):
        self.objects.append(object)

    def add_event(self, event: Event):
        self.events.append(event)

    def add_agent(self, agent: Agent):
        self.agents.append(agent)

    def to_element(self):
        """Returns the premis node as an lxml element.

        Returns:
            The premis element."""

        # Premis premis
        premis_element = etree.Element(
            qname_text(NSMAP, "premis", "premis"), nsmap=NSMAP, attrib=self.ATTRS
        )
        # Add the objects
        for obj in self.objects:
            premis_element.append(obj.to_element())

        # Add the events
        for event in self.events:
            premis_element.append(event.to_element())

        # Add the agents
        for agent in self.agents:
            premis_element.append(agent.to_element())

        return premis_element
