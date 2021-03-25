# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# invenio-records-marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Marc21 Api."""

from __future__ import absolute_import, print_function

from invenio_drafts_resources.records import Draft, Record
from invenio_records.systemfields import ModelField
from invenio_records_resources.records.api import RecordFile as BaseRecordFile
from invenio_records_resources.records.systemfields import (
    FilesField,
    IndexField,
    PIDField,
)
from werkzeug.local import LocalProxy

from .models import DraftFile, DraftMetadata, RecordFile, RecordMetadata
from .systemfields import (
    MarcDraftProvider,
    MarcPIDFieldContext,
    MarcRecordProvider,
    MarcResolver,
)


class DraftFile(BaseRecordFile):
    """Marc21 file associated with a marc21 draft model."""

    model_cls = DraftFile
    record_cls = LocalProxy(lambda: Marc21Draft)


class Marc21Draft(Draft):
    """Marc21 draft API."""

    model_cls = DraftMetadata

    index = IndexField(
        "marc21records-drafts-marc21-v1.0.0", search_alias="marc21records-marc21"
    )

    pid = PIDField(
        key="id",
        provider=MarcDraftProvider,
        context_cls=MarcPIDFieldContext,
        resolver_cls=MarcResolver,
        delete=False,
    )

    conceptpid = PIDField(
        key="conceptid",
        provider=MarcDraftProvider,
        context_cls=MarcPIDFieldContext,
        resolver_cls=MarcResolver,
        delete=False,
    )

    files = FilesField(
        store=False,
        file_cls=DraftFile,
        delete=False,
    )

    bucket_id = ModelField(dump=False)

    bucket = ModelField(dump=False)


class RecordFile(BaseRecordFile):
    """Marc21 record file API."""

    model_cls = RecordFile
    record_cls = LocalProxy(lambda: Marc21Record)


class Marc21Record(Record):
    """Define API for Marc21 create and manipulate."""

    model_cls = RecordMetadata

    index = IndexField(
        "marc21records-marc21-marc21-v1.0.0", search_alias="marc21records-marc21"
    )

    pid = PIDField(
        key="id",
        provider=MarcRecordProvider,
        delete=False,
        context_cls=MarcPIDFieldContext,
        resolver_cls=MarcResolver,
    )

    conceptpid = PIDField(
        key="conceptid",
        provider=MarcRecordProvider,
        delete=False,
        context_cls=MarcPIDFieldContext,
        resolver_cls=MarcResolver,
    )

    files = FilesField(
        store=False,
        file_cls=RecordFile,
        create=False,
        delete=False,
    )

    bucket_id = ModelField(dump=False)

    bucket = ModelField(dump=False)
