# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Marc21 embargo access schemas."""

import arrow
from flask_babelex import lazy_gettext as _
from marshmallow import Schema, ValidationError, validates_schema
from marshmallow.fields import Bool
from marshmallow_utils.fields import ISODateString, SanitizedUnicode


class EmbargoSchema(Schema):
    """Schema for an embargo on the record."""

    active = Bool(allow_none=True, missing=None)
    until = ISODateString(allow_none=True, missing=None)
    reason = SanitizedUnicode(allow_none=True, missing=None)

    @validates_schema
    def validate_embargo(self, data, **kwargs):
        """Validate that the properties are consistent with each other."""
        if data.get("until") is not None:
            until_date = arrow.get(data.get("until"))
        else:
            until_date = None

        if data.get("active", False):
            if until_date is None or until_date < arrow.utcnow():
                raise ValidationError(
                    _(
                        "Embargo end date must be set to a future date "
                        "if active is True."
                    ),
                    field_name="until",
                )

        elif data.get("active", None) is not None:
            if until_date is not None and until_date > arrow.utcnow():
                raise ValidationError(
                    _(
                        "Embargo end date must be unset or in the past "
                        "if active is False."
                    ),
                    field_name="until",
                )
