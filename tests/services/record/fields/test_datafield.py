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

from invenio_records_marc21.services.record import DataField, SubField


def test_datafield():
    datafield = DataField()
    assert datafield.tag == ""
    assert datafield.ind1 == " "
    assert datafield.ind2 == " "
    assert datafield.subfields == list()

    datafield = DataField("laborum", "a", "b")
    assert datafield.tag == "laborum"
    assert datafield.ind1 == "a"
    assert datafield.ind2 == "b"

    subfield = SubField(code="123", value="laborum sunt ut nulla")
    datafield.subfields.append(subfield)
    assert len(datafield.subfields) == 1


def test_datafield_to_xml():
    subfield = SubField(code="123", value="laborum sunt ut nulla")
    datafield = DataField("laborum")
    datafield.subfields.append(subfield)

    xml = datafield.to_xml_tag()
    assert '<datafield tag="laborum" ind1=" " ind2=" ">\n' in xml
    assert '<subfield code="123">laborum sunt ut nulla</subfield>' in xml
    assert xml.startswith("    ")
    assert xml.endswith("\n")

    xml = datafield.to_xml_tag(tagsep="", indent=0)
    assert xml.startswith(
        '<datafield tag="laborum" ind1=" " ind2=" "><subfield code="123">laborum sunt ut nulla</subfield>'
    )
