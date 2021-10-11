# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 data field class."""


from os import linesep
from .sub import SubField


class DataField(object):
    """DataField class representing the datafield HTML tag in MARC21 XML."""

    def __init__(self, tag: str = "", ind1: str = " ", ind2: str = " ", subfields=None):
        """Default constructor of the class."""
        self.tag = tag
        self.ind1 = ind1
        self.ind2 = ind2
        self.subfields = list()
        if subfields:
            self.init_subfields(subfields)

    def init_subfields(self, subfields):
        """Init containing subfields."""
        for subfield in subfields:
            self.subfields.append(SubField(**subfield.attrib, value=subfield.text))

    def to_xml_tag(self, tagsep: str = linesep, indent: int = 4) -> str:
        """Get the Marc21 Datafield XML tag as string."""
        datafield_tag = " " * indent
        datafield_tag += (
            f'<datafield tag="{self.tag}" ind1="{self.ind1}" ind2="{self.ind2}">'
        )
        datafield_tag += tagsep
        for subfield in self.subfields:
            datafield_tag += subfield.to_xml_tag(tagsep, indent)
        datafield_tag += " " * indent
        datafield_tag += "</datafield>"
        datafield_tag += tagsep
        return datafield_tag
