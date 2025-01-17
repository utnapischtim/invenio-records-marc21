# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# invenio-records-marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Marc21 Api."""

from __future__ import absolute_import, print_function

from invenio_drafts_resources.records import Draft, Record
from invenio_drafts_resources.records.api import ParentRecord as BaseParentRecord
from invenio_drafts_resources.records.systemfields import ParentField
from invenio_records.systemfields import ConstantField, ModelField
from invenio_records_resources.records.api import FileRecord as BaseFileRecord
from invenio_records_resources.records.systemfields import (
    FilesField,
    IndexField,
    PIDField,
)
from werkzeug.local import LocalProxy

from . import models
from .systemfields import (
    MarcDraftProvider,
    MarcPIDFieldContext,
    MarcRecordProvider,
    MarcResolver,
)
from .systemfields.access import ParentRecordAccessField, RecordAccessField


#
# Parent record API
#
class Marc21Parent(BaseParentRecord):
    """Parent record."""

    versions_model_cls = models.VersionsState
    model_cls = models.ParentMetadata

    schema = ConstantField("$schema", "local://marc21/parent-v1.0.0.json")

    pid = PIDField(
        key="id",
        provider=MarcDraftProvider,
        context_cls=MarcPIDFieldContext,
        resolver_cls=MarcResolver,
        delete=False,
    )
    access = ParentRecordAccessField()


class DraftFile(BaseFileRecord):
    """Marc21 file associated with a marc21 draft model."""

    model_cls = models.DraftFile
    record_cls = LocalProxy(lambda: Marc21Draft)


class Marc21Draft(Draft):
    """Marc21 draft API."""

    model_cls = models.DraftMetadata
    versions_model_cls = models.VersionsState
    parent_record_cls = Marc21Parent

    index = IndexField(
        "marc21records-drafts-marc21-v1.0.0", search_alias="marc21records-marc21"
    )

    parent = ParentField(Marc21Parent, create=True, soft_delete=False, hard_delete=True)

    pid = PIDField(
        key="id",
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
    access = RecordAccessField()

    bucket_id = ModelField(dump=False)

    bucket = ModelField(dump=False)


class RecordFile(BaseFileRecord):
    """Marc21 record file API."""

    model_cls = models.RecordFile
    record_cls = LocalProxy(lambda: Marc21Record)


class Marc21Record(Record):
    """Define API for Marc21 create and manipulate."""

    model_cls = models.RecordMetadata
    versions_model_cls = models.VersionsState
    parent_record_cls = Marc21Parent

    index = IndexField(
        "marc21records-marc21-marc21-v1.0.0", search_alias="marc21records-marc21"
    )

    parent = ParentField(Marc21Parent, create=True, soft_delete=False, hard_delete=True)

    pid = PIDField(
        key="id",
        provider=MarcRecordProvider,
        context_cls=MarcPIDFieldContext,
        resolver_cls=MarcResolver,
        delete=False,
    )

    files = FilesField(
        store=False,
        file_cls=RecordFile,
        create=False,
        delete=False,
    )

    access = RecordAccessField()

    bucket_id = ModelField(dump=False)

    bucket = ModelField(dump=False)
