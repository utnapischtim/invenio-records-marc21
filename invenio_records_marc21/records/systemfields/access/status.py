# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Marc21 access status."""

from enum import Enum


class AccessStatusEnum(Enum):
    """Enum defining access statuses."""

    PUBLIC = "public"

    EMBARGOED = "embargoed"

    RESTRICTED = "restricted"

    @staticmethod
    def list():
        """List all access statuses."""
        return list(map(lambda c: c.value, AccessStatusEnum))
