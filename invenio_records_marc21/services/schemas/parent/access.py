# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Marc21 parent record access schemas."""

from flask_babelex import lazy_gettext as _
from marshmallow import Schema, fields
from marshmallow_utils.fields import SanitizedUnicode


class Agent(Schema):
    """An agent schema."""

    user = fields.Integer(required=True)


class ParentAccessSchema(Schema):
    """Access schema."""

    metadata = SanitizedUnicode(required=True)
    files = SanitizedUnicode(required=True)
    status = SanitizedUnicode(dump_only=False)
    owned_by = fields.List(fields.Nested(Agent))
