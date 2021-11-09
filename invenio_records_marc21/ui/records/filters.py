# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Filters to be used in the Jinja templates."""

import re
from flask_babelex import gettext as _
import idutils
from dojson.contrib.marc21.utils import create_record
from dojson.contrib.to_marc21 import to_marc21
from flask import current_app


PERSONAL_CODES = {
    "aut": _("Author")
}

def get_personal_code(code):
    return PERSONAL_CODES.get(code, code)


def pid_url(identifier, scheme=None, url_scheme="https"):
    """Convert persistent identifier into a link."""
    if scheme is None:
        try:
            scheme = idutils.detect_identifier_schemes(identifier)[0]
        except IndexError:
            scheme = None
    try:
        if scheme and identifier:
            return idutils.to_url(identifier, scheme, url_scheme=url_scheme)
    except Exception:
        current_app.logger.warning(
            f"URL generation for identifier {identifier} failed.",
            exc_info=True,
        )
    return ""


def marc21_to_json(marcxml):
    """Convert record into json."""
    return create_record(marcxml)


def json_to_marc21(json):
    """Convert record into marc21 xml."""
    return to_marc21.do(json)


def sanitize_title(title):
    """Sanitize record title."""
    return re.sub("[<>]", "", title)


def personal_name(titles):
    """Personal Name for the Frontend."""
    name = titles.get("personal_name")
    code = get_personal_code(titles.get("relator_code"))

    return f"{name}[{code}]"
