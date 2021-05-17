# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Marc21 parent record schemas."""

from invenio_drafts_resources.services.records.schema import ParentSchema
from marshmallow import fields

from .access import ParentAccessSchema


class Marc21ParentSchema(ParentSchema):
    """Record schema."""

    access = fields.Nested(ParentAccessSchema)


__all__ = ("Marc21ParentSchema",)
