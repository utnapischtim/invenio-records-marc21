# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Flask extension for Invenio-Records-Marc21."""

from __future__ import absolute_import, print_function

import six
from invenio_records_resources.resources import FileResource
from invenio_records_resources.services import FileService
from werkzeug.utils import import_string

from . import config
from .services import (
    Marc21DraftFilesServiceConfig,
    Marc21RecordFilesServiceConfig,
    Marc21RecordPermissionPolicy,
    Marc21RecordService,
    Marc21RecordServiceConfig,
)


def obj_or_import_string(value, default=None):
    """Import string or return object.

    :params value: Import path or class object to instantiate.
    :params default: Default object to return if the import fails.
    :returns: The imported object.
    """
    if isinstance(value, six.string_types):
        return import_string(value)
    elif value:
        return value
    return default


class InvenioRecordsMARC21(object):
    """Invenio-Records-Marc21 extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        self.init_services(app)
        app.extensions["invenio-records-marc21"] = self

    def init_config(self, app):
        """Initialize configuration.

        Override configuration variables with the values in this package.
        """
        with_endpoints = app.config.get("INVENIO_MARC21_ENDPOINTS_ENABLED", True)
        for k in dir(config):
            if k.startswith("INVENIO_MARC21_"):
                app.config.setdefault(k, getattr(config, k))
            elif k == "SEARCH_UI_JSTEMPLATE_RESULTS":
                app.config["SEARCH_UI_JSTEMPLATE_RESULTS"] = getattr(config, k)
            else:
                for n in [
                    "INVENIO_MARC21_REST_ENDPOINTS",
                    "INVENIO_MARC21_UI_ENDPOINTS",
                ]:
                    if k == n and with_endpoints:
                        app.config.setdefault(n, {})
                        app.config[n].update(getattr(config, k))

    def init_services(self, app):
        """Initialize services."""
        service_config = Marc21RecordServiceConfig
        service_config.permission_policy_cls = obj_or_import_string(
            app.config.get("RECORDS_PERMISSIONS_RECORD_POLICY1"),
            default=Marc21RecordPermissionPolicy,
        )
        self.records_service = Marc21RecordService(
            config=service_config,
            files_service=FileService(Marc21RecordFilesServiceConfig),
            draft_files_service=FileService(Marc21DraftFilesServiceConfig),
        )

        self.records_resource = Marc21RecordResource(
            service=self.records_service,
            config=app.config.get(Marc21RecordResource.config_name),
        )

        self.drafts_resource = Marc21DraftResource(
            service=self.records_service,
            config=app.config.get(Marc21DraftResource.config_name),
        )
