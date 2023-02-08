#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

import pytest

from app.helpers.bag import guess_mimetype, calculate_sip_type


@pytest.mark.parametrize(
    "extension,mimetype",
    [
        (".jpg", "image/jpeg"),
        (".pdf", "application/pdf"),
        (".tiff", "image/tiff"),
        (".tif", "image/tiff"),
        (".mxf", "application/mxf"),
        (".mov", "video/quicktime"),
        (".mp4", "video/mp4"),
        (".mp3", "audio/mpeg"),
        (".wav", "audio/x-wav"),
        (".jp2", "image/jp2"),
        (".jpeg", "image/jpeg"),
        (".mp2", "audio/mpeg"),
        (".mpg", "video/mpeg"),
        (".ogg", "audio/ogg"),
        (".zip", "application/zip"),
        (".ts", "video/MP2T"),
        (".m4v", "video/mp4"),
        (".xml", "application/xml"),
        (".psb", "application/vnd.adobe.photoshop"),
        (".mpeg", "video/mpeg"),
        (".mts", "video/MP2T"),
        (".srt", "text/plain"),
        (".mkv", "video/x-matroska"),
        (".avi", "video/x-msvideo"),
    ],
)
def test_guess_mimetype(extension, mimetype):
    result = guess_mimetype(Path("/folder", f"file{extension}"))
    assert result == mimetype

    # Uppercase extension should also work
    result_upper = guess_mimetype(Path("/folder", f"file{extension.upper()}"))
    assert result_upper == mimetype


def test_guess_mimetype_other():
    result = guess_mimetype(Path("/folder", "file.unknown"))
    assert result is None


@pytest.mark.parametrize(
    "mimetype,sip_type",
    [
        ("image/jpeg", "Photographs - Digital"),
        ("image/tiff", "Photographs - Digital"),
        ("image/jp2", "Photographs - Digital"),
        ("audio/mpeg", "Audio - Media-independent (digital)"),
        ("audio/x-wav", "Audio - Media-independent (digital)"),
        ("audio/ogg", "Audio - Media-independent (digital)"),
        ("application/pdf", "Textual works - Digital"),
        ("application/zip", "Collection"),
        ("video/quicktime", "Video - File-based and Physical Media"),
        ("video/mp4", "Video - File-based and Physical Media"),
        ("video/MP2T", "Video - File-based and Physical Media"),
        ("video/mpeg", "Video - File-based and Physical Media"),
        ("application/mxf", "Video - File-based and Physical Media"),
        ("application/vnd.adobe.photoshop", "Photographs - Digital"),
        ("video/x-matroska", "Video - File-based and Physical Media"),
        ("video/x-msvideo", "Video - File-based and Physical Media"),
    ],
)
def test_calculate_sip_type(mimetype, sip_type):
    result = calculate_sip_type(mimetype)
    assert result == sip_type


def test_calculate_sip_type_other():
    result = calculate_sip_type(None)
    assert result == "OTHER"
