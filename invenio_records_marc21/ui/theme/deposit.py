# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Marc21 records deposit backend."""


from flask import current_app, g
from invenio_communities.proxies import current_communities
from invenio_i18n.ext import current_i18n
from invenio_rdm_records.services.schemas.utils import dump_empty

from invenio_records_marc21.services.schemas import Marc21RecordSchema

from ...proxies import current_records_marc21


def empty_record():
    """Create an empty record."""
    record = dump_empty(Marc21RecordSchema)
    record["metadata"] = "<record><leader>00000nam a2200000zca4500</leader></record>"
    record["access"] = {"record": "public", "files": "public"}
    record["files"] = {"enabled": True}
    record["status"] = "draft"
    return record


def get_user_communities_memberships():
    """Return current identity communities memberships."""
    memberships = current_communities.service.members.read_memberships(g.identity)
    return {id: role for (id, role) in memberships["memberships"]}



def get_user_roles(identity):
    """Get user role names."""
    roles = [role.name for role in identity.user.roles]
    return roles


def deposit_templates():
    """Retrieve from DB the tamplates for marc21 deposit form."""
    roles = get_user_roles(g.identity)
    templates = current_records_marc21.templates_service.get_templates(roles=roles)

    if templates:
        return [template.to_dict() for template in templates]
    return []


def deposit_config(**kwargs):
    """Create an deposit configuration."""
    app_config = current_app.config
    jsonschema = current_app.extensions["invenio-jsonschemas"]
    schema = {}
    if jsonschema:
        schema = jsonschema.get_schema(path="marc21/marc21-structure-v1.0.0.json")
    config = dict(
        current_locale=str(current_i18n.locale),
        default_locale=app_config.get("BABEL_DEFAULT_LOCALE", "en"),
        error="",
        schema=schema,
        quota=app_config.get("APP_RDM_DEPOSIT_FORM_QUOTA"),
        createUrl="/api/publications",
        apiHeaders=app_config.get("MARC21_API_HEADERS"),
        user_communities_memberships=get_user_communities_memberships(),
        # UploadFilesToolbar  disable file upload
        canHaveMetadataOnlyRecords=True,
        **kwargs
    )
    return config
