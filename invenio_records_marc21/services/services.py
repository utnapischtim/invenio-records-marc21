# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Marc21 Record Service."""

from invenio_drafts_resources.services.records import (
    RecordDraftService,
    RecordDraftServiceConfig,
)
from invenio_drafts_resources.services.records.components import (
    DraftFilesComponent,
    RelationsComponent,
)
from invenio_records_resources.services.files.config import FileServiceConfig
from invenio_records_resources.services.files.service import RecordFileService
from invenio_records_resources.services.records.components import MetadataComponent
from invenio_records_resources.services.records.search import terms_filter
from invenio_records_resources.services.records.service import RecordService

from ..api import Marc21Draft, Marc21Record
from .components import AccessComponent
from .permissions import Marc21RecordPermissionPolicy
from .schemas import Marc21RecordSchema


class Marc21RecordServiceConfig(RecordDraftServiceConfig):
    """Marc21 record service config."""

    # Record class
    record_cls = Marc21Record
    # Draft class
    draft_cls = Marc21Draft

    schema = Marc21RecordSchema
    permission_policy_cls = Marc21RecordPermissionPolicy

    search_facets_options = dict(
        aggs={
            "resource_type": {
                "terms": {"field": "metadata.resource_type.type"},
                "aggs": {
                    "subtype": {
                        "terms": {"field": "metadata.resource_type.subtype"},
                    }
                },
            },
            "access_right": {
                "terms": {"field": "access.access_right"},
            },
            "languages": {
                "terms": {"field": "metadata.languages.id"},
            },
        },
        post_filters={
            "subtype": terms_filter("metadata.resource_type.subtype"),
            "resource_type": terms_filter("metadata.resource_type.type"),
            "access_right": terms_filter("access.access_right"),
            "languages": terms_filter("metadata.languages.id"),
        },
    )

    components = [
        MetadataComponent,
        AccessComponent,
    ]


class Marc21RecordService(RecordDraftService):
    """Bibliographic record service."""

    config_name = "MARC21_RECORDS_BIBLIOGRAPHIC_SERVICE_CONFIG"
    default_config = Marc21RecordServiceConfig
