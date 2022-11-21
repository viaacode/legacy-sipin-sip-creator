#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path
from json import JSONDecodeError
from typing import List, Union


class InvalidMessageException(Exception):
    pass


class SIPItem:
    """Class representing the information of a SIP item

    This is a composite part of the watchfolder message.

    Args:
        message: The SIP item.
    """

    def __init__(self, sip_item: dict):
        self.file_name = sip_item["file_name"]
        self.file_path = sip_item["file_path"]


class WatchfolderMessage:
    """Class representing an incoming watchfolder message

    Args:
        message: The incoming watchfolder message.
    """

    def __init__(self, message: bytes):
        try:
            msg: dict = json.loads(message)
        except JSONDecodeError as e:
            raise InvalidMessageException(f"Message is not valid JSON: '{e}'")
        try:
            self.cp_name = msg["cp_name"]
            self.flow_id = msg["flow_id"]
            self.files = {}
            collaterals = []
            for sip_package in msg["sip_package"]:
                if sip_package["file_type"] == "collateral":
                    collaterals.append(SIPItem(sip_package))
                else:
                    self.files[sip_package["file_type"]] = SIPItem(sip_package)

            self.files["collateral"] = collaterals

        except KeyError as e:
            raise InvalidMessageException(f"Missing mandatory key: {e}")

    def _get_files(self, file_type: str) -> Union[SIPItem, List[SIPItem]]:
        """Return the SIPItem(s) of a file in the incoming SIP.

        Only the type 'sidecar', 'essence' or 'collateral' is allowed.

        There should be only one file of type 'sidecar' and 'essence'.
        It is possible to have multiple files op type 'collateral'.

        Args:
            file_type: The type of the file.

        Returns: The SIPItem(s).
        """
        try:
            return self.files[file_type]
        except KeyError:
            raise ValueError(
                "Not a valid file type of the incoming SIP: {file_type}. Only 'sidecar', 'essence' or 'collateral' is allowed"
            )

    def get_essence_path(self) -> Path:
        """Return the path of the essence file.

        Returns: The essence file as a Path.
        """
        file = self._get_files("essence")
        return Path(file.file_path, file.file_name)

    def get_xml_path(self) -> Path:
        """Return the path of the metadata file.

        Returns: The metadata file as a Path.
        """

        file = self._get_files("sidecar")
        return Path(file.file_path, file.file_name)

    def get_collateral_paths(self) -> list[Path]:
        """Return the paths of the collateral files.

        Returns: The collateral files as list of Paths.
        """
        return [
            Path(file.file_path, file.file_name)
            for file in self._get_files("collateral")
        ]
