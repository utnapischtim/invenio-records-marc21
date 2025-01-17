# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Test for record MetadataSchema."""


from dojson.contrib.marc21 import marc21
from dojson.contrib.marc21.utils import create_record

from invenio_records_marc21.services.schemas.metadata import MetadataSchema


def _test_metadata(test, expected):
    assert test.keys() == expected.keys()
    for key in test.keys():
        assert test[key] == expected[key]


def test_full_metadata_xml_schema(app, full_metadata):
    """Test metadata schema."""

    metadata = MetadataSchema()
    data = metadata.load(full_metadata)
    _test_metadata(
        data["json"],
        marc21.do(create_record(full_metadata["xml"])),
    )
    assert "xml" not in data


def test_minimal_metadata_xml_schema(app, min_metadata):
    metadata = MetadataSchema()
    data = metadata.load(min_metadata)
    _test_metadata(
        data["json"],
        marc21.do(create_record(min_metadata["xml"])),
    )
    assert "xml" not in data


def test_minimal_metadata_json_schema(app, min_json_metadata):
    metadata = MetadataSchema()
    data = metadata.load(min_json_metadata)
    assert data == min_json_metadata
    _test_metadata(
        data,
        min_json_metadata,
    )
    assert "xml" not in data
