#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

import pytest

from app.helpers.sidecar import Sidecar


def test_sidecar():
    sidecar = Sidecar(Path("tests", "resources", "sidecar", "sidecar.xml"))
    assert not sidecar.md5
    assert sidecar.cp_id == "CP ID"
    assert sidecar.is_xdcam() is False


def test_sidecar_md5():
    sidecar = Sidecar(Path("tests", "resources", "sidecar", "sidecar_md5.xml"))
    assert sidecar.md5 == "7e0ef8c24fe343d98fbb93b6a7db6ccb"


@pytest.mark.parametrize(
    "input_file,bestandsnaam",
    [
        ("sidecar_bestandsnaam_source.xml", "bestandsnaam"),
        ("sidecar_source.xml", "source"),
        ("sidecar_bestandsnaam.xml", "bestandsnaam"),
        ("sidecar_bestandsnamen_source.xml", "Bestandsnaam"),
        ("sidecar.xml", None),
    ],
)
def test_sidecar_calculate_original_filename(input_file, bestandsnaam):
    sidecar = Sidecar(Path("tests", "resources", "sidecar", input_file))
    assert sidecar.calculate_original_filename() == bestandsnaam


def test_sidecar_xdcam():
    sidecar = Sidecar(Path("tests", "resources", "sidecar", "sidecar_xdcam.xml"))
    assert sidecar.format == "XDCAM"
    assert sidecar.digitization_date == "2022-05-24"
    assert sidecar.digitization_time == "14:15:50"
    assert sidecar.player_manufacturer == "SONY"
    assert sidecar.player_model == "PDW-U4"
    assert sidecar.player_serial_number == "0000000"
    assert sidecar.sp_id == "SP ID"
    assert sidecar.sp_name == "SP Name"
    assert sidecar.type_viaa == "Video"
    assert sidecar.is_xdcam() is True


def test_sidecar_batch_id():
    sidecar = Sidecar(Path("tests", "resources", "sidecar", "sidecar_batch_id.xml"))
    assert sidecar.batch_id == "Batch ID"
