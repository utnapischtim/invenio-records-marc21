# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Access module."""

from .embargo import Embargo
from .fields import (
    ParentRecordAccess,
    ParentRecordAccessField,
    RecordAccess,
    RecordAccessField,
)
from .owners import Owner, Owners
from .protection import Protection
from .status import AccessStatusEnum

__all__ = (
    "AccessStatusEnum",
    "Embargo",
    "ParentRecordAccessField",
    "ParentRecordAccess",
    "RecordAccessField",
    "RecordAccess",
    "Owner",
    "Owners",
    "Protection",
)
