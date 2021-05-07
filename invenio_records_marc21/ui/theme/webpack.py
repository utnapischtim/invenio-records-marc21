# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""JS/CSS Webpack bundles for theme."""

from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    "assets",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
                "invenio-records-marc21-search": "./js/invenio_records_marc21/search/index.js",
            },
            dependencies={
                "@babel/runtime": "^7.9.0",
                "formik": "^2.1.4",
                "luxon": "^1.23.0",
                "path": "^0.12.7",
                "prop-types": "^15.7.2",
                "react-dnd": "^11.1.3",
                "react-dnd-html5-backend": "^11.1.3",
                "react-invenio-forms": "^0.6.3",
                "react-dropzone": "^11.0.3",
                "yup": "^0.27.0",
                "@ckeditor/ckeditor5-build-classic": "^16.0.0",
                "@ckeditor/ckeditor5-react": "^2.1.0",
            },
            aliases={
                "themes/marc21": "less/invenio_records_marc21/theme",
                "@less/invenio_records_marc21": "less/invenio_records_marc21",
            },
        ),
    },
)
