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

from invenio_records_marc21.services.record import SubField


def test_subfield():
    subfield = SubField()
    assert subfield.code == ""
    assert subfield.value == ""

    subfield = SubField("12")
    assert subfield.code == "12"
    assert subfield.value == ""

    subfield = SubField(code="123", value="laborum sunt ut nulla")
    assert subfield.code == "123"
    assert subfield.value == "laborum sunt ut nulla"


def test_subfield_to_xml():
    subfield = SubField(code="123", value="laborum sunt ut nulla")
    xml = subfield.to_xml_tag()
    assert '<subfield code="123">laborum sunt ut nulla</subfield>' in xml
    assert xml.startswith("        ")
    assert xml.endswith("\n")

    xml = subfield.to_xml_tag(tagsep="", indent=0)
    assert '<subfield code="123">laborum sunt ut nulla</subfield>' == xml
