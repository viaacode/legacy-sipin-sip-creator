#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Optional
from lxml import etree


class Sidecar:
    """Class used for parsing the metadata sidecar of the essence pair."""

    def __init__(self, path: Path):
        self.root = etree.parse(str(path))
        self.md5 = self.root.findtext("md5")
        self.cp_id = self.root.findtext("CP_id")
        self.dc_source = self.root.findtext("dc_source")
        self.local_id_filename = self.root.findtext(
            "dc_identifiers_localids/bestandsnaam"
        )

    def calculate_original_filename(self) -> Optional[str]:
        """Calculate the original filename

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
