# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Marc21 parent record schemas."""

from .embargo import EmbargoSchema
from .parent import ParentAccessSchema
from .record import AccessSchema

__all__ = (
    "ParentAccessSchema",
    "AccessSchema",
    "EmbargoSchema",
)
