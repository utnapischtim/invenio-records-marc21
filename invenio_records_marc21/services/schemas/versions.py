# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 TU Wien.
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Marc21 record schema version."""

from invenio_drafts_resources.services.records.schema import (
    VersionsSchema as VersionsSchemaBase,
)
from marshmallow_utils.permissions import FieldPermissionsMixin


class VersionsSchema(VersionsSchemaBase, FieldPermissionsMixin):
    """Version schema with field-level permissions."""

    field_load_permissions = {}

    field_dump_permissions = {
        "is_latest_draft": "edit",
    }
