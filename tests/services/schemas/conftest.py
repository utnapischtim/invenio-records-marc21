# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
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
def full_metadata():
    """Metadata full record marc21 xml."""
    metadata = {
        "xml": "<record><controlfield tag='001'>990079940640203331</controlfield> <controlfield tag='003'>AT-OBV</controlfield><controlfield tag='005'>20170703041800.0</controlfield><controlfield tag='007'>cr</controlfield> <controlfield tag='008'>100504|1932</controlfield><controlfield tag='009'>AC08088803</controlfield><datafield tag='035' ind1=' ' ind2=' '><subfield code='a'>AC08088803</subfield></datafield></record>"
    }
    return metadata


@pytest.fixture()
def min_metadata():
    """Metadata empty record marc21 xml."""
    metadata = {
        "xml": "<record></record>"
    }
    return metadata


@pytest.fixture()
def min_json_metadata():
    """Metadata empty record marc21 json."""
    metadata = {
        "json": {}
    }
    return metadata
