# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Marc21 record schemas."""

import time
from urllib import parse

import arrow
import idutils
from dojson.contrib.marc21 import marc21
from dojson.contrib.marc21.utils import create_record
from edtf.parser.grammar import level0Expression
from flask import current_app
from flask_babelex import lazy_gettext as _
from marshmallow import (
    EXCLUDE,
    INCLUDE,
    Schema,
    ValidationError,
    fields,
    post_load,
    validate,
    validates,
    validates_schema,
)
from marshmallow_utils.fields import (
    EDTFDateString,
    GenFunction,
    ISODateString,
    ISOLangString,
    SanitizedUnicode,
)
from marshmallow_utils.schemas import GeometryObjectSchema

from .utils import validate_entry


def _no_duplicates(value_list):
    str_list = [str(value) for value in value_list]
    return len(value_list) == len(set(str_list))


class MetadataSchema(Schema):
    """Schema for the record metadata."""

    field_load_permissions = {
        # TODO: define "can_admin" action
    }

    field_dump_permissions = {
        # TODO: define "can_admin" action
    }

    class Meta:
        """Meta class to accept unknwon fields."""

        unknown = INCLUDE

    # TODO convert after load from marc21 to json the record item

    @post_load
    def postload(self, data, **kwargs):
        """ Convert record into json"""
        if "record" in data:
            data["record"] = marc21.do(create_record(data["record"]))
        return data
