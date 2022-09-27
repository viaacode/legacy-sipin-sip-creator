#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

import pytest
from app.helpers.dc import DC
from tests.helpers import load_resource

from lxml import etree


@pytest.mark.parametrize(
    "input_file,output_file",
    [
        ("metadata_deelarchief.xml", "dc_deelarchief.xml"),
        ("metadata_archief.xml", "dc_archief.xml"),
        ("metadata_seizoen.xml", "dc_seizoen.xml"),
        ("metadata_seizoennummer.xml", "dc_seizoennummer.xml"),
        ("metadata_serienummer.xml", "dc_serienummer.xml"),
        ("metadata_deelreeks.xml", "dc_deelreeks.xml"),
        ("metadata_deelreeks_serienummer.xml", "dc_deelreeks_serienummer.xml"),
        ("metadata_reeks.xml", "dc_reeks.xml"),
        ("metadata_reeks_serienummer.xml", "dc_reeks_serienummer.xml"),
        ("metadata_reeks_deelreeks.xml", "dc_reeks_deelreeks.xml"),
        ("metadata_serie.xml", "dc_serie.xml"),
        ("metadata_serie_serienummer.xml", "dc_serie_serienummer.xml"),
        ("metadata_serie_deelreeks.xml", "dc_serie_deelreeks.xml"),
        ("metadata_programma.xml", "dc_programma.xml"),
        (
            "metadata_programmabeschrijving.xml",
            "dc_programmabeschrijving.xml",
        ),
        ("metadata_bestandsnamen.xml", "dc_bestandsnamen.xml"),
        ("metadata_dc_Subjects.xml", "dc_dc_Subjects.xml"),
        ("metadata_description_short.xml", "dc_description_short.xml"),
        ("metadata_titles_empty_title.xml", "dc_titles_empty_title.xml"),
        ("metadata_all_empty_titles.xml", "dc_all_empty_titles.xml"),
        ("metadata_dc_subjects_trefwoord.xml", "dc_dc_subjects_trefwoord.xml"),
        ("metadata_dc_creators_auteur.xml", "dc_dc_creators_auteur.xml"),
        (
            "metadata_dc_rights_rightsOwners_auteursrechthouder.xml",
            "dc_dc_rights_rightsOwners_auteursrechthouder.xml",
        ),
        ("metadata_dc_publishers_publisher.xml", "dc_dc_publishers_publisher.xml"),
    ],
)
def test_transform(input_file, output_file):
    # Arrange
    medadata_path = Path("tests", "resources", "dc", input_file)
    # Act
    terms_element = DC.transform(medadata_path)
    # Assert
    terms_xml = etree.tostring(terms_element, pretty_print=True).strip()
    xml = load_resource(Path("tests", "resources", "dc", output_file))
    assert terms_xml == xml


def test_transform_uuid():
    # Arrange
    medadata_path = Path("tests", "resources", "dc", "metadata.xml")
    # Act
    terms_element = DC.transform(
        medadata_path,
        ie_uuid=etree.XSLT.strparam("uuid-865b767d-05f9-49d5-ba54-e9e82acec30d"),
    )
    # Assert
    terms_xml = etree.tostring(terms_element, pretty_print=True).strip()
    xml = load_resource(Path("tests", "resources", "dc", "dc.xml"))
    assert terms_xml == xml
