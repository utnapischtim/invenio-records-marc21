# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Tests for record MetadataSchema."""

import pytest

from invenio_records_marc21.services.record import Marc21Metadata
from invenio_records_marc21.services.record.fields import (
    ControlField,
    DataField,
    LeaderField,
    SubField,
)


def test_create_metadata():

    metadata = Marc21Metadata()
    assert metadata.leader.to_xml_tag() == LeaderField().to_xml_tag()
    assert metadata.controlfields == list()
    assert metadata.datafields == list()

    assert "<?xml version='1.0' ?>" in metadata.xml
    assert '<record xmlns="http://www.loc.gov/MARC21/slim"' in metadata.xml
    assert (
        'xsi:schemaLocation="http://www.loc.gov/MARC21/slim schema.xsd" type="Bibliographic"'
        in metadata.xml
    )
    assert 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"' in metadata.xml

    metadata.emplace_field(
        tag="245", ind1="1", ind2="0", code="a", value="laborum sunt ut nulla"
    )

    assert '<datafield tag="245" ind1="1" ind2="0">' in metadata.xml
    assert '<subfield code="a">laborum sunt ut nulla</subfield>' in metadata.xml


def test_validate_metadata():
    metadata = Marc21Metadata()
    metadata.emplace_field(
        tag="245", ind1="1", ind2="0", code="a", value="laborum sunt ut nulla"
    )
    assert metadata.is_valid_marc21_xml_string()

    metadata.emplace_field(
        tag="245", ind1="1", ind2="0", code="", value="laborum sunt ut nulla"
    )

    assert not metadata.is_valid_marc21_xml_string()


def test_subfield_metadata():
    metadata = Marc21Metadata()
    metadata.emplace_field(
        tag="245", ind1="1", ind2="0", code="a", value="laborum sunt ut nulla"
    )

    metadata.emplace_field(
        tag="245", ind1="1", ind2="0", code="b", value="laborum sunt ut nulla"
    )

    assert metadata.is_valid_marc21_xml_string()


def test_controlfields_metadata():
    metadata = Marc21Metadata()
    controlfield = ControlField(tag="123", value="laborum sunt ut nulla")

    assert len(metadata.datafields) == 0
    assert len(metadata.controlfields) == 0

    metadata.controlfields.append(controlfield)
    assert len(metadata.datafields) == 0
    assert len(metadata.controlfields) == 1
    assert '<controlfield tag="123">laborum sunt ut nulla' in metadata.xml


def test_uniqueness_metadata():
    metadata = Marc21Metadata()
    metadata.emplace_unique_field(
        tag="245", ind1="1", ind2="0", code="a", value="laborum sunt ut nulla"
    )

    metadata.emplace_unique_field(
        tag="245", ind1="1", ind2="0", code="a", value="laborum sunt ut nulla"
    )

    assert len(metadata.datafields) == 1
    assert len(metadata.controlfields) == 0
    assert len(metadata.datafields[0].subfields) == 1
    assert metadata.is_valid_marc21_xml_string()


def test_xml_type():
    metadata = Marc21Metadata()

    test = '<datafield tag="245" ind1="0" ind2="0"></datafield>'
    metadata.xml = test
    assert metadata.xml

    test = {}
    with pytest.raises(TypeError):
        metadata.xml = test


def test_json_type():
    metadata = Marc21Metadata()

    test = dict()
    metadata.json = test
    assert metadata.json == {}

    test = ""
    with pytest.raises(TypeError):
        metadata.json = test


def test_xml_metadata():
    metadata = Marc21Metadata()
    test = DataField(tag="245", ind1="0", ind2="0")

    metadata.xml = test.to_xml_tag()

    assert metadata.leader.to_xml_tag() == LeaderField().to_xml_tag()
    assert len(metadata.datafields) == 1
    assert len(metadata.controlfields) == 0
    assert len(metadata.datafields[0].subfields) == 0
    assert test.to_xml_tag() in metadata.xml

    test.subfields.append(SubField(code="a", value="Brain-Computer Interface"))
    metadata = Marc21Metadata()
    metadata.xml = test.to_xml_tag()

    assert len(metadata.datafields) == 1
    assert len(metadata.controlfields) == 0
    assert len(metadata.datafields[0].subfields) == 1
    assert test.to_xml_tag() in metadata.xml

    test.subfields.append(SubField(code="b", value="Subtitle field."))
    metadata = Marc21Metadata()
    metadata.xml = test.to_xml_tag()

    assert len(metadata.datafields) == 1
    assert len(metadata.controlfields) == 0
    assert len(metadata.datafields[0].subfields) == 2
    assert test.to_xml_tag() in metadata.xml

    test.subfields.append(SubField(code="c", value="hrsg. von Josef Frank"))
    metadata = Marc21Metadata()
    metadata.xml = test.to_xml_tag()

    assert len(metadata.datafields) == 1
    assert len(metadata.controlfields) == 0
    assert len(metadata.datafields[0].subfields) == 3
    assert test.to_xml_tag() in metadata.xml
