# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Module tests."""

from datetime import date, timedelta

import pytest

from invenio_records_marc21.services import (
    Marc21RecordService,
    Marc21RecordServiceConfig,
)


def _assert_fields_exists(fields, data):
    for key in fields:
        assert key in data


def _assert_fields(fields, values, expected):
    for key in fields:
        assert values[key] == expected[key]


@pytest.fixture()
def marc21():
    """marc21 record."""
    return {"metadata": {"xml": "<record></record>"}}


def test_create_with_service(app, marc21, identity_simple):

    service = Marc21RecordService(config=Marc21RecordServiceConfig)

    draft = service.create(data=marc21, identity=identity_simple, access=None)

    root_fields = [
        "id",
        "versions",
        "links",
        "is_published",
        "parent",
        "revision_id",
        "created",
        "updated",
        "metadata",
    ]
    expected = {"metadata": {}}
    _assert_fields_exists(root_fields, draft.data)
    _assert_fields(["metadata"], draft.data, expected)
    assert not draft["is_published"]

    record = service.publish(id_=draft.id, identity=identity_simple)

    assert record
    _assert_fields_exists(root_fields, record.data)
    _assert_fields(["metadata"], record.data, expected)
    assert record["is_published"]


@pytest.fixture()
def empty_data():
    """marc21 record."""
    return {"metadata": {"xml": "<record></record>"}}


@pytest.mark.parametrize(
    "access",
    [
        {
            "input": {
                "metadata": "public",
            },
            "expect": {
                "access": {
                    "metadata": "public",
                    "owned_by": [{"user": 1}],
                    "files": "public",
                },
            },
        },
        {
            "input": {
                "metadata": "restricted",
            },
            "expect": {
                "access": {
                    "files": "public",
                    "owned_by": [{"user": 1}],
                    "metadata": "restricted",
                },
            },
        },
        {
            "input": {
                "metadata": "embargoed",
                "embargo": {
                    "until": (date.today() + timedelta(days=2)).strftime("%Y-%m-%d"),
                    "active": True,
                    "reason": "Because I can!",
                },
            },
            "expect": {
                "access": {
                    "files": "public",
                    "owned_by": [{"user": 1}],
                    "metadata": "embargoed",
                },
            },
        },
    ],
)
def test_create_with_access(app, empty_data, identity_simple, access):

    service = Marc21RecordService(config=Marc21RecordServiceConfig)
    draft = service.create(
        data=empty_data, identity=identity_simple, access=access["input"]
    )
    record = service.publish(id_=draft.id, identity=identity_simple)
    _assert_fields(
        ["access"],
        record.data["parent"],
        access["expect"],
    )
