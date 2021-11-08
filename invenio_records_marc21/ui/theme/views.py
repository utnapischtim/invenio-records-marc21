# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Routes for general pages provided by Invenio-Records-Marc21."""

from flask import render_template
from flask_login import login_required

from .deposit import deposit_config, deposit_templates, empty_record


def index():
    """Frontpage."""
    return render_template("invenio_records_marc21/index.html")


def search():
    """Search help guide."""
    return render_template("invenio_records_marc21/search.html")


@login_required
def deposit_create():
    """Create a new deposit page."""
    return render_template(
        "invenio_records_marc21/deposit.html",
        record=empty_record(),
        templates=deposit_templates(),
        forms_config=deposit_config(),
    )
