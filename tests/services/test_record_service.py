# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Service tests.

Test to add:
- Read a tombstone page
- Read with missing permissions
- Read with missing pid
"""

import time
from collections import namedtuple

import pytest
from dojson.contrib.marc21.utils import create_record
from dojson.contrib.to_marc21 import to_marc21
from invenio_pidstore.errors import PIDDoesNotExistError
from invenio_pidstore.models import PIDStatus
from sqlalchemy.orm.exc import NoResultFound

RunningApp = namedtuple("RunningApp", ["app", "service", "identity_simple"])


@pytest.fixture()
def running_app(app, service, identity_simple):
    """This fixture provides an app with the typically needed db data loaded.

    All of these fixtures are often needed together, so collecting them
    under a semantic umbrella makes sense.
    """
    return RunningApp(app, service, identity_simple)


#
# Operations tests
#

def test_create_draft(running_app, metadata):
    """Test draft creation of a non-existing record."""

    service = running_app.service
    draft = service.create(running_app.identity_simple, metadata=metadata)
    draft_dict = draft.to_dict()

    assert draft.id

    # files attribute in record causes at create change the revision_id twice
    assert draft._record.revision_id == 3

    # Check for pid and parent pid
    assert draft["id"]
    assert draft._record.pid.status == PIDStatus.NEW


def test_create_empty_draft(running_app):
    """Test an empty draft can be created.

    Errors (missing required fields) are reported, but don't prevent creation.
    """
    input_data = {"metadata": {}}
    service = running_app.service
    identity_simple = running_app.identity_simple

    draft = service.create(identity_simple, input_data)
    draft_dict = draft.to_dict()

    assert draft["id"]
    assert draft._record.pid.status == PIDStatus.NEW


def test_read_draft(running_app, metadata):
    """Test read a draft can be created."""

    service = running_app.service
    identity_simple = running_app.identity_simple
    draft = service.create(identity_simple, metadata=metadata)
    assert draft.id

    draft_2 = service.read_draft(draft.id, identity_simple)
    assert draft.id == draft_2.id


def test_delete_draft(running_app, metadata):
    """Test a created  draft can be deleted."""
    identity_simple = running_app.identity_simple
    service = running_app.service

    draft = service.create(identity=identity_simple, metadata=metadata)
    assert draft.id

    success = service.delete_draft(draft.id, identity_simple)
    assert success

    # Check draft deleted
    with pytest.raises(PIDDoesNotExistError):
        delete_draft = service.read_draft(draft.id, identity=identity_simple)


def _create_and_publish(service, metadata, identity_simple):
    """Creates a draft and publishes it."""
    # Cannot create with record service due to the lack of versioning
    draft = service.create(identity=identity_simple, metadata=metadata)

    record = service.publish(draft.id, identity=identity_simple)

    assert record.id == draft.id

    # files attribute in record causes at create change the revision_id twice
    assert record._record.revision_id == 1

    return record


def test_publish_draft(running_app, metadata):
    """Test draft publishing of a non-existing record.

    Note that the publish action requires a draft to be created first.
    """
    service = running_app.service
    identity_simple = running_app.identity_simple
    record = _create_and_publish(service, metadata, identity_simple)
    assert record._record.pid.status == PIDStatus.REGISTERED

    # Check draft deleted
    with pytest.raises(NoResultFound):
        draft = service.read_draft(id_=record.id, identity=identity_simple)

    # Test record exists
    record = service.read(id_=record.id, identity=identity_simple)

    assert record.id
    assert record._record.pid.status == PIDStatus.REGISTERED


def _test_metadata(metadata, metadata2):
    assert metadata.keys() == metadata2.keys()
    for key in metadata.keys():
        assert metadata[key] == metadata2[key]


def test_update_draft(running_app, metadata, metadata2):
    service = running_app.service
    identity_simple = running_app.identity_simple
    draft = service.create(identity=identity_simple, metadata=metadata)
    assert draft.id

    # Update draft content
    update_draft = service.update_draft(
        draft.id, identity=identity_simple, metadata=metadata2
    )

    # Check the updates where savedif "json" in data:

    read_draft = service.read_draft(id_=draft.id, identity=identity_simple)

    assert draft.id == update_draft.id
    _test_metadata(
        to_marc21.do(update_draft["metadata"]["json"]),
        to_marc21.do(read_draft["metadata"]["json"]),
    )


def test_create_publish_new_version(running_app, metadata):
    """Test creating a new revision of a record.

    This tests the `new_version` service method.
    """
    service = running_app.service
    identity_simple = running_app.identity_simple
    record = _create_and_publish(service, metadata, identity_simple)
    marcid = record.id

    # Create new version
    draft = service.new_version(marcid, identity_simple)

    # files attribute in record causes at create change the revision_id twice
    assert draft._record.revision_id == 3
    assert draft["id"] != record["id"]
    assert draft._record.pid.status == PIDStatus.NEW

    # Publish it
    record_2 = service.publish(draft.id, identity_simple)

    assert record_2.id
    assert record_2._record.pid.status == PIDStatus.REGISTERED

    # files attribute in record causes at create change the revision_id twice
    assert record_2._record.revision_id == 1
    assert record_2["id"] != record["id"]
