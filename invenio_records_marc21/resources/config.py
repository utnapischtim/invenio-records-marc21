# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Resources configuration."""
import marshmallow as ma
from flask_resources import (
    JSONDeserializer,
    JSONSerializer,
    RequestBodyParser,
    ResponseHandler,
)
from flask_resources.serializers import JSONSerializer
from invenio_drafts_resources.resources import RecordResourceConfig
from invenio_records_resources.resources.files import FileResourceConfig
from invenio_records_resources.resources.records.args import SearchRequestArgsSchema

from .serializers.ui import UIJSONSerializer

record_serializer = {
    "application/json": ResponseHandler(UIJSONSerializer()),
    "application/vnd.inveniomarc21.v1+json": ResponseHandler(UIJSONSerializer()),
}

url_prefix = "/marc21"

record_ui_routes = {
    "search" : f"{url_prefix}",
    "list": f"{url_prefix}/list",
    "item": f"{url_prefix}/<pid_value>",
    "item-versions": f"{url_prefix}/<pid_value>/versions",
    "item-latest": f"{url_prefix}/<pid_value>/versions/latest",
    "item-draft": f"{url_prefix}/<pid_value>/draft",
    "item-publish": f"{url_prefix}/<pid_value>/draft/actions/publish",
    "item-files-import": f"{url_prefix}/<pid_value>/draft/actions/files-import",
}


class Marc21RecordResourceConfig(RecordResourceConfig):
    """Marc21 Record resource configuration."""

    blueprint_name = "marc21_records"
    url_prefix = url_prefix

    default_accept_mimetype = "application/json"

    response_handlers = record_serializer

    request_view_args = {
        "pid_value": ma.fields.Str(),
        "pid_type": ma.fields.Str(),
    }
    links_config = {}

    routes = record_ui_routes

    # Request parsing
    request_args = SearchRequestArgsSchema
    request_view_args = {"pid_value": ma.fields.Str()}
    request_headers = {"if_match": ma.fields.Int()}
    request_body_parsers = {"application/json": RequestBodyParser(JSONDeserializer())}

    request_view_args = {
        "pid_value": ma.fields.Str(),
        "pid_type": ma.fields.Str(),
    }


class Marc21RecordFilesResourceConfig(FileResourceConfig):
    """Bibliographic record files resource config."""

    allow_upload = False
    blueprint_name = "marc21_files"
    url_prefix = f"{url_prefix}/<pid_value>"

    links_config = {}


#
# Draft files
#
class Marc21DraftFilesResourceConfig(FileResourceConfig):
    """Bibliographic record files resource config."""

    blueprint_name = "marc21_draft_files"
    url_prefix = f"{url_prefix}/<pid_value>/draft"


class Marc21ParentRecordLinksResourceConfig(RecordResourceConfig):
    """User records resource configuration."""

    blueprint_name = "marc21_access"

    url_prefix = f"{url_prefix}/<pid_value>/access"

    routes = {
        "search" : "",
        "list": "/links",
        "item": "/links/<link_id>",
    }

    links_config = {}

    request_view_args = {"pid_value": ma.fields.Str(), "link_id": ma.fields.Str()}

    response_handlers = {"application/json": ResponseHandler(JSONSerializer())}
