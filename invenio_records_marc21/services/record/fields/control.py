# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 control field class."""


from os import linesep


class ControlField(object):
    """ControlField class representing the controlfield HTML tag in MARC21 XML."""

    def __init__(self, tag: str = "", value: str = ""):
        """Default constructor of the class."""
        self.tag = tag
        self.value = value

    def to_xml_tag(self, tagsep: str = linesep, indent: int = 4) -> str:
        """Get the Marc21 Controlfield XML tag as string."""
        controlfield_tag = " " * indent
        controlfield_tag += f'<controlfield tag="{self.tag}">{self.value}'
        controlfield_tag += " " * indent
        controlfield_tag += "</controlfield>"
        controlfield_tag += tagsep
        return controlfield_tag
