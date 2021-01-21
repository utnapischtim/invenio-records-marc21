# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Marc21 record schemas."""

from dojson.contrib.marc21 import marc21
from dojson.contrib.marc21.utils import create_record
from marshmallow import INCLUDE, Schema, post_load


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

    @post_load
    def postload(self, data, **kwargs):
        """Convert record into json."""
        if "record" in data:
            data.update(marc21.do(create_record(data["record"])))
            del data["record"]
        return data
