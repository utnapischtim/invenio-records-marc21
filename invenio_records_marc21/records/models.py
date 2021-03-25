# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Marc21 Record and Draft models."""

from invenio_db import db
from invenio_drafts_resources.records import DraftMetadataBase
from invenio_files_rest.models import Bucket
from invenio_records.models import RecordMetadataBase
from invenio_records_resources.records.models import RecordFileBase
from sqlalchemy_utils.types import UUIDType


class RecordMetadata(db.Model, RecordMetadataBase):
    """Represent a marc21 record metadata."""

    __tablename__ = "marc21_records_metadata"

    __versioned__ = {}

    bucket_id = db.Column(UUIDType, db.ForeignKey(Bucket.id))
    bucket = db.relationship(Bucket)


class DraftMetadata(db.Model, DraftMetadataBase):
    """Represent a marc21 record draft metadata."""

    __tablename__ = "marc21_drafts_metadata"

    bucket_id = db.Column(UUIDType, db.ForeignKey(Bucket.id))
    bucket = db.relationship(Bucket)


class RecordFile(db.Model, RecordFileBase):
    """File associated with a marc21 record."""

    record_model_cls = RecordMetadata

    __tablename__ = "marc21_records_files"


class DraftFile(db.Model, RecordFileBase):
    """File associated with a marc21 draft."""

    record_model_cls = DraftMetadata

    __tablename__ = "marc21_drafts_files"
