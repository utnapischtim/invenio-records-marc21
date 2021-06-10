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

from invenio_records_marc21.services.record.fields import LeaderField


def _assert_field_value(fields, object, expected):
    for key in fields:
        assert getattr(object, key) == expected[key]


def test_leaderfield(leader_kwargs):
    leaderfield = LeaderField()
    _assert_field_value(leader_kwargs.keys(), leaderfield, leader_kwargs)

    leader_kwargs["length"] = "99999"
    leaderfield = LeaderField(**leader_kwargs)
    _assert_field_value(leader_kwargs.keys(), leaderfield, leader_kwargs)

    leader_kwargs["status"] = "d"
    leaderfield = LeaderField(**leader_kwargs)
    _assert_field_value(leader_kwargs.keys(), leaderfield, leader_kwargs)

    leader_kwargs["type"] = "g"
    leaderfield = LeaderField(**leader_kwargs)
    _assert_field_value(leader_kwargs.keys(), leaderfield, leader_kwargs)

    leader_kwargs["level"] = "c"
    leaderfield = LeaderField(**leader_kwargs)
    _assert_field_value(leader_kwargs.keys(), leaderfield, leader_kwargs)

    leader_kwargs["control"] = "a"
    leaderfield = LeaderField(**leader_kwargs)
    _assert_field_value(leader_kwargs.keys(), leaderfield, leader_kwargs)

    leader_kwargs["charset"] = " "
    leaderfield = LeaderField(**leader_kwargs)
    _assert_field_value(leader_kwargs.keys(), leaderfield, leader_kwargs)

    leader_kwargs["ind_count"] = "6"
    leaderfield = LeaderField(**leader_kwargs)
    _assert_field_value(leader_kwargs.keys(), leaderfield, leader_kwargs)

    leader_kwargs["sub_count"] = "6"
    leaderfield = LeaderField(**leader_kwargs)
    _assert_field_value(leader_kwargs.keys(), leaderfield, leader_kwargs)

    leader_kwargs["ind_count"] = "6"
    leaderfield = LeaderField(**leader_kwargs)
    _assert_field_value(leader_kwargs.keys(), leaderfield, leader_kwargs)

    leader_kwargs["address"] = "99999"
    leaderfield = LeaderField(**leader_kwargs)
    _assert_field_value(leader_kwargs.keys(), leaderfield, leader_kwargs)

    leader_kwargs["encoding"] = "u"
    leaderfield = LeaderField(**leader_kwargs)
    _assert_field_value(leader_kwargs.keys(), leaderfield, leader_kwargs)

    leader_kwargs["description"] = "a"
    leaderfield = LeaderField(**leader_kwargs)
    _assert_field_value(leader_kwargs.keys(), leaderfield, leader_kwargs)

    leader_kwargs["multipart_resource_record_level"] = " "
    leaderfield = LeaderField(**leader_kwargs)
    _assert_field_value(leader_kwargs.keys(), leaderfield, leader_kwargs)

    leader_kwargs["length_field_position"] = "9"
    leaderfield = LeaderField(**leader_kwargs)
    _assert_field_value(leader_kwargs.keys(), leaderfield, leader_kwargs)

    leader_kwargs["length_starting_character_position_portion"] = "9"
    leaderfield = LeaderField(**leader_kwargs)
    _assert_field_value(leader_kwargs.keys(), leaderfield, leader_kwargs)

    leader_kwargs["length_implementation_defined_portion"] = "9"
    leaderfield = LeaderField(**leader_kwargs)
    _assert_field_value(leader_kwargs.keys(), leaderfield, leader_kwargs)

    leader_kwargs["undefined"] = "9"
    leaderfield = LeaderField(**leader_kwargs)
    _assert_field_value(leader_kwargs.keys(), leaderfield, leader_kwargs)


def test_leaderfield_to_xml(leader_kwargs):
    leaderfield = LeaderField(**leader_kwargs)
    xml = leaderfield.to_xml_tag()
    assert "<leader>00000nam a2200000zca4500</leader>" in xml
    assert xml.startswith("    ")
    assert xml.endswith("\n")

    xml = leaderfield.to_xml_tag(tagsep="", indent=0)
    assert "<leader>00000nam a2200000zca4500</leader>" == xml
