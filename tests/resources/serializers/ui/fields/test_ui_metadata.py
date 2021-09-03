# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Test for record ui MetadataSchema."""

from copy import deepcopy

from dojson.contrib.marc21 import marc21
from dojson.contrib.marc21.utils import create_record
from dojson.contrib.to_marc21 import to_marc21
from dojson.contrib.to_marc21.utils import dumps

from invenio_records_marc21.resources.serializers.errors import Marc21XMLConvertError
from invenio_records_marc21.resources.serializers.fields import MetadataSchema


def _test_metadata(test, expected, exept=["__order__"]):
    # assert test.keys() == expected.keys()
    for key in test.keys():
        if key not in exept:
            assert test[key] == expected[key]


def _test_without_order(data, key="__order__"):
    """Test no Key with the name in dict."""
    if isinstance(data, dict):
        for k, v in data.items():
            assert not key == k
            _test_without_order(v, key)
    elif isinstance(data, (list, tuple)):
        for item in data:
            _test_without_order(item, key)


def test_ui_metadata_remove_order(marc21_metadata):
    metadata = MetadataSchema(context={"remove_order": True})
    data = metadata.dump(marc21_metadata)
    _test_without_order(data)


def test_ui_metadata_convert_xml(marc21_metadata):
    metadata = MetadataSchema(context={"marcxml": True})
    test = deepcopy(marc21_metadata)

    data = metadata.dump(test)
    assert "xml" in data
    assert "json" not in data
    assert isinstance(data["xml"], str)

    expect_str = dumps(to_marc21.do(marc21_metadata["json"])).decode("UTF-8")
    assert expect_str == data["xml"]


def test_ui_metadata_default_schema(marc21_metadata):
    metadata = MetadataSchema()
    data = metadata.dump(marc21_metadata)
    assert data == marc21_metadata
    _test_metadata(
        data["json"],
        marc21_metadata["json"],
    )
    assert "xml" not in data


def test_ui_metadata_xml_schema(marc21_metadata):
    """Test metadata schema."""

    metadata = MetadataSchema(
        context={
            "marcxml": True,
        }
    )
    test = deepcopy(marc21_metadata)
    data = metadata.dump(test)
    assert "json" not in data
    assert "xml" in data

    s = "".join(data["xml"].split("\n")[1:-1])
    test = marc21.do(create_record(s))
    _test_without_order(
        test,
        marc21_metadata["json"],
    )


def test_ui_metadata_json_schema(marc21_metadata):
    metadata = MetadataSchema(
        context={
            "marcxml": False,
        }
    )
    test = deepcopy(marc21_metadata)
    data = metadata.dump(test)
    assert "xml" not in data
    assert "json" in data
    _test_metadata(
        data["json"],
        marc21_metadata["json"],
    )
