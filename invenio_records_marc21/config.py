# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Default configuration."""

from __future__ import absolute_import, print_function

INVENIO_MARC21_BASE_TEMPLATE = "invenio_records_marc21/base.html"

INVENIO_MARC21_REST_ENDPOINTS = {}
"""REST API for invenio-records-marc21."""

INVENIO_MARC21_RECORD_EXPORTERS = {
    "json": {
        "name": "JSON",
        "serializer": (
            "invenio_records_marc21.resources.serializers.ui:" "UIJSONSerializer"
        ),
    }
}

INVENIO_MARC21_UI_ENDPOINTS = {
    "record-detail": "/<pid_value>",
    "record-export": "/<pid_value>/export/<export_format>",
}

INVENIO_MARC21_UI_THEME_ENDPOINTS = {
    "index": "/",
    "record-search": "/search",
}

"""Records UI for invenio-records-marc21."""

SEARCH_UI_JSTEMPLATE_RESULTS = "templates/invenio_records_marc21/results.html"
"""Result list template."""

INVENIO_MARC21_ENDPOINTS_ENABLED = True
"""Enable/disable automatic endpoint registration."""
