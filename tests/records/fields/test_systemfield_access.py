#
# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test access system field."""


from datetime import timedelta

import arrow
import pytest

from invenio_records_marc21.records import Marc21Record
from invenio_records_marc21.records.systemfields.access import (
    Embargo,
    Protection,
    RecordAccess,
)

#
# Protection
#


def test_protection_valid():
    p = Protection("public", "public")
    assert p.metadata == "public"
    assert p.files == "public"
    p.set("restricted", files="restricted")
    assert p.metadata == "restricted"
    assert p.files == "restricted"


def test_protection_invalid_values():
    with pytest.raises(ValueError):
        Protection("invalid", "values")


#
# Embargo
#


def test_embargo_creation():
    future_date = arrow.utcnow().datetime + timedelta(days=+30)
    embargo = Embargo(
        until=future_date,
        reason="Because I can!",
    )
    assert embargo.active

    past_date = arrow.utcnow().datetime + timedelta(days=-30)
    embargo = Embargo(
        until=past_date,
        reason="espionage",
    )
    assert not embargo.active


def test_embargo_from_dict():
    date_feature = arrow.utcnow().datetime + timedelta(days=+30)
    embargo_dict = {
        "until": date_feature,
        "active": True,
        "reason": "espionage",
    }
    embargo = Embargo.from_dict(embargo_dict)
    assert embargo.active
    assert embargo.until == date_feature
    assert embargo.reason == "espionage"
    embargo_dict["until"] = date_feature.strftime("%Y-%m-%d")
    assert embargo.dump() == embargo_dict


def test_embargo_lift():
    future_date = arrow.utcnow().datetime + timedelta(days=+30)
    past_date = arrow.utcnow().datetime + timedelta(days=-30)
    embargo_dict1 = {"until": future_date, "active": True, "reason": "espionage"}
    embargo_dict2 = {"until": past_date, "active": True, "reason": "espionage"}
    new_embargo = Embargo.from_dict(embargo_dict1)
    old_embargo = Embargo.from_dict(embargo_dict2)

    assert old_embargo.lift()
    assert not old_embargo.active
    assert not new_embargo.lift()
    assert new_embargo.active


#
# Record Access System Field
#


def test_access_field_on_record(appaccess, marc21_record, parent):
    future_date = arrow.utcnow().datetime + timedelta(days=+30)
    marc21_record["access"]["embargo"] = {
        "until": future_date.strftime("%Y-%m-%d"),
        "active": True,
        "reason": "nothing in particular",
    }
    rec = Marc21Record.create(marc21_record, parent=parent)

    assert isinstance(rec.access, RecordAccess)
    assert isinstance(rec.access.protection, Protection)
    assert rec.access.protection.metadata == marc21_record["access"]["metadata"]
    assert rec.access.protection.files == marc21_record["access"]["files"]
    assert isinstance(rec.access.embargo, Embargo)


def test_access_field_update_embargo(appaccess, marc21_record, parent):
    future_date = arrow.utcnow().datetime + timedelta(days=+30)
    marc21_record["access"]["embargo"] = {
        "until": future_date.strftime("%Y-%m-%d"),
        "active": True,
        "reason": "Because I can",
    }
    rec = Marc21Record.create(marc21_record.copy(), parent=parent)
    assert rec.access.embargo

    rec.access.embargo.active = False
    rec.access.embargo.reason = "can't remember"
    rec.commit()

    marc21_record["access"]["embargo"]["active"] = False
    marc21_record["access"]["embargo"]["reason"] = "can't remember"


def test_access_field_clear_embargo(appaccess, marc21_record, parent):
    future_date = arrow.utcnow().datetime + timedelta(days=+30)
    marc21_record["access"]["embargo"] = {
        "until": future_date.strftime("%Y-%m-%d"),
        "active": True,
        "reason": "nothing in particular",
    }
    rec = Marc21Record.create(marc21_record, parent=parent)

    rec.access.embargo.clear()
    assert not rec.access.embargo


def test_access_field_update_protection(appaccess, marc21_record, parent):
    marc21_record["access"]["metadata"] = "restricted"
    marc21_record["access"]["files"] = "restricted"

    rec = Marc21Record.create(marc21_record, parent=parent)
    assert rec.access.protection.metadata == "restricted"
    assert rec.access.protection.files == "restricted"

    rec.access.protection.set("public", "public")
    rec.commit()

    assert rec["access"]["metadata"] == "public"
    assert rec["access"]["files"] == "public"
