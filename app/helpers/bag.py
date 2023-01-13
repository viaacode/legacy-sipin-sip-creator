#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

import bagit
from lxml import etree

from app.helpers.dc import DC
from app.helpers.events import WatchfolderMessage
from app.helpers.mets import (
    METSDocSIP,
    Agent,
    AgentRole,
    AgentType,
    Note,
    NoteType,
    File,
    FileGrpUse,
    FileType,
    generate_uuid,
)
from app.helpers.premis import (
    Agent as PremisAgent,
    AgentExtension,
    AgentIdentifier,
    Event,
    EventDetailInformation,
    EventIdentifier,
    Fixity,
    LinkingAgentIdentifier,
    LinkingAgentRole,
    LinkingObjectIdentifier,
    LinkingObjectRole,
    Object,
    ObjectIdentifier,
    ObjectType,
    OriginalName,
    Relationship,
    RelationshipSubtype,
    Storage,
    Premis,
)
from app.helpers.sidecar import Sidecar
from app.services.org_api import OrgApiClient

EXTENSION_MIMETYPE_MAP = {
    ".jpg": "image/jpeg",
    ".pdf": "application/pdf",
    ".tiff": "image/tiff",
    ".tif": "image/tiff",
    ".mxf": "application/mxf",
    ".mov": "video/quicktime",
    ".mp4": "video/mp4",
    ".mp3": "audio/mpeg",
    ".wav": "audio/x-wav",
    ".jp2": "image/jp2",
    ".jpeg": "image/jpeg",
    ".mp2": "audio/mpeg",
    ".mpg": "video/mpeg",
    ".ogg": "audio/ogg",
    ".zip": "application/zip",
    ".ts": "video/MP2T",
    ".m4v": "video/mp4",
    ".xml": "application/xml",
    ".psb": "application/vnd.adobe.photoshop",
    ".mpeg": "video/mpeg",
    ".mts": "video/MP2T",
    ".srt": "text/plain",
    ".mkv": "video/x-matroska",
}

MIMETYPE_TYPE_MAP = {
    "image/jpeg": "Photographs - Digital",
    "image/tiff": "Photographs - Digital",
    "image/jp2": "Photographs - Digital",
    "audio/mpeg": "Audio - Media-independent (digital)",
    "audio/x-wav": "Audio - Media-independent (digital)",
    "audio/ogg": "Audio - Media-independent (digital)",
    "application/pdf": "Textual works - Digital",
    "application/zip": "Collection",
    "video/quicktime": "Video - File-based and Physical Media",
    "video/mp4": "Video - File-based and Physical Media",
    "video/MP2T": "Video - File-based and Physical Media",
    "video/mpeg": "Video - File-based and Physical Media",
    "application/mxf": "Video - File-based and Physical Media",
    "application/vnd.adobe.photoshop": "Photographs - Digital",
    "video/x-matroska": "Video - File-based and Physical Media",
}


def guess_mimetype(file: Path) -> str | None:
    """Calculate the mimetype of a path based on the extension.

    Args:
        The path of the file.

    Returns:
        The mimetype.
    """
    try:
        return EXTENSION_MIMETYPE_MAP[file.suffix.lower()]
    except KeyError:
        return None


def calculate_sip_type(mimetype: str) -> str:
    """Calculate the type of the SIP based on the mimetype of the essence.

    Args:
        Mimetype to map to the type.

    Returns:
        The type of the SIP.
    """
    try:
        return MIMETYPE_TYPE_MAP[mimetype]
    except KeyError:
        return "OTHER"


def md5(file: Path) -> str:
    """Calculate the md5 of a given file.

    Args:
        File to calculate the md5 for.

    Returns:
        The md5 value in hex value.
    """
    hash_md5 = hashlib.md5()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


class Bag:
    def __init__(
        self,
        watchfolder_message: WatchfolderMessage,
        sidecar: Sidecar,
        org_api_client: OrgApiClient,
    ):
        self.watchfolder_message: WatchfolderMessage = watchfolder_message
        self.sidecar: Sidecar = sidecar
        self.org_api_client: OrgApiClient = org_api_client

    def _create_package_mets(self, sip_root_folder: Path):
        """Create the package METS.

        Args:
            sip_root_folder: The root folder of the SIP.

        Returns:
            The METS document as an lxml element.
        """
        # METS doc
        doc = METSDocSIP(
            is_package_mets=True,
            type=calculate_sip_type(
                guess_mimetype(self.watchfolder_message.get_essence_path())
            ),
        )

        # Mandatory agent
        mandatory_agent = Agent(
            AgentRole.CREATOR,
            AgentType.OTHER,
            other_type="SOFTWARE",
            name="meemoo SIP creator",
            note=Note("0.1.0", NoteType.SOFTWARE_VERSION),
        )
        doc.add_agent(mandatory_agent)

        cp_name = self.org_api_client.get_label(self.watchfolder_message.flow_id)
        # Archival agent
        archival_agent = Agent(
            AgentRole.ARCHIVIST, AgentType.ORGANIZATION, name=cp_name
        )
        doc.add_agent(archival_agent)

        # Submitting agent
        submitting_agent = Agent(
            AgentRole.CREATOR,
            AgentType.ORGANIZATION,
            name=cp_name,
            note=Note(self.watchfolder_message.flow_id, NoteType.IDENTIFICATIONCODE),
        )
        doc.add_agent(submitting_agent)

        root_folder = File(file_type=FileType.DIRECTORY, use=FileGrpUse.ROOT.value)
        metadata_folder = File(
            file_type=FileType.DIRECTORY,
            use=FileGrpUse.METADATA.value,
            label=FileGrpUse.METADATA.value,
        )
        metadata_desc_folder = File(
            file_type=FileType.DIRECTORY,
            use=f"{FileGrpUse.METADATA.value}/{FileGrpUse.DESCRIPTIVE.value}",
            label=FileGrpUse.DESCRIPTIVE.value,
        )
        metadata_pres_folder = File(
            file_type=FileType.DIRECTORY,
            use=f"{FileGrpUse.METADATA.value}/{FileGrpUse.PRESERVATION.value}",
            label=FileGrpUse.PRESERVATION.value,
        )

        # The descriptive metadata on IE level
        desc_ie_path_rel = Path("metadata", "descriptive", "dc.xml")
        desc_ie_path = Path(sip_root_folder, desc_ie_path_rel)
        desc_ie_file = File(
            file_type=FileType.FILE,
            label="descriptive",
            checksum=md5(desc_ie_path),
            size=desc_ie_path.stat().st_size,
            mimetype=guess_mimetype(desc_ie_path),
            created=datetime.fromtimestamp(desc_ie_path.stat().st_ctime),
            path=str(desc_ie_path_rel),
        )
        metadata_desc_folder.add_child(desc_ie_file)

        # The preservation metadata on IE level
        pres_ie_path_rel = Path("metadata", "preservation", "premis.xml")
        pres_ie_path = Path(sip_root_folder, pres_ie_path_rel)
        pres_ie_file = File(
            file_type=FileType.FILE,
            label="preservation",
            checksum=md5(pres_ie_path),
            size=pres_ie_path.stat().st_size,
            mimetype=guess_mimetype(pres_ie_path),
            created=datetime.fromtimestamp(pres_ie_path.stat().st_ctime),
            path=str(pres_ie_path_rel),
        )
        metadata_pres_folder.add_child(pres_ie_file)

        metadata_preserv_folder = File(
            file_type=FileType.DIRECTORY,
            use=f"{FileGrpUse.METADATA.value}/{FileGrpUse.PRESERVATION.value}",
            label=FileGrpUse.PRESERVATION.value,
        )
        reps_folder = File(
            file_type=FileType.DIRECTORY,
            use=FileGrpUse.REPRESENTATIONS.value,
            label=FileGrpUse.REPRESENTATIONS.value,
        )
        reps_folder_1 = File(
            file_type=FileType.DIRECTORY,
            use=f"{FileGrpUse.REPRESENTATIONS.value}/representation_1",
            label="representation_1",
        )

        # The representation METS File used for fileSec and structMap
        reps_path_rel = Path("representations", "representation_1", "mets.xml")
        reps_path = Path(sip_root_folder, reps_path_rel)
        reps_file = File(
            file_type=FileType.FILE,
            label="representation_1",
            checksum=md5(reps_path),
            size=reps_path.stat().st_size,
            mimetype=guess_mimetype(reps_path),
            created=datetime.fromtimestamp(reps_path.stat().st_ctime),
            path=str(reps_path_rel),
            is_mets=True,
        )
        reps_folder_1.add_child(reps_file)

        reps_folder.add_child(reps_folder_1)

        metadata_folder.add_child(metadata_desc_folder)
        metadata_folder.add_child(metadata_preserv_folder)

        root_folder.add_child(metadata_folder)
        root_folder.add_child(reps_folder)

        doc.add_file(root_folder)

        # dmdsec / amdsec
        doc.add_dmdsec(desc_ie_file)
        doc.add_amdsec(pres_ie_file)

        return doc.to_element()

    def _create_representation_mets(self, sip_root_folder: Path):
        """Create the representation METS.

        Args:
            sip_root_folder: The root folder of the SIP.

        Returns:
            The METS document as an lxml element.
        """
        # METS doc
        doc = METSDocSIP(
            type=calculate_sip_type(
                guess_mimetype(self.watchfolder_message.get_essence_path())
            ),
        )

        essence_file_name: Path = self.watchfolder_message.get_essence_path().name
        collaterals_file_names: list[Path] = [
            path.name for path in self.watchfolder_message.get_collateral_paths()
        ]

        metadata_folder = File(
            file_type=FileType.DIRECTORY,
            use=FileGrpUse.METADATA.value,
            label=FileGrpUse.METADATA.value,
        )
        metadata_desc_folder = File(
            file_type=FileType.DIRECTORY,
            use=f"{FileGrpUse.METADATA.value}/{FileGrpUse.DESCRIPTIVE.value}",
            label=FileGrpUse.DESCRIPTIVE.value,
        )
        metadata_preserv_folder = File(
            file_type=FileType.DIRECTORY,
            use=f"{FileGrpUse.METADATA.value}/{FileGrpUse.PRESERVATION.value}",
            label=FileGrpUse.PRESERVATION.value,
        )
        data_folder = File(
            file_type=FileType.DIRECTORY,
            use=FileGrpUse.DATA.value,
            label=FileGrpUse.DATA.value,
        )

        representation_path = Path("representations", "representation_1")

        # The preservation metadata file used for fileSec and structMap
        pres_path_rel = Path(
            representation_path, "metadata", "preservation", "premis.xml"
        )
        pres_path = Path(sip_root_folder, pres_path_rel)
        pres_file = File(
            file_type=FileType.FILE,
            use=FileGrpUse.PRESERVATION.value,
            label=FileGrpUse.PRESERVATION.value,
            mimetype=guess_mimetype(pres_path),
            path=str(pres_path_rel),
            size=pres_path.stat().st_size,
            checksum=md5(pres_path),
            created=datetime.fromtimestamp(pres_path.stat().st_ctime),
        )
        metadata_preserv_folder.add_child(pres_file)

        # The essence file used for fileSec and structMap
        data_path_rel = Path(representation_path, "data", essence_file_name)
        data_path = Path(sip_root_folder, data_path_rel)
        data_file = File(
            file_type=FileType.FILE,
            use=FileGrpUse.DATA.value,
            label=FileGrpUse.DATA.value,
            mimetype=guess_mimetype(data_path),
            path=str(data_path_rel),
            size=data_path.stat().st_size,
            checksum=self.sidecar.md5,
            created=datetime.fromtimestamp(data_path.stat().st_ctime),
        )
        data_folder.add_child(data_file)

        # The collateral files used for fileSec and structMap
        for collaterals_file_name in collaterals_file_names:
            collateral_path_rel = Path(
                representation_path, "data", collaterals_file_name
            )
            collateral_path = Path(sip_root_folder, collateral_path_rel)
            collateral_file = File(
                file_type=FileType.FILE,
                use=FileGrpUse.DATA.value,
                label=FileGrpUse.DATA.value,
                mimetype=guess_mimetype(collateral_path),
                path=str(collateral_path),
                size=collateral_path.stat().st_size,
                checksum=md5(collateral_path),
                created=datetime.fromtimestamp(collateral_path.stat().st_ctime),
            )
            data_folder.add_child(collateral_file)

        # Add folders
        metadata_folder.add_child(metadata_desc_folder)
        metadata_folder.add_child(metadata_preserv_folder)

        doc.add_file(metadata_folder)
        doc.add_file(data_folder)

        # amdsec
        doc.add_amdsec(pres_file)

        return doc.to_element()

    def _write_descriptive_metadata_ie(self, folder: Path, dc: Path, ie_uuid: str):
        dc_terms = DC.transform(
            dc,
            ie_uuid=etree.XSLT.strparam(ie_uuid),
        )
        etree.ElementTree(dc_terms).write(
            str(folder.joinpath("dc.xml")),
            pretty_print=True,
        )

    def _write_preservation_metadata_ie(
        self, folder: Path, ie_uuid: str, rep_uuid: str
    ):
        premis_element = Premis()
        # Premis object IE
        premis_object_element_ie = Object(
            ObjectType.IE, [ObjectIdentifier("uuid", ie_uuid)]
        )
        # Premis identifiers
        # local_id
        premis_object_element_ie.add_identifier(
            ObjectIdentifier("local_id", self.sidecar.local_id)
        )

        # local_ids
        for type, value in self.sidecar.local_ids.items():
            if type not in ("bestandsnaam", "Bestandsnaam"):
                premis_object_element_ie.add_identifier(ObjectIdentifier(type, value))
        # Premis object IE relationship
        premis_object_element_ie_relationship = Relationship(
            RelationshipSubtype.REPRESENTED_BY, [rep_uuid]
        )
        premis_object_element_ie.add_relationship(premis_object_element_ie_relationship)

        premis_element.add_object(premis_object_element_ie)

        # XDCAM
        if self.sidecar.is_xdcam():

            # UUIDs
            player_agent_uuid = generate_uuid()
            premis_object_rep_uuid = generate_uuid()

            # Premis object representation
            premis_object_element_rep = Object(
                ObjectType.REPRESENTATION,
                identifiers=[ObjectIdentifier("uuid", premis_object_rep_uuid)],
                storages=[Storage("XDCAM")],
            )

            premis_element.add_object(premis_object_element_rep)

            # Premis event
            premis_event = Event(
                EventIdentifier("UUID", generate_uuid()),
                "DIGITIZATION",
                f"{self.sidecar.digitization_date}T{self.sidecar.digitization_time}",
                event_detail_informations=[
                    EventDetailInformation(self.sidecar.digitization_note)
                ],
                linking_agent_identifiers=[
                    LinkingAgentIdentifier(
                        "VIAA SP Agent ID",
                        self.sidecar.sp_id,
                        roles=[
                            LinkingAgentRole(
                                "implementer",
                                value_uri="http://id.loc.gov/vocabulary/preservation/eventRelatedAgentRole/imp",
                            ),
                        ],
                    ),
                    LinkingAgentIdentifier(
                        "UUID",
                        player_agent_uuid,
                        roles=[
                            LinkingAgentRole("player"),
                        ],
                    ),
                ],
                linking_object_identifiers=[
                    LinkingObjectIdentifier(
                        "UUID",
                        rep_uuid,
                        roles=[
                            LinkingObjectRole(
                                "outcome",
                                value_uri="http://id.loc.gov/vocabulary/preservation/eventRelatedObjectRole/out",
                            ),
                        ],
                    ),
                    LinkingObjectIdentifier(
                        "UUID",
                        premis_object_rep_uuid,
                        roles=[
                            LinkingObjectRole(
                                "source",
                                value_uri="http://id.loc.gov/vocabulary/preservation/eventRelatedObjectRole/out",
                            ),
                        ],
                    ),
                ],
            )

            premis_element.add_event(premis_event)

            # Premis Agent SP
            premis_agent_sp = PremisAgent(
                [AgentIdentifier("VIAA SP Agent ID", self.sidecar.sp_id)],
                type="SP Agent",
                name=self.sidecar.sp_name,
            )

            premis_element.add_event(premis_agent_sp)

            # Premis Agent player
            premis_agent_type_extension = AgentExtension(
                model=self.sidecar.player_model,
                brand_name=self.sidecar.player_manufacturer,
                serial_number=self.sidecar.player_serial_number,
            )
            premis_agent_type = PremisAgent(
                [AgentIdentifier("UUID", player_agent_uuid)],
                type="player",
                name=f"{self.sidecar.player_manufacturer} {self.sidecar.player_model}",
                extension=premis_agent_type_extension,
            )

            premis_element.add_agent(premis_agent_type)

        # Write preservation data on IE level.
        etree.ElementTree(premis_element.to_element()).write(
            str(folder.joinpath("premis.xml")),
            pretty_print=True,
        )

    def _write_preservation_metadata_representation(
        self,
        folder: Path,
        essence: Path,
        rep_uuid: str,
        file_uuid: str,
        ie_uuid: str,
        collaterals: dict[str, Path],
    ):
        premis_element = Premis()
        # Premis object representation
        premis_object_element_rep = Object(
            ObjectType.REPRESENTATION,
            [ObjectIdentifier("uuid", rep_uuid)],
        )
        # Premis object representation relationships
        premis_object_element_rep_relation_includes = Relationship(
            RelationshipSubtype.INCLUDES, [file_uuid] + list(collaterals.keys())
        )
        premis_object_element_rep.add_relationship(
            premis_object_element_rep_relation_includes
        )

        premis_object_element_rep_relation_represents = Relationship(
            RelationshipSubtype.REPRESENTS, [ie_uuid]
        )
        premis_object_element_rep.add_relationship(
            premis_object_element_rep_relation_represents
        )

        # Calculate original name
        # First of, check in the sidecar metadata in order of existence:
        #   VIAA/dc_identifier_localids/Bestandsnaam
        #   VIAA/dc_identifier_localids/bestandsnaam
        #   VIAA/dc_source
        # If not available, use the filename of the essence
        original_name = self.sidecar.calculate_original_filename()
        if not original_name:
            original_name = essence.name
        premis_element.add_object(premis_object_element_rep)

        # Premis object file
        premis_object_element_file = Object(
            ObjectType.FILE,
            [ObjectIdentifier("uuid", file_uuid)],
            original_name=OriginalName(original_name),
            fixity=Fixity(self.sidecar.md5),
        )

        # Premis object file relationship with its representation
        premis_object_element_file_relation_rep = Relationship(
            RelationshipSubtype.INCLUDED_IN, [rep_uuid]
        )
        premis_object_element_file.add_relationship(
            premis_object_element_file_relation_rep
        )

        # Premis object file relationship with collaterals
        if collaterals:
            premis_object_element_file_relation_cols = Relationship(
                RelationshipSubtype.IS_REQUIRED_BY, list(collaterals.keys())
            )
            premis_object_element_file.add_relationship(
                premis_object_element_file_relation_cols
            )

        premis_element.add_object(premis_object_element_file)

        # Premis object collateral files
        for uuid, path in collaterals.items():
            premis_object_element_collateral = Object(
                ObjectType.FILE,
                [ObjectIdentifier("uuid", uuid)],
                original_name=OriginalName(path.name),
                fixity=Fixity(md5(path)),
            )
            # Premis object collateral relationship with its representation
            premis_object_element_collateral_relation_rep = Relationship(
                RelationshipSubtype.INCLUDED_IN, [rep_uuid]
            )
            premis_object_element_collateral.add_relationship(
                premis_object_element_collateral_relation_rep
            )

            # Premis object collateral relationship with its video file
            premis_object_element_collateral_relation_file = Relationship(
                RelationshipSubtype.REQUIRES, [file_uuid]
            )
            premis_object_element_collateral.add_relationship(
                premis_object_element_collateral_relation_file
            )

            premis_element.add_object(premis_object_element_collateral)

        etree.ElementTree(premis_element.to_element()).write(
            str(folder.joinpath("premis.xml")),
            pretty_print=True,
        )

    def create_sip_bag(self) -> tuple[Path, bagit.Bag]:
        """Create the SIP in the bag format.

        - Create the minimal SIP
        - Create a bag from the minimal SIP
        - Zip the bag
        - Remove the folder

        Structure of SIP:
            mets.xml
            metadata/
                descriptive/
                    dc.xml
                preservation/
                    premis.xml
            representations/representation_1/
                data/
                    essence.ext
                    essence.srt (optional)
                metadata/
                    descriptive/
                    preservation/
                        premis.xml

        Args:
            watchfolder_message: The parse watchfolder message.
        Returns:
            The path of the zipped bag and the bag information.
        """
        essence_path: Path = self.watchfolder_message.get_essence_path()
        xml_path: Path = self.watchfolder_message.get_xml_path()
        collateral_paths: list[Path] = self.watchfolder_message.get_collateral_paths()
        if not essence_path.exists() or not xml_path.exists():
            # TODO: raise error
            return

        # Relationships uuids
        ie_uuid = generate_uuid()
        rep_uuid = generate_uuid()
        file_uuid = generate_uuid()

        # Collateral uuids
        collaterals_map = {}
        for collateral in collateral_paths:
            collaterals_map[generate_uuid()] = collateral

        # Root folder for bag
        root_folder = Path(essence_path.parent, essence_path.stem)
        root_folder.mkdir(exist_ok=True)

        # /metadata
        metadata_folder = root_folder.joinpath("metadata")
        metadata_folder.mkdir(exist_ok=True)
        # /metadata/descriptive/
        metadata_desc_folder = metadata_folder.joinpath("descriptive")
        metadata_desc_folder.mkdir(exist_ok=True)
        # Write descriptive metadata
        self._write_descriptive_metadata_ie(metadata_desc_folder, xml_path, ie_uuid)

        # /metadata/preservation/
        metadata_pres_folder = metadata_folder.joinpath("preservation")
        metadata_pres_folder.mkdir(exist_ok=True)

        # Write preservation metadata on IE level
        self._write_preservation_metadata_ie(metadata_pres_folder, ie_uuid, rep_uuid)

        # /representations/representation_1/
        representations_folder = root_folder.joinpath(
            "representations", "representation_1"
        )
        representations_folder.mkdir(exist_ok=True, parents=True)

        # /representations/representation_1/data/
        representations_data_folder = representations_folder.joinpath("data")
        representations_data_folder.mkdir(exist_ok=True)
        # Copy essence
        shutil.copy(
            essence_path, representations_data_folder.joinpath(essence_path.name)
        )

        # Copy collaterals
        for collateral_path in collateral_paths:
            shutil.copy(
                collateral_path,
                representations_data_folder.joinpath(collateral_path.name),
            )

        # representations/representation_1/metadata/
        representations_metadata_folder = representations_folder.joinpath("metadata")
        representations_metadata_folder.mkdir(exist_ok=True)
        # representations/representation_1/metadata/descriptive
        representations_metadata_desc_folder = representations_metadata_folder.joinpath(
            "descriptive"
        )
        representations_metadata_desc_folder.mkdir(exist_ok=True)

        # representations/representation_1/metadata/preservation
        representations_metadata_pres_folder = representations_metadata_folder.joinpath(
            "preservation"
        )
        representations_metadata_pres_folder.mkdir(exist_ok=True)

        # Write preservation metadata on representation level
        self._write_preservation_metadata_representation(
            representations_metadata_pres_folder,
            essence_path,
            rep_uuid,
            file_uuid,
            ie_uuid,
            collaterals_map,
        )

        # Create and write representation mets.xml
        representation_mets_element = self._create_representation_mets(root_folder)
        etree.ElementTree(representation_mets_element).write(
            str(representations_folder.joinpath("mets.xml")), pretty_print=True
        )

        # Create and write package mets.xml
        package_mets_element = self._create_package_mets(root_folder)
        etree.ElementTree(package_mets_element).write(
            str(root_folder.joinpath("mets.xml")), pretty_print=True
        )

        # Bag
        # Bag info
        bag_info = {}
        if self.sidecar.batch_id:
            bag_info["Meemoo-Batch-Identifier"] = self.sidecar.batch_id
        if self.sidecar.sp_name == "TAPE":
            bag_info["Meemoo-Workflow"] = self.sidecar.sp_name

        # Make bag
        bag = bagit.make_bag(root_folder, bag_info=bag_info, checksums=["md5"])

        # Zip bag
        bag_path = root_folder.with_suffix(".bag.zip")
        with zipfile.ZipFile(bag_path, mode="w") as archive:
            for file_path in root_folder.rglob("*"):
                archive.write(file_path, arcname=file_path.relative_to(root_folder))

        # Remove root folder
        shutil.rmtree(root_folder)

        return Path(bag_path), bag
