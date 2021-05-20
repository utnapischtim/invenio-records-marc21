# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Marc21 Record Service config."""

from flask import current_app
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
from invenio_records_resources.services.records.links import RecordLink
from invenio_records_resources.services.records.search import terms_filter

from ..records import Marc21Draft, Marc21Parent, Marc21Record
from .components import AccessComponent, MetadataComponent, PIDComponent
from .permissions import Marc21RecordPermissionPolicy
from .schemas import Marc21ParentSchema, Marc21RecordSchema


class Marc21SearchOptions(SearchOptions):
    """Search options for record search."""

    facets_options = dict(
        aggs={
            "title": {
                "terms": {"field": "metadata.json.title_statement.title"},
            },
            "access_right": {
                "terms": {"field": "access.metadata"},
            },
        },
        post_filters={
            "title": terms_filter(
                "metadata.json.title_statement.title",
            ),
            "access_right": terms_filter("access.metadata"),
        },
    )


class Marc21SearchDraftsOptions(SearchDraftsOptions):
    """Search options for drafts search."""

    facets_options = dict(
        aggs={
            "resource_type": {
                "terms": {"field": "metadata"},
                "aggs": {},
            },
            "access_right": {
                "terms": {"field": "access.metadata"},
            },
            "is_published": {
                "terms": {"field": "is_published"},
            },
        },
        post_filters={
            "access_right": terms_filter("access.metadata"),
            "is_published": terms_filter("is_published"),
        },
    )


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

    search_facets_options = dict(
        aggs={
            "is_published": {
                "terms": {"field": "is_published"},
            },
        },
        post_filters={
            "access_right": terms_filter("access.status"),
            "is_published": terms_filter("is_published"),
        },
    )

    links_search = pagination_links("{+api}/marc21{?args*}")

    links_search_drafts = pagination_links("{+api}/marc21/draft{?args*}")

    links_search_versions = pagination_links(
        "{+api}/marc21/{id}/versions{?args*}")

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
