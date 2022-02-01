# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
# Copyright (C) 2021 Northwestern University.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.


"""DataCite based Schema for Invenio RDM Records."""

from flask import current_app
from flask_babelex import lazy_gettext as _
from marshmallow import Schema, fields, missing


def get_scheme_datacite(scheme, config_name, default=None):
    """Returns the datacite equivalent of a scheme."""
    config_item = current_app.config[config_name]
    return config_item.get(scheme, {}).get("datacite", default)


class CreatorSchema43(Schema):
    """Creator schema for v4."""

    name = fields.Str(attribute="personal_name")


class Marc21DataCite43Schema(Schema):
    """DataCite JSON 4.3 Marshmallow Schema."""

    # PIDS-FIXME: What about versioning links and related ids
    identifiers = fields.Method("get_identifiers")
    types = fields.Method("get_type")
    titles = fields.Method("get_titles")
    creators = fields.Nested(
        CreatorSchema43, attribute="metadata.main_entry_personal_name"
    )
    publisher = fields.Str(attribute="metadata.publisher")
    publicationYear = fields.Method("get_publication_year")
    schemaVersion = fields.Constant("http://datacite.org/schema/kernel-4")

    def get_type(self, obj):
        """Get resource type."""
        # FIXME: The metadatafield 970 from dojson module needed
        return {
            "resourceTypeGeneral": "Other",
            "resourceType": "Text",
        }

    def get_titles(self, obj):
        """Get titles list."""
        titles = obj["metadata"].get("title_statement", {})
        return {"title": titles.get("title", "")}

    def get_publication_year(self, obj):
        """Get publication year from edtf date."""
        publication_dates = obj["metadata"].get(
            "dates_of_publication_and_or_sequential_designation", {}
        )
        publication_date = publication_dates.get(
            "dates_of_publication_and_or_sequential_designation", ""
        )
        return publication_date

    def get_language(self, obj):
        """Get language."""
        languages = obj["metadata"].get("languages", [])
        if languages:
            # DataCite support only one language, so we take the first.
            return languages[0]["id"]

        return missing

    def get_identifiers(self, obj):
        """Get (main and alternate) identifiers list."""
        serialized_identifiers = []

        # pids go first so the DOI from the record is included
        pids = obj["pids"]
        for scheme, id_ in pids.items():
            id_scheme = get_scheme_datacite(
                scheme,
                "INVENIO_MARC21_IDENTIFIERS_SCHEMES",
                default=scheme,
            )

            if id_scheme:
                serialized_identifiers.append(
                    {
                        "identifier": id_["identifier"],
                        "identifierType": id_scheme,
                    }
                )

        return serialized_identifiers or missing
