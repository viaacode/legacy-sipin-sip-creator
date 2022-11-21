#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

import pytest

from app.helpers.events import WatchfolderMessage, InvalidMessageException
from tests.helpers import load_resource


folder = Path("tests", "resources", "watchfolder")


def _load_resource(filename):
    return load_resource(folder.joinpath(filename))


def test_message_valid():
    event = WatchfolderMessage(_load_resource("message.json"))
    assert event.cp_name == "CPFIELD"
    assert event.flow_id == "FLOWFIELD"
    essence_file = event._get_files("essence")
    assert essence_file.file_name == "file.mxf"
    assert essence_file.file_path == "/path/to/essence/file"

    xml_file = event._get_files("sidecar")
    assert xml_file.file_name == "file.xml"
    assert xml_file.file_path == "/path/to/xml/file"


def test_message_invalid_json():
    with pytest.raises(InvalidMessageException) as e:
        WatchfolderMessage(_load_resource("message_invalid.json"))
    assert (
        str(e.value)
        == "Message is not valid JSON: 'Expecting value: line 1 column 1 (char 0)'"
    )


def test_message_missing_key():
    with pytest.raises(InvalidMessageException) as e:
        WatchfolderMessage(_load_resource("message_missing_cp_name.json"))
    assert str(e.value) == "Missing mandatory key: 'cp_name'"


def test_get_essence_path():
    event = WatchfolderMessage(_load_resource("message.json"))
    assert event.get_essence_path() == Path("/path/to/essence/file/file.mxf")


def test_get_collateral_paths():
    event = WatchfolderMessage(_load_resource("message_collaterals.json"))
    assert event.get_collateral_paths() == [
        Path("/path/to/srt/file/sub1.srt"),
        Path("/path/to/srt/file/sub2.srt"),
    ]


def test_get_xml_path():
    event = WatchfolderMessage(_load_resource("message.json"))
    assert event.get_xml_path() == Path("/path/to/xml/file/file.xml")
