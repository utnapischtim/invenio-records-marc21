# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Test metadata access schema."""

import pytest
from flask_babelex import lazy_gettext as _
from marshmallow import ValidationError
from marshmallow.exceptions import ValidationError

from invenio_records_marc21.services.schemas.access import AccessSchema


def _assert_raises_messages(lambda_expression, expected_messages):
    with pytest.raises(ValidationError) as e:
        lambda_expression()

    messages = e.value.normalized_messages()
    assert expected_messages == messages


def test_valid_full():
    valid_full = {
        "metadata": "public",
        "owned_by": [{"user": 1}],
        "embargo": {
            "until": "2120-10-06",
            "active": True,
            "reason": "Because I can!"
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
                _(
                    "'record' must be either 'public', 'embargoed' or 'restricted'"
                )
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
