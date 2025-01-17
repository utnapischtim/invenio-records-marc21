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

import tempfile
from datetime import timedelta

import arrow
import pytest
from invenio_app.factory import create_api
from invenio_files_rest.models import Location

from invenio_records_marc21.records import Marc21Draft, Marc21Parent


@pytest.fixture()
def embargoed_record():
    """Embargoed record."""
    embargoed_record = {
        "metadata": {"json": "test"},
        "access": {
            "files": "restricted",
            "status": "embargoed",
            "embargo": {
                "active": True,
                "until": (arrow.utcnow().datetime + timedelta(days=2)).strftime(
                    "%Y-%m-%d"
                ),
                "reason": None,
            },
        },
    }
    return embargoed_record


@pytest.fixture()
def marc21_record():
    """Normal record."""
    marc21_record = {
        "metadata": {"json": "test"},
        "access": {
            "files": "public",
            "status": "public",
            "metadata": "public",
            "embargo": {
                "active": False,
                "reason": None,
            },
        },
    }
    return marc21_record


@pytest.fixture()
def parent(app, db):
    """A parent record."""
    return Marc21Parent.create({})


@pytest.fixture()
def example_record(app, db):
    """Example record."""
    record = Marc21Draft.create({}, metadata={"title": "Test"})
    db.session.commit()
    return record


@pytest.fixture(scope="module")
def celery_config():
    """Override pytest-invenio fixture.

    TODO: Remove this fixture if you add Celery support.
    """
    return {}


@pytest.fixture(scope="module")
def app_config(app_config):
    """Application config fixture."""
    app_config[
        "RECORDS_REFRESOLVER_CLS"
    ] = "invenio_records.resolver.InvenioRefResolver"
    app_config[
        "RECORDS_REFRESOLVER_STORE"
    ] = "invenio_jsonschemas.proxies.current_refresolver_store"

    # Variable not used. We set it to silent warnings
    app_config["JSONSCHEMAS_HOST"] = "not-used"

    return app_config


@pytest.fixture(scope="module")
def app(base_app, database):
    """Application with just a database.

    Pytest-Invenio also initialises ES with the app fixture.
    """
    location_obj = Location(
        name="marctest-location", uri=tempfile.mkdtemp(), default=True
    )

    database.session.add(location_obj)
    database.session.commit()
    yield base_app


@pytest.fixture(scope="module")
def create_app(instance_path):
    """Application factory fixture."""
    return create_api
