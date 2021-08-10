# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""System access fields module."""

from .parent import ParentRecordAccess, ParentRecordAccessField
from .record import RecordAccess, RecordAccessField

__all__ = (
    "ParentRecordAccessField",
    "ParentRecordAccess",
    "RecordAccessField",
    "RecordAccess",
)
