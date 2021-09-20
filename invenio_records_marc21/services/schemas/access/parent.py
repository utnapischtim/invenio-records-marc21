# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 record ParentAccessSchema."""

from flask_babelex import lazy_gettext as _
from marshmallow import Schema, ValidationError, fields, validates_schema
from marshmallow.fields import Integer, List

from ....records.systemfields.access import AccessStatusEnum


class Agent(Schema):
    """An agent schema."""

    user = Integer(required=True)


class ParentAccessSchema(Schema):
    """Access schema."""

    owned_by = List(fields.Nested(Agent))
