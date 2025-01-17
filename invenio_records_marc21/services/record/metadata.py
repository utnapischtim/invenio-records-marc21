# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Marc21 record class."""

from io import StringIO
from os import linesep
from os.path import dirname, join

from lxml import etree

from .fields import DataField, LeaderField, SubField


class Marc21Metadata(object):
    """MARC21 Record class to facilitate storage of records in MARC21 format."""

    def __init__(self, leader: LeaderField = LeaderField()):
        """Default constructor of the class."""
        self._xml = ""
        self._json = {}
        self.leader = leader
        self.controlfields = list()
        self.datafields = list()

    @property
    def json(self):
        """Metadata json getter method."""
        return self._json

    @json.setter
    def json(self, json: dict):
        """Metadata json setter method."""
        if not isinstance(json, dict):
            raise TypeError("json must be from type dict")
        self._json = json

    @property
    def xml(self):
        """Metadata xml getter method."""
        self._to_string()
        return self._xml

    @xml.setter
    def xml(self, xml: str):
        """Metadata xml setter method."""
        if not isinstance(xml, str):
            raise TypeError("xml must be from type str")

        self._to_xml_tree(xml)
        self._xml = xml

    def _to_xml_tree(self, xml: str):
        """Xml to internal representation method."""
        test = etree.parse(StringIO(xml))
        for element in test.iter():
            if "datafield" in element.tag:
                self.datafields.append(DataField(**element.attrib))
            elif "subfield" in element.tag:
                self.datafields[-1].subfields.append(
                    SubField(**element.attrib, value=element.text)
                )

    def _to_string(self, tagsep: str = linesep, indent: int = 4) -> str:
        """Get a pretty-printed XML string of the record."""
        self._xml = "<?xml version='1.0' ?>"
        self._xml += '<record xmlns="http://www.loc.gov/MARC21/slim" xsi:schemaLocation="http://www.loc.gov/MARC21/slim schema.xsd" type="Bibliographic" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        self._xml += tagsep
        if self.leader:
            self._xml += self.leader.to_xml_tag(tagsep, indent)
        for controlfield in self.controlfields:
            self._xml += controlfield.to_xml_tag(tagsep, indent)
        for datafield in self.datafields:
            self._xml += datafield.to_xml_tag(tagsep, indent)
        self._xml += "</record>"

    def contains(self, ref_df: DataField, ref_sf: SubField) -> bool:
        """Return True if record contains reference datafield, which contains reference subfield."""
        for df in self.datafields:
            if (
                df.tag == ref_df.tag and df.ind1 == ref_df.ind1 and df.ind2 == ref_df.ind2
            ):
                for sf in df.subfields:
                    if sf.code == ref_sf.code and sf.value == ref_sf.value:
                        return True
        return False

    def emplace_field(
        self,
        tag: str = "",
        ind1: str = " ",
        ind2: str = " ",
        code: str = "",
        value: str = "",
    ) -> None:
        """Add value to record for given datafield and subfield."""
        datafield = DataField(tag, ind1, ind2)
        subfield = SubField(code, value)
        datafield.subfields.append(subfield)
        self.datafields.append(datafield)

    def emplace_unique_field(
        self,
        tag: str = "",
        ind1: str = " ",
        ind2: str = " ",
        code: str = "",
        value: str = "",
    ) -> None:
        """Add value to record if it doesn't already contain it."""
        datafield = DataField(tag, ind1, ind2)
        subfield = SubField(code, value)
        if not self.contains(datafield, subfield):
            datafield.subfields.append(subfield)
            self.datafields.append(datafield)

    def is_valid_marc21_xml_string(self) -> bool:
        """Validate the record against a Marc21XML Schema."""
        with open(
            join(dirname(__file__), "schema", "MARC21slim.xsd"), "r", encoding="utf-8"
        ) as fp:
            marc21xml_schema = etree.XMLSchema(etree.parse(fp))
            marc21xml = etree.parse(StringIO(self.xml))
            return marc21xml_schema.validate(marc21xml)
