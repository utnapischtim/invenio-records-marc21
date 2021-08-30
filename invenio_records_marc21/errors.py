# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 error messages."""

from flask_babelex import gettext as _

error_messages = {
    "ProgrammingError": [
        {
            "args": "UndefinedTable",
            "message": _(
                "The table you are looking for does not exist.\n"
                "Maybe you missed to re-setup the services after the marc21 module was installed.\n"
                "Try to do a invenio-cli services setup -f"
            ),
        },
    ],
    "OperationalError": [
        {
            "args": "could not connect to server",
            "message": _(
                "Connection to Database refused.\n"
                "Maybe you missed to start the database service.\n"
                "Try to do a invenio-cli services setup -f"
            ),
        },
    ],
}
