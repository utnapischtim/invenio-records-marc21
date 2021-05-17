# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Marc21 AccessComponent."""

from enum import Enum

from invenio_records_resources.services.records.components import ServiceComponent


class AccessStatusEnum(Enum):
    """Enum defining access statuses."""

    PUBLIC = "public"

    EMBARGOED = "embargoed"

    RESTRICTED = "restricted"

    # METADATA_ONLY = "metadata-only"

    @staticmethod
    def list():
        return list(map(lambda c: c.value, AccessStatusEnum))


class AccessComponent(ServiceComponent):
    """Service component for access integration."""

    def _default_access(self, identity, data, record, **kwargs):
        """Create default access component if not pressent in the record."""
        default_access = {
            "access": {
                "owned_by": [{"user": identity.id}],
                "metadata": AccessStatusEnum.PUBLIC.value,
                "files": AccessStatusEnum.PUBLIC.value,
            },
        }
        if record is not None and "access" in data:
            record.parent.update({"access": data.get("access")})
            record.parent.commit()
        elif "access" not in data:
            data.update(default_access)
            record.parent.update({"access": data.get("access")})
            record.parent.commit()

    def _init_owned_by(self, identity, record, **kwargs):
        """Initialize the owned by atribute in access component."""
        access_data = record.parent.get("access", {})
        if not "owned_by" in access_data and identity.id:
            access_data.setdefault("owned_by", [{"user": identity.id}])
            record.parent.update(access_data)

    def create(self, identity, data=None, record=None, **kwargs):
        """Add basic ownership fields to the record."""
        self._default_access(identity, data, record, **kwargs)
        self._init_owned_by(identity, record, **kwargs)

    def update_draft(self, identity, data=None, record=None, **kwargs):
        """Update draft handler."""
        self._default_access(identity, data, record, **kwargs)

    def update(self, identity, data=None, record=None, **kwargs):
        """Update handler."""
        self._init_owned_by(identity, record, **kwargs)
