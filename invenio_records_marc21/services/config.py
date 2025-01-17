# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Marc21 Record Service config."""


from flask_babelex import gettext as _
from invenio_drafts_resources.services.records.config import (
    RecordServiceConfig,
    SearchDraftsOptions,
    SearchOptions,
    is_record,
)
from invenio_records_resources.services import (
    ConditionalLink,
    FileServiceConfig,
    pagination_links,
)
from invenio_records_resources.services.files.config import FileServiceConfig
from invenio_records_resources.services.records.facets import TermsFacet
from invenio_records_resources.services.records.links import RecordLink

from ..records import Marc21Draft, Marc21Parent, Marc21Record
from ..records.systemfields.access import AccessStatusEnum
from .components import AccessComponent, MetadataComponent, PIDComponent
from .permissions import Marc21RecordPermissionPolicy
from .schemas import Marc21ParentSchema, Marc21RecordSchema

access_right_facet = TermsFacet(
    field="access.metadata",
    label=_("Access status"),
    value_labels={
        AccessStatusEnum.PUBLIC.value: _("Public"),
        AccessStatusEnum.EMBARGOED.value: _("Embargoed"),
        AccessStatusEnum.RESTRICTED.value: _("Restricted"),
    },
)

is_published_facet = TermsFacet(
    field="is_published",
    label=_("State"),
    value_labels={"true": _("Published"), "false": _("Unpublished")},
)


class Marc21SearchOptions(SearchOptions):
    """Search options for record search."""

    facets = {
        "access_right": access_right_facet,
    }


class Marc21SearchDraftsOptions(SearchDraftsOptions):
    """Search options for drafts search."""

    facets = {
        "access_right": access_right_facet,
        "is_published": is_published_facet,
    }


class Marc21RecordServiceConfig(RecordServiceConfig):
    """Marc21 record service config."""

    # Record class
    record_cls = Marc21Record
    # Draft class
    draft_cls = Marc21Draft
    # Parent class
    parent_record_cls = Marc21Parent

    # Schemas
    schema = Marc21RecordSchema
    schema_parent = Marc21ParentSchema

    # TODO: ussing from invenio-permissions
    permission_policy_cls = Marc21RecordPermissionPolicy

    links_search = pagination_links("{+api}/marc21{?args*}")

    links_search_drafts = pagination_links("{+api}/marc21/draft{?args*}")

    links_search_versions = pagination_links("{+api}/marc21/{id}/versions{?args*}")

    components = [
        MetadataComponent,
        AccessComponent,
        PIDComponent,
    ]

    links_item = {
        "self": ConditionalLink(
            cond=is_record,
            if_=RecordLink("{+api}/marc21/{id}"),
            else_=RecordLink("{+api}/marc21/{id}/draft"),
        ),
        "self_html": ConditionalLink(
            cond=is_record,
            if_=RecordLink("{+ui}/marc21/{id}"),
            else_=RecordLink("{+ui}/uploads/{id}"),
        ),
    }


#
# Record files
#
class Marc21RecordFilesServiceConfig(Marc21RecordServiceConfig, FileServiceConfig):
    """Marc21 record files service configuration."""


#
# Draft files
#
class Marc21DraftFilesServiceConfig(Marc21RecordServiceConfig, FileServiceConfig):
    """Marc21 draft files service configuration."""

    record_cls = Marc21Draft
