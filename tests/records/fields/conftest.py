# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""

import tempfile

import pytest
from flask import Flask
from flask_security.utils import hash_password
from invenio_accounts import InvenioAccounts
from invenio_db import InvenioDB
from invenio_files_rest import InvenioFilesREST
from invenio_files_rest.models import Location
from invenio_jsonschemas import InvenioJSONSchemas
from invenio_records import InvenioRecords

from invenio_records_marc21 import InvenioRecordsMARC21
from invenio_records_marc21.records import Marc21Parent


@pytest.fixture(scope="module")
def create_app(instance_path):
    """Application factory fixture for use with pytest-invenio."""

    def _create_app(**config):
        app_ = Flask(
            __name__,
            instance_path=instance_path,
        )
        app_.config.update(config)
        InvenioDB(app_)
        InvenioFilesREST(app_)
        InvenioRecordsMARC21(app_)
        return app_

    return _create_app


@pytest.fixture(scope="module")
def testapp(base_app, database):
    """Application with just a database.

    Pytest-Invenio also initialises ES with the app fixture.
    """
    location_obj = Location(
        name="marctest-location", uri=tempfile.mkdtemp(), default=True
    )

    database.session.add(location_obj)
    database.session.commit()
    InvenioRecords(base_app)
    InvenioJSONSchemas(base_app)
    yield base_app


@pytest.fixture(scope="module")
def appaccess(base_app, database):
    """Create App  systemfields."""
    InvenioRecords(base_app)
    InvenioJSONSchemas(base_app)
    yield base_app


@pytest.fixture()
def parent(app, db):
    """A parent record."""
    return Marc21Parent.create({})
