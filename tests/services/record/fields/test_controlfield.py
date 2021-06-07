# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""

import pytest

from invenio_records_marc21.services.record import ControlField


def test_controlfield():
    controlfield = ControlField()
    assert controlfield.tag == ""
    assert controlfield.value == ""

    controlfield = ControlField("12")
    assert controlfield.tag == "12"
    assert controlfield.value == ""

    controlfield = ControlField(tag="123", value="laborum sunt ut nulla")
    assert controlfield.tag == "123"
    assert controlfield.value == "laborum sunt ut nulla"


def test_controlfield_to_xml():
    controlfield = ControlField(tag="123", value="laborum sunt ut nulla")
    xml = controlfield.to_xml_tag()
    assert '<controlfield tag="123">laborum sunt ut nulla' in xml
    assert '</controlfield>' in xml
    assert xml.startswith("    ")
    assert xml.endswith("\n")

    xml = controlfield.to_xml_tag(tagsep="", indent=0)
    assert '<controlfield tag="123">laborum sunt ut nulla</controlfield>' == xml
