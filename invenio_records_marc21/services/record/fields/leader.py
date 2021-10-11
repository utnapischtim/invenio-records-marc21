# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 leader field class."""


from os import linesep


class LeaderField(object):
    """LeaderField class representing the leaderfield HTML tag in MARC21 XML."""

    def __init__(self, data=None, **kwargs):
        """Default constructor of the class."""
        if data is not None:
            self._load_from_str(data)
        else:
            self._load_from_dict(**kwargs)

    def _load_from_str(self, data: str):
        if len(data) != 24:
            raise ValueError("Leader must have 24 characters!!")
        self.length = data[0:5]
        self.status = data[5]
        self.type = data[6]
        self.level = data[7]
        self.control = data[8]
        self.charset = data[9]

        self.ind_count = data[10]
        self.sub_count = data[11]
        self.address = data[12:17]
        self.encoding = data[17]
        self.description = data[18]
        self.multipart_resource_record_level = data[19]
        self.length_field_position = data[20]
        self.length_starting_character_position_portion = data[21]
        self.length_implementation_defined_portion = data[22]
        self.undefined = data[23]

    def _load_from_dict(self, **kwargs):
        self.length = kwargs.get("length", "00000")  # 00-04
        self.status = kwargs.get("status", "n")  # 05
        self.type = kwargs.get("type", "a")  # 06
        self.level = kwargs.get("level", "m")  # 07
        self.control = kwargs.get("control", " ")  # 08
        self.charset = kwargs.get("charset", "a")  # 09

        self.ind_count = kwargs.get("ind_count", "2")  # 10
        self.sub_count = kwargs.get("sub_count", "2")  # 11
        self.address = kwargs.get("address", "00000")  # 12-16
        self.encoding = kwargs.get("encoding", "z")  # 17
        self.description = kwargs.get("description", "c")  # 18
        self.multipart_resource_record_level = kwargs.get(
            "multipart_resource_record_level", "a"
        )  # 19
        self.length_field_position = kwargs.get("length_field_position", "4")  # 20
        self.length_starting_character_position_portion = kwargs.get(
            "length_starting_character_position_portion", "5"
        )  # 21
        self.length_implementation_defined_portion = kwargs.get(
            "length_implementation_defined_portion", "0"
        )  # 22
        self.undefined = kwargs.get("undefined", "0")  # 23

    def to_xml_tag(self, tagsep: str = linesep, indent: int = 4) -> str:
        """Get the Marc21 Leaderfield XML tag as string."""
        leader = " " * indent
        leader += "<leader>"
        leader += f"{self.length}{self.status}{self.type}{self.level}{self.control}{self.charset}"
        leader += f"{self.ind_count}{self.sub_count}{self.address}{self.encoding}{self.description}"
        leader += f"{self.multipart_resource_record_level}{self.length_field_position}"
        leader += f"{self.length_starting_character_position_portion}{self.length_implementation_defined_portion}"
        leader += f"{self.undefined}"
        leader += "</leader>"
        leader += tagsep
        return leader
