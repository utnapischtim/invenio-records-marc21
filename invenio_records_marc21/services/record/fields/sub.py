# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 sub field class."""


from os import linesep


class SubField(object):
    """SubField class representing the subfield HTML tag in MARC21 XML."""

    def __init__(self, code: str = "", value: str = ""):
        """Default constructor of the class."""
        self.code = code
        self.value = value

    def to_xml_tag(self, tagsep: str = linesep, indent: int = 4) -> str:
        """Get the Marc21 Subfield XML tag as string."""
        subfield_tag = 2 * " " * indent
        subfield_tag += f'<subfield code="{self.code}">{self.value}'
        subfield_tag += f"</subfield>"
        subfield_tag += tagsep
        return subfield_tag
