#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from lxml import etree
from lxml.etree import XMLSyntaxError


class InvalidSidecarException(Exception):
    pass


class Sidecar:
    """Class used for parsing the metadata sidecar of the essence pair."""

    def __init__(self, path: Path):
        try:
            self.root = etree.parse(str(path))
        except XMLSyntaxError as e:
            raise InvalidSidecarException(f"XML syntax error: '{e}'")
        # Mandatory
        self.md5 = self.root.findtext("md5")
        if not self.md5:
            raise InvalidSidecarException("Missing mandatory key: 'md5'")

        # Optional
        self.cp_id = self.root.findtext("CP_id")
        self.dc_source = self.root.findtext("dc_source")
        # Ensure order: Bestandsnaam should have priority over bestandsnaam
        self.local_id_filename = self.root.findtext(
            "dc_identifier_localids/Bestandsnaam"
        )
        if not self.local_id_filename:
            self.local_id_filename = self.root.findtext(
                "dc_identifier_localids/bestandsnaam"
            )
        self.local_id = self.root.findtext("dc_identifier_localid")
        self.local_ids = {}
        for lid in self.root.findall("dc_identifier_localids/*"):
            self.local_ids[lid.tag] = lid.text
        # XDCAM
        self.type_viaa = self.root.findtext("type_viaa")
        self.format = self.root.findtext("format")
        self.sp_name = self.root.findtext("sp_name")
        self.sp_id = self.root.findtext("sp_id")
        self.digitization_date = self.root.findtext("digitization_date")
        self.digitization_time = self.root.findtext("digitization_time")
        self.digitization_note = self.root.findtext("digitization_note")
        self.player_manufacturer = self.root.findtext("player_manufacturer")
        self.player_serial_number = self.root.findtext("player_serial_number")
        self.player_model = self.root.findtext("player_model")
        # Batch ID
        self.batch_id = self.root.findtext("batch_id")

    def calculate_original_filename(self) -> str | None:
        """Calculate the original filename.

        Give preference to the "bestandsnaam" field in the "dc_identifiers_localids"
        list. If it doesn't exists, use the value of the 'dc_source' field.

        If both don't exist, return None.

        Returns:
            The original filename.
        """
        if self.local_id_filename:
            return self.local_id_filename
        elif self.dc_source:
            return self.dc_source
        else:
            return None

    def is_xdcam(self) -> bool:
        """Determines if it is XDCAM.

        Returns:
            True if XDCAM.
        """
        return self.format == "XDCAM"
