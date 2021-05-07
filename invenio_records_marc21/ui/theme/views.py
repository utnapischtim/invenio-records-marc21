# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Routes for general pages provided by Invenio-Records-Marc21."""

from flask import render_template


def index():
    """Frontpage."""
    return render_template("invenio_records_marc21/index.html")


def search():
    """Search help guide."""
    return render_template("invenio_records_marc21/search.html")
