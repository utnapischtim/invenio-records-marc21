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

"""Access field for UI."""


from babel_edtf import format_edtf
from flask_babelex import gettext as _
from marshmallow import fields

from .....records.systemfields.access import AccessStatusEnum


class UIAccessSchema:
    """Access status properties to display in the UI."""

    def __init__(self, access):
        """Build access status object."""
        self.access = access
        self.access_status = AccessStatusEnum(access.get("status"))

    @property
    def id(self):
        """Access status id."""
        return self.access_status.value

    @property
    def title(self):
        """Access status title."""
        return {
            AccessStatusEnum.PUBLIC: _("Public"),
            AccessStatusEnum.EMBARGOED: _("Embargoed"),
            AccessStatusEnum.RESTRICTED: _("Restricted"),
        }.get(self.access_status)

    @property
    def icon(self):
        """Access status icon."""
        return {
            AccessStatusEnum.PUBLIC: "unlock",
            AccessStatusEnum.EMBARGOED: "outline clock",
            AccessStatusEnum.RESTRICTED: "ban",
        }.get(self.access_status)

    @property
    def embargo_date(self):
        """Embargo date."""
        until = self.access.get("embargo").get("until")
        if until:
            return format_edtf(until, format="long")
        return until

    @property
    def message_class(self):
        """UI message class name."""
        return {
            AccessStatusEnum.PUBLIC: "teal",
            AccessStatusEnum.EMBARGOED: "warning",
            AccessStatusEnum.RESTRICTED: "negative",
        }.get(self.access_status)


class AccessField(fields.Field):
    """Record access status."""

    def _serialize(self, value, attr, obj, **kwargs):
        """Serialise access status."""
        record_access_dict = obj.get("access")
        if record_access_dict:
            record_access_ui = UIAccessSchema(record_access_dict)
            return {
                "id": record_access_ui.id,
                "title": record_access_ui.title,
                "icon": record_access_ui.icon,
                "embargo_date": record_access_ui.embargo_date,
                "message_class": record_access_ui.message_class,
            }
