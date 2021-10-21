# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Marc21 record files schemas."""

from marshmallow import Schema, fields
from marshmallow_utils.fields import SanitizedUnicode


class FileSchema(Schema):
    """File schema."""

    type = fields.String()
    checksum = fields.String()
    size = fields.Integer()
    key = SanitizedUnicode()
    version_id = SanitizedUnicode()
    bucket_id = SanitizedUnicode()
    mimetype = SanitizedUnicode()
    storage_class = SanitizedUnicode()


class FilesSchema(Schema):
    """Files metadata schema."""

    field_dump_permissions = {
        "default_preview": "read_files",
        "order": "read_files",
    }

    enabled = fields.Bool()
    default_preview = SanitizedUnicode(allow_none=True)
    order = fields.List(SanitizedUnicode())

    def get_attribute(self, obj, attr, default):
        """Override how attributes are retrieved when dumping.

        NOTE: We have to access by attribute because although we are loading
              from an external pure dict, but we are dumping from a data-layer
              object whose fields should be accessed by attributes and not
              keys. Access by key runs into FilesManager key access protection
              and raises.
        """
        value = getattr(obj, attr, default)

        if attr == "default_preview" and not value:
            return default

        return value
