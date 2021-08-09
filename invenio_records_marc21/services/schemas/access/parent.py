# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Marc21 parent record access schemas."""

from flask_babelex import lazy_gettext as _
from marshmallow import Schema, ValidationError, fields, validates_schema
from marshmallow.fields import Integer, List, Nested
from marshmallow_utils.fields import NestedAttribute, SanitizedUnicode

from ...components import AccessStatusEnum
from .embargo import EmbargoSchema


class Agent(Schema):
    """An agent schema."""

    user = Integer(required=True)


class ParentAccessSchema(Schema):
    """Access schema."""

    owned_by = List(fields.Nested(Agent))

    @validates_schema
    def validate_embargo(self, data, **kwargs):
        """Validate that the properties are consistent with each other."""
        metadata = data.get("metadata", "")
        embargo = data.get("embargo", None)
        if AccessStatusEnum.EMBARGOED.value == metadata and not embargo:
            raise ValidationError(
                _("Embargo schema must be set if metadata is Embargoed"),
                field_name="embargo",
            )
