# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Marc21 record schemas."""

import arrow
from flask_babelex import lazy_gettext as _
from marshmallow import Schema, ValidationError, validates, validates_schema
from marshmallow.fields import Integer, List, Nested
from marshmallow_utils.fields import NestedAttribute, SanitizedUnicode

from ...components import AccessStatusEnum
from .embargo import EmbargoSchema


class Agent(Schema):
    """An agent schema."""

    user = Integer(required=True)


class AccessSchema(Schema):
    """Access schema."""

    metadata = SanitizedUnicode(required=True)
    files = SanitizedUnicode(required=True)
    embargo = NestedAttribute(EmbargoSchema)
    status = SanitizedUnicode(dump_only=False)
    owned_by = List(Nested(Agent))

    def validate_protection_value(self, value, field_name):
        """Check that the protection value is valid."""
        if value not in AccessStatusEnum.list():
            raise ValidationError(
                _("'{}' must be either '{}', '{}' or '{}'").format(
                    field_name,
                    *AccessStatusEnum.list(),
                ),
                "record",
            )

    def get_attribute(self, obj, key, default):
        """Override from where we get attributes when serializing."""
        if key in ["metadata", "files"]:
            return getattr(obj.protection, key, default)
        elif key == "status":
            return obj.status.value
        return getattr(obj, key, default)

    @validates("metadata")
    def validate_metadata_protection(self, value):
        """Validate the metadata protection value."""
        self.validate_protection_value(value, "metadata")

    @validates_schema
    def validate_embargo(self, data, **kwargs):
        """Validate that the properties are consistent with each other."""
        metadata = data.get("metadata", "")
        embargo = data.get("embargo", "")
        if AccessStatusEnum.EMBARGOED.value == metadata and not embargo:
            raise ValidationError(
                _("Embargo must be set if metadata is Embargoed"),
                field_name="embargo",
            )

    @validates("files")
    def validate_files_protection(self, value):
        """Validate the files protection value."""
        self.validate_protection_value(value, "files")
