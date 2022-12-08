#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
from datetime import datetime
from enum import Enum
from uuid import uuid4

from lxml import etree

from app.helpers.xml_utils import qname_text


class AgentRole(Enum):
    CREATOR = "CREATOR"
    EDITOR = "EDITOR"
    ARCHIVIST = "ARCHIVIST"
    PRESERVATION = "PRESERVATION"
    DISSEMINATOR = "DISSEMINATOR"
    CUSTODIAN = "CUSTODIAN"
    IPOWNER = "IPOWNER"
    OTHER = "OTHER"


class AgentType(Enum):
    INDIVIDUAL = "INDIVIDUAL"
    ORGANIZATION = "ORGANIZATION"
    OTHER = "OTHER"


class NoteType(Enum):
    SOFTWARE_VERSION = "SOFTWARE VERSION"
    IDENTIFICATIONCODE = "IDENTIFICATIONCODE"


class FileType(Enum):
    DIRECTORY = "DIRECTORY"
    FILE = "FILE"


class FileGrpUse(Enum):
    DOCUMENTATION = "documentation"
    SCHEMAS = "schemas"
    REPRESENTATIONS = "representations"
    METADATA = "metadata"
    DESCRIPTIVE = "descriptive"
    PRESERVATION = "preservation"
    DATA = "data"
    ROOT = "root"


NAMESPACES = {
    "mets": "http://www.loc.gov/METS/",
    "csip": "https://DILCIS.eu/XML/METS/CSIPExtensionMETS",
    "sip": "https://DILCIS.eu/XML/METS/SIPExtensionMETS",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "xlink": "http://www.w3.org/1999/xlink",
}


def generate_uuid() -> str:
    """Generates a UUID with prefix "uuid".

    The ID attribute is of type "xs:id" meaning that it only can begin with a
    letter, not a number. Prefixing the UUID with "uuid" fulfills this requirement.

    Returns:
        The prefixed UUID.
    """
    return f"uuid-{uuid4()}"


class Note:
    """Class representing a METS note.

    Example:
        <mets:note csip:NOTETYPE="SOFTWARE VERSION">2.1.0-beta.7</mets:note>

    Args:
        value: The textual value of the note.
        type: The type of the note.
    """

    NOTE_TAG = etree.QName(NAMESPACES["mets"], "note")

    def __init__(
        self,
        value: str,
        type: NoteType = None,
    ):
        self.value = value
        self.type = type

    def to_element(self):
        """Returns the Note node as an lxml element.

        Returns:
            The Note element."""
        note_attrs = {}
        if self.type:
            note_attrs[qname_text(NAMESPACES, "csip", "NOTETYPE")] = self.type.value
        note_element = etree.Element(self.NOTE_TAG, note_attrs)
        note_element.text = self.value
        return note_element


class Agent:
    """Class representing a METS agent.

    Example:
        <mets:agent ROLE="ARCHIVIST" TYPE="ORGANIZATION">
            <mets:name>The Swedish health agency</mets:name>
            <mets:note csip:NOTETYPE="IDENTIFICATIONCODE">VAT:SE201345098701</mets:note>
        </mets:agent>

    Args:
        role: The role of the agent.
        type: The type of the agent.
        other_role: If the role is "OTHER", this field is needed to denote the value
                    of the other role.
        other_type: If the type is "OTHER", this field is needed to denote the value
                    of the other type.
        name: The name of the agent.
        note: The note of the agent.
    """

    AGENT_TAG = etree.QName(NAMESPACES["mets"], "agent")

    def __init__(
        self,
        role: AgentRole,
        type: AgentType,
        other_role: str = "",
        other_type: str = "",
        name: str = "",
        note: Note = None,
    ):
        self.role = role
        # If role is "OTHER" the other_role needs to be filled in
        if role == AgentRole.OTHER and not other_role:
            raise ValueError("The field 'other_role' is mandatory when role is 'OTHER'")
        self.other_role = other_role

        self.type = type
        # If type is "OTHER" the other_type needs to be filled in
        if type == AgentType.OTHER and not other_type:
            raise ValueError("The field 'other_type' is mandatory when type is 'OTHER'")
        self.other_type = other_type

        self.name = name
        self.note = note

    def to_element(self):
        """Returns the Agent node as an lxml element.

        Returns:
            The Agent element."""
        agents_attrs = {}
        if self.role:
            agents_attrs["ROLE"] = self.role.value
        if self.other_role:
            agents_attrs["OTHERROLE"] = self.other_role

        if self.type:
            agents_attrs["TYPE"] = self.type.value
        if self.other_type:
            agents_attrs["OTHERTYPE"] = self.other_type

        element = etree.Element(self.AGENT_TAG, **agents_attrs)

        if self.name:
            name_tag = etree.QName(NAMESPACES["mets"], "name")
            name_element = etree.Element(name_tag)
            name_element.text = self.name
            element.append(name_element)
        if self.note:
            element.append(self.note.to_element())
        return element


class File:
    """Class representing a File to create sctructMap and fileSec elements.

    Args:
        path: The path to the file.
        checksum: The checksum value of the file used in a fileSec entry.
        file_type: The type: "directory" or "file".
        use: The use used in a fileSec entry.
        label: The label used in a structMap entry.
        mimetype: The mimetype of the file used in a fileSec entry.
        size: The size of the file used in a fileSec entry.
        created: The creation date of the file used in a fileSec entry.
    """

    FILE_TAG = etree.QName(NAMESPACES["mets"], "file")
    FILEGRP_TAG = etree.QName(NAMESPACES["mets"], "fileGrp")
    DIV_TAG = etree.QName(NAMESPACES["mets"], "div")
    MPTR_TAG = etree.QName(NAMESPACES["mets"], "mptr")
    FPTR_TAG = etree.QName(NAMESPACES["mets"], "fptr")
    MDREF_TAG = etree.QName(NAMESPACES["mets"], "mdRef")

    def __init__(
        self,
        path: str = None,
        checksum: str = None,
        file_type: FileType = None,
        use: str = None,
        label: str = "",
        mimetype: str = None,
        size: int = None,
        created: str = None,
        is_mets: bool = False,
    ):

        self.path = path
        self.checksum = checksum
        self.type = file_type
        self.use = use
        self.label = label
        self.mimetype = mimetype
        self.size = size
        self.created = created
        self.children = []
        self.is_mets = is_mets

    def is_fptr(self) -> bool | None:
        """Calculates if a file is a fptr or a mptr

        If a file points to a METS file, it is a mptr (METS pointer).
        In all the other cases it is a fptr (File pointer). This only
        counts for files and not for directories.

        Returns:
            True if a file points to a non-METS file. False if a file points to a
            METS file. None in the case of a directory.

        """
        if self.type == FileType.FILE:
            if not self.is_mets:
                return True
            else:
                return False
        return None

    def add_child(self, file: File):
        """Add a child to the file.

        Args:
            file: The file to add.
        Raises:
            ValueError: When adding a file to a file.
        """
        if self.type == FileType.FILE and file.type == FileType.FILE:
            raise ValueError("A file can not be a child of a file, only of a folder")
        else:
            self.children.append(file)

    def to_filesec_element(self):
        """Returns the fileSec node as an lxml element.

        Returns:
            The fileSec element."""
        if self.type == FileType.DIRECTORY:
            file_tag = self.FILEGRP_TAG
            file_element = etree.Element(file_tag, ID=generate_uuid())
            for child in self.children:
                file_element.append(child.to_filesec_element())
        elif self.type == FileType.FILE:
            file_tag = self.FILE_TAG
            file_element = etree.Element(file_tag, ID=generate_uuid())
        else:
            raise ValueError("No valid type")

        if self.checksum:
            file_element.attrib["CHECKSUM"] = self.checksum
            file_element.attrib["CHECKSUMTYPE"] = "MD5"

        if self.use:
            file_element.attrib["USE"] = self.use

        if self.path:
            flocat_tag = qname_text(NAMESPACES, "mets", "FLocat")
            flocat_attribs = {
                "LOCTYPE": "URL",
                qname_text(NAMESPACES, "xlink", "type"): "simple",
                qname_text(NAMESPACES, "xlink", "href"): self.path,
            }
            flocat_element = etree.Element(flocat_tag, flocat_attribs)
            file_element.append(flocat_element)

        if self.mimetype:
            file_element.attrib["MIMETYPE"] = self.mimetype
        if self.size:
            file_element.attrib["SIZE"] = str(self.size)
        if self.created:
            file_element.attrib["CREATED"] = self.created.astimezone().isoformat()

        return file_element

    def to_structmap_element(self):
        """Returns the structMap node as an lxml element.

        Returns:
            The structMap element."""
        if self.type == FileType.DIRECTORY:
            file_tag = self.DIV_TAG
            file_element = etree.Element(file_tag, ID=generate_uuid(), LABEL=self.label)
            for child in self.children:
                file_element.append(child.to_structmap_element())
        elif self.type == FileType.FILE:
            if self.is_fptr():
                file_tag = self.FPTR_TAG
                file_attrs = {"FILEID": generate_uuid()}
            else:
                file_tag = self.MPTR_TAG
                file_attrs = {
                    qname_text(NAMESPACES, "xlink", "type"): "simple",
                    qname_text(NAMESPACES, "xlink", "href"): self.path,
                    "LOCTYPE": "URL",
                }
            file_element = etree.Element(file_tag, file_attrs)
        else:
            raise ValueError("No valid type")
        return file_element

    def to_dmdsec_element(self):
        """Returns the dmdSec node as an lxml element.

        Returns:
            The dmdSec element."""

        dmdsec_attrs = {
            "ID": generate_uuid(),
            "LOCTYPE": "URL",
            "MDTYPE": "PREMIS",
            qname_text(NAMESPACES, "xlink", "type"): "simple",
            qname_text(NAMESPACES, "xlink", "href"): self.path,
        }
        if self.mimetype:
            dmdsec_attrs["MIMETYPE"] = self.mimetype
        if self.size:
            dmdsec_attrs["SIZE"] = str(self.size)
        if self.created:
            dmdsec_attrs["CREATED"] = self.created.astimezone().isoformat()
        if self.checksum:
            dmdsec_attrs["CHECKSUM"] = self.checksum
            dmdsec_attrs["CHECKSUMTYPE"] = "MD5"
        return etree.Element(self.MDREF_TAG, dmdsec_attrs)

    def to_amdsec_element(self):
        """Returns the amdSec node as an lxml element.

        Returns:
            The amdSec element."""

        digiprov_element = etree.Element(
            etree.QName(NAMESPACES["mets"], "digiprovMD"), {"ID": generate_uuid()}
        )

        amdsec_attrs = {
            "ID": generate_uuid(),
            "LOCTYPE": "URL",
            "MDTYPE": "PREMIS",
            qname_text(NAMESPACES, "xlink", "type"): "simple",
            qname_text(NAMESPACES, "xlink", "href"): self.path,
        }
        if self.mimetype:
            amdsec_attrs["MIMETYPE"] = self.mimetype
        if self.size:
            amdsec_attrs["SIZE"] = str(self.size)
        if self.created:
            amdsec_attrs["CREATED"] = self.created.astimezone().isoformat()
        if self.checksum:
            amdsec_attrs["CHECKSUM"] = self.checksum
            amdsec_attrs["CHECKSUMTYPE"] = "MD5"
        digiprov_element.append(etree.Element(self.MDREF_TAG, amdsec_attrs))
        return digiprov_element


class METSDocSIP:
    """Class representing a METS document with E-ARK SIP extension.

    Args:
        is_package_mets: Denotes if this is the package mets.

        type: The type of the SIP.
        other_type: If the type is "OTHER", this field is needed to denote the value
                    of the other type.
    """

    FILESEC_TAG = etree.QName(NAMESPACES["mets"], "fileSec")
    STRUCTMAP_TAG = etree.QName(NAMESPACES["mets"], "structMap")
    AMDSEC_TAG = etree.QName(NAMESPACES["mets"], "amdSec")
    DMDSEC_TAG = etree.QName(NAMESPACES["mets"], "dmdSec")
    ATTRS = {
        "OBJID": "54c3a254-9c78-494d-a1f1-d07640989038",
        qname_text(
            NAMESPACES, "csip", "CONTENTINFORMATIONTYPE"
        ): "https://data.hetarchief.be/id/sip/1.0/basic",
        "PROFILE": "https://earksip.dilcis.eu/profile/E-ARK-SIP.xml",
    }

    def __init__(self, type: str, is_package_mets: bool = False, other_type: str = ""):
        self.agents = []
        self.files = []
        self.dmdsec = []
        self.amdsec = []
        self.date_created: str = datetime.now().astimezone().isoformat()
        self.is_package_mets = is_package_mets

        self.type = type
        # If type is "OTHER" the other_type needs to be filled in
        if type == "OTHER" and not other_type:
            raise ValueError("The field 'other_type' is mandatory when type is 'OTHER'")
        self.other_type = other_type

    def _document_root(self):
        """Returns the METS root node as an lxml element.

        Returns:
            The root element."""
        attrs = self.ATTRS.copy()
        attrs["TYPE"] = self.type
        if self.other_type:
            attrs["OTHERTYPE"] = self.other_type
        return etree.Element(
            qname_text(NAMESPACES, "mets", "mets"),
            nsmap=NAMESPACES,
            attrib=attrs,
        )

    def _document_hdr(self):
        """Returns the metsHdr node as an lxml element.

        Returns:
            The metsHdr element."""
        hdr_tag = etree.QName(NAMESPACES["mets"], "metsHdr")
        hdr_attrs = {
            "CREATEDATE": self.date_created,
        }
        if self.is_package_mets:
            hdr_attrs[qname_text(NAMESPACES, "csip", "OAISPACKAGETYPE")] = "SIP"
        hdr_element = etree.Element(hdr_tag, **hdr_attrs)
        for agent in self.agents:
            hdr_element.append(agent.to_element())
        return hdr_element

    def _filesec(self):
        """Returns fileSec node for all files as an lxml element.

        Returns:
            The fileSec element."""
        filesec_element = etree.Element(self.FILESEC_TAG, ID=generate_uuid())
        for file in self.files:
            filesec_element.append(file.to_filesec_element())
        return filesec_element

    def _structmap(self):
        """Returns structMap node for all files as an lxml element.

        Returns:
            The structMap element."""
        structmap_attrs = {"ID": generate_uuid(), "TYPE": "PHYSICAL", "LABEL": "CSIP"}
        structmap_element = etree.Element(self.STRUCTMAP_TAG, structmap_attrs)
        for file in self.files:
            structmap_element.append(file.to_structmap_element())
        return structmap_element

    def add_dmdsec(self, file):
        """Add a File as an dmdSec element.

        args:
            file: The file to add.
        """
        self.dmdsec.append(file)

    def add_amdsec(self, file: File):
        """Add a File as an amdSec element.

        args:
            file: The file to add.
        """
        self.amdsec.append(file)

    def _dmdSec(self):
        """Returns dmdSec node including all dmdSec files as an lxml element.

        Returns:
            The dmdSec element."""
        dmdsec_attrs = {"ID": generate_uuid()}
        dmdsec_element = etree.Element(self.DMDSEC_TAG, dmdsec_attrs)
        for file in self.dmdsec:
            dmdsec_element.append(file.to_dmdsec_element())
        return dmdsec_element

    def _amdSec(self):
        """Returns amdSec node including all amdSec files as an lxml element.

        Returns:
            The amdSec element."""
        amdsec_attrs = {"ID": generate_uuid()}
        amdsec_element = etree.Element(self.AMDSEC_TAG, amdsec_attrs)
        for file in self.amdsec:
            amdsec_element.append(file.to_amdsec_element())
        return amdsec_element

    def add_file(self, file: File):
        """Adds a file to the METS docs.

        Args:
            file: File to add.
        """
        self.files.append(file)

    def add_agent(self, agent: Agent):
        """Adds an agent to the METS docs.

        Args:
            file: Agent to add.
        """
        self.agents.append(agent)

    def to_element(self):
        """Returns the METS document as an lxml element.

        Returns:
            The METS document."""
        root = self._document_root()
        # Add metsHdr
        root.append(self._document_hdr())
        # Add dmdSec and amdSec
        root.append(self._dmdSec())
        root.append(self._amdSec())
        # Add files: fileSec and StructMap
        root.append(self._filesec())
        root.append(self._structmap())

        return root
