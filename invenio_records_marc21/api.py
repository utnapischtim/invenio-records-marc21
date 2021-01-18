# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# invenio-records-marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Marc21 Api."""

from __future__ import absolute_import, print_function

from flask import current_app
from invenio_db import db
from invenio_drafts_resources.records import Draft, Record
from invenio_jsonschemas import current_jsonschemas
from invenio_pidstore.models import PersistentIdentifier
from invenio_pidstore.resolver import Resolver
from invenio_records.dumpers import ElasticsearchDumper
from invenio_records.models import RecordMetadata
from invenio_records.systemfields import ModelField, RelationsField
from invenio_records_resources.records.systemfields import (  # FilesField,; PIDListRelation,
    IndexField,
)
from werkzeug.local import LocalProxy

from . import models


class Marc21Draft(Draft):
    """Marc21 draft API."""

    model_cls = models.DraftMetadata

    index = IndexField("marc21-drafts-marc21-v1.0.0", search_alias="marc21-drafts")


class Marc21Record(Record):
    """Define API for Marc21 creation and manipulation."""

    model_cls = models.RecordMetadata

    index = IndexField("marc21-marc21-v1.0.0", search_alias="marc21-marc21")
