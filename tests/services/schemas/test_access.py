# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Test record AccessSchema."""


from datetime import timedelta

import arrow
import pytest
from flask_babelex import lazy_gettext as _
from marshmallow import ValidationError
from marshmallow.exceptions import ValidationError

from invenio_records_marc21.services.schemas.access import AccessSchema, EmbargoSchema


def _assert_raises_messages(lambda_expression, expected_messages):
    with pytest.raises(ValidationError) as e:
        lambda_expression()

    messages = e.value.normalized_messages()
    assert expected_messages == messages


def test_valid_full():
    valid_full = {
        "metadata": "embargoed",
        "owned_by": [{"user": 1}],
        "embargo": {
            "until": (arrow.utcnow().datetime + timedelta(days=2)).strftime("%Y-%m-%d"),
            "active": True,
            "reason": "Because I can!",
        },
        "files": "public",
    }
    assert valid_full == AccessSchema().load(valid_full)


def test_invalid_access_right():
    invalid_access_right = {
        "files": "public",
        "owned_by": [{"user": 1}],
        "metadata": "invalid value",
    }

    _assert_raises_messages(
        lambda: AccessSchema().load(invalid_access_right),
        {
            "metadata": [
                _("'metadata' must be either 'public', 'embargoed' or 'restricted'")
            ]
        },
    )


@pytest.mark.parametrize(
    "invalid_access,missing_attr",
    [
        (
            {
                "metadata": "public",
                "files": "public",
                "owned_by": [1],
            },
            "owned_by",
        ),
        (
            {"metadata": "public", "owned_by": [{"user": 1}]},
            "files",
        ),
        (
            {"owned_by": [{"user": 1}], "files": "public"},
            "metadata",
        ),
    ],
)
def test_invalid(invalid_access, missing_attr):

    with pytest.raises(ValidationError) as e:
        AccessSchema().load(invalid_access)

    error_fields = e.value.messages.keys()
    assert len(error_fields) == 1
    assert missing_attr in error_fields


def test_embargo_load_no_until_is_valid():
    expected = {"active": False, "until": None, "reason": None}

    valid_no_until = {
        "active": False,
    }
    assert expected == EmbargoSchema().load(valid_no_until)

    valid_no_until = {
        "active": False,
        "until": None,
    }
    assert expected == EmbargoSchema().load(valid_no_until)


def test_embargo_dump_no_until_is_valid():
    valid_no_until = {
        "active": False,
    }
    assert valid_no_until == EmbargoSchema().dump(valid_no_until)

    expected = {
        "active": False,
    }
    valid_no_until = {
        "active": False,
        "until": None,
    }
    assert expected == EmbargoSchema().dump(valid_no_until)


@pytest.mark.parametrize(
    "invalid_access,invalid_attr",
    [
        (
            {
                "files": "restricted",
                "embargo": {
                    "active": True,
                    "until": (arrow.utcnow().datetime + timedelta(days=2)).strftime("%Y-%m-%d"),
                    "reason": "Because I can!",
                },
            },
            "metadata",
        ),
        (
            {
                "metadata": "public",
                "embargo": {
                    "active": True,
                    "until": (arrow.utcnow().datetime + timedelta(days=2)).strftime("%Y-%m-%d"),
                    "reason": "Because I can!",
                },
            },
            "files",
        ),
        (
            {
                "metadata": "public",
                "files": "restricted",
                "embargo": {
                    "active": False,
                    "until": (arrow.utcnow().datetime + timedelta(days=2)).strftime("%Y-%m-%d"),
                    "reason": "Because I can!",
                },
            },
            "embargo",
        ),
        (
            {
                "metadata": "public",
                "files": "restricted",
                "embargo": {
                    "active": True,
                    "until": (arrow.utcnow().datetime + timedelta(days=-20)).strftime("%Y-%m-%d"),
                    "reason": "Because I can!",
                },
            },
            "embargo",
        ),
        (
            {
                "metadata": "invalid",
                "files": "restricted",
                "embargo": {
                    "active": False,
                    "until": (arrow.utcnow().datetime + timedelta(days=-20)).strftime("%Y-%m-%d"),
                    "reason": "Because I can!",
                },
            },
            "metadata",
        ),
        (
            {
                "metadata": "public",
                "files": "invalid",
                "embargo": {
                    "active": False,
                    "until": (arrow.utcnow().datetime + timedelta(days=-20)).strftime("%Y-%m-%d"),
                    "reason": "Because I can!",
                },
            },
            "files",
        ),
    ],
)
def test_invalid(invalid_access, invalid_attr):

    with pytest.raises(ValidationError) as e:
        AccessSchema().load(invalid_access)

    error_fields = e.value.messages.keys()
    assert len(error_fields) == 1
    assert invalid_attr in error_fields
