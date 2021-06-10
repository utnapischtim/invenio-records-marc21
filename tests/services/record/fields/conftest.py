# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""

import pytest


@pytest.fixture()
def leader_kwargs():
    """Input data (as coming from the view layer)."""
    leader = {}
    leader["length"] = "00000"
    leader["status"] = "n"
    leader["type"] = "a"
    leader["level"] = "m"
    leader["control"] = " "
    leader["charset"] = "a"

    leader["ind_count"] = "2"
    leader["sub_count"] = "2"
    leader["address"] = "00000"
    leader["encoding"] = "z"
    leader["description"] = "c"
    leader["multipart_resource_record_level"] = "a"
    leader["length_field_position"] = "4"
    leader["length_starting_character_position_portion"] = "5"
    leader["length_implementation_defined_portion"] = "0"
    leader["undefined"] = "0"
    return leader
