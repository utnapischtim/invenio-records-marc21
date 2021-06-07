# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Marc21 record schemas."""

from invenio_drafts_resources.services.records.schema import ParentSchema
from invenio_records_resources.services.records.schema import BaseRecordSchema
from marshmallow import EXCLUDE, INCLUDE, Schema, fields, missing, post_dump
from marshmallow_utils.fields import NestedAttribute

from .access import AccessSchema, ParentAccessSchema
from .files import FilesSchema
from .metadata import MetadataSchema
from .pids import PIDSchema
from .versions import VersionsSchema


class Marc21ParentSchema(ParentSchema):
    """Record schema."""

    access = fields.Nested(ParentAccessSchema)


class Marc21RecordSchema(BaseRecordSchema):
    """Record schema."""

    id = fields.Str()
    # pid
    pids = fields.List(NestedAttribute(PIDSchema))

    parent = NestedAttribute(Marc21ParentSchema, dump_only=True)

    metadata = NestedAttribute(MetadataSchema)
    access = NestedAttribute(AccessSchema)
    files = NestedAttribute(FilesSchema, dump_only=True)

    created = fields.Str(dump_only=True)
    updated = fields.Str(dump_only=True)
    revision = fields.Integer(dump_only=True)

    versions = NestedAttribute(VersionsSchema, dump_only=True)

    is_published = fields.Boolean(dump_only=True)

    # Add version to record schema
    # versions = NestedAttribute(VersionsSchema, dump_only=True)

    @post_dump
    def default_nested(self, data, many, **kwargs):
        """Serialize metadata as empty dict for partial drafts.

        Cannot use marshmallow for Nested fields due to issue:
        https://github.com/marshmallow-code/marshmallow/issues/1566
        https://github.com/marshmallow-code/marshmallow/issues/41
        and more.
        """
        if not data.get("metadata"):
            data["metadata"] = {}

        return data


__all__ = (
    "Marc21RecordSchema",
    "Marc21ParentSchema",
)
