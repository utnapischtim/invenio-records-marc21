# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Module cli tests."""


from datetime import timedelta

import arrow

from invenio_records_marc21.cli import (
    create_fake_metadata,
    create_fake_record,
    fake_access_right,
    fake_feature_date,
    marc21,
    system_identity,
)
from invenio_records_marc21.records.systemfields.access import AccessStatusEnum


def test_system_identity():
    """Test r identity for demo."""
    identity = system_identity()
    assert identity.id == 1
    assert identity.provides


def test_fake_access_right():
    """Test random access right for demo."""
    access = fake_access_right()
    assert access in AccessStatusEnum.list()


def test_fake_feature_date():
    """Test create future date for demo."""
    assert isinstance(fake_feature_date(), str)
    date = fake_feature_date(days=30)
    start_date = arrow.utcnow().datetime
    assert isinstance(date, str)
    date_arrow = arrow.get(date)
    assert date_arrow >= arrow.get(start_date.date() + timedelta(days=1))
    assert date_arrow < arrow.get(start_date.date() + timedelta(days=30))


def test_fake_demo_record_creation(app):
    """Test create fake full record with marc21 service."""
    with app.app_context():
        record = create_fake_record("../tests/test-record.json")
        assert record
        assert record.id


def test_fake_demo_metadata_creation(app):
    """Test create fake metadata record with marc21 service."""
    with app.app_context():
        record = create_fake_metadata("../tests/test-metadata.xml")
        assert record
        assert record.id


def test_cli_create_demo_record(app):
    """Test cli marc21 demo record."""
    runner = app.test_cli_runner()
    result = runner.invoke(
        marc21,
        [
            "demo",
            "-f",
            "../tests/test-record.json",
            "-m",
            "False",
            "-n",
            "10",
        ],
    )
    assert result.exit_code == 0
    assert result.output == "Creating demo records...\nCreated records!\n"


def test_cli_create_demo_metadata(app):
    """Test cli marc21 demo metadata."""
    runner = app.test_cli_runner()
    result = runner.invoke(
        marc21,
        [
            "demo",
            "-f",
            "../tests/test-metadata.xml",
            "-m",
            "True",
            "-n",
            "10",
        ],
    )
    assert result.exit_code == 0
    assert result.output == "Creating demo records...\nCreated records!\n"
