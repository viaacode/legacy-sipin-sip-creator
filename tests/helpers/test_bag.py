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
        (".psb", "image/vnd.adobe.photoshop"),
        (".mpeg", "video/mpeg"),
        (".mts", "video/MP2T"),
        (".srt", "text/plain"),
        (".mkv", "video/x-matroska"),
        (".avi", "video/x-msvideo"),
        (".dng", "image/x-adobe-dng"),
        (".flv", "video/x-flv"),
        (".wmv", "video/x-ms-wmv"),
        (".dv", "video/x-dv"),
        (".f4v", "video/mp4"),
        (".png", "image/png"),
        (".m4a", "audio/mp4"),
        (".vob", "video/dvd"),
        (".m2v", "video/mpeg"),
        (".aif", "audio/aiff"),
        (".wma", "audio/x-ms-wma"),
        (".ac3", "audio/ac3"),
        (".psd", "image/vnd.adobe.photoshop"),
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
        ("image/vnd.adobe.photoshop", "Photographs - Digital"),
        ("video/x-matroska", "Video - File-based and Physical Media"),
        ("video/x-msvideo", "Video - File-based and Physical Media"),
        ("image/x-adobe-dng", "Photographs - Digital"),
        ("video/x-flv", "Video - File-based and Physical Media"),
        ("video/x-ms-wmv", "Video - File-based and Physical Media"),
        ("video/x-dv", "Video - File-based and Physical Media"),
        ("image/png", "Other Graphic Images - Digital"),
        ("audio/mp4", "Audio - Media-independent (digital)"),
        ("video/dvd", "Video - File-based and Physical Media"),
        ("audio/aiff", "Audio - Media-independent (digital)"),
        ("audio/x-ms-wma", "Audio - Media-independent (digital)"),
        ("audio/ac3", "Audio - Media-independent (digital)"),
    ],
)
def test_calculate_sip_type(mimetype, sip_type):
    result = calculate_sip_type(mimetype)
    assert result == sip_type


def test_calculate_sip_type_other():
    result = calculate_sip_type(None)
    assert result == "OTHER"
