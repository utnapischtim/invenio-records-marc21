# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2023 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 Record Service."""


from invenio_db import db
from invenio_rdm_records.services import RDMRecordService
from invenio_records_resources.services.files.service import FileService
from invenio_records_resources.services.records.results import RecordItem
from invenio_records_resources.services.uow import unit_of_work
from invenio_search.engine import dsl
from sqlalchemy.orm.exc import NoResultFound

from .config import Marc21DraftFilesServiceConfig, Marc21RecordFilesServiceConfig
from .errors import EmbargoNotLiftedError
from .record import Marc21Metadata


class Marc21RecordService(RDMRecordService):
    """Marc21 record service class."""

    def _create_data(
        self, identity, data=None, metadata=None, files=False, access=None
    ):
        """Create a data json.

        :param identity: Identity of user creating the record.
        :type identity: `flask_principal.identity`
        :param data: Input data according to the data schema.
        :type data: dict
        :param metadata: Input data according to the metadata schema.
        :type metadata: `services.record.Marc21Metadata`
        :param files: enable/disable file support for the record.
        :type files: bool
        :param dict access: provide access additional information
        :return: marc21 record dict
        :rtype: dict
        """
        if data is None:
            data = metadata.json
        if "files" not in data:
            data["files"] = {"enabled": files}
        if "access" not in data:
            default_access = {
                "access": {
                    "record": "public",
                    "files": "public",
                },
            }
            if access is not None:
                default_access["access"].update(access)
            data.update(default_access)
        return data

    @unit_of_work()
    def create(
        self,
        identity,
        data=None,
        metadata=Marc21Metadata(),
        files=False,
        access=None,
        uow=None,
    ) -> RecordItem:
        """Create a draft record.

        :param identity: Identity of user creating the record.
        :type identity: `flask_principal.identity`
        :param data: Input data according to the data schema.
        :type data: dict
        :param metadata: Input data according to the metadata schema.
        :type metadata: `services.record.Marc21Metadata`
        :param files: enable/disable file support for the record.
        :type files: bool
        :param dict access: provide access additional information
        :return: marc21 record item
        :rtype: `invenio_records_resources.services.records.results.RecordItem`
        """
        data = self._create_data(identity, data, metadata, files, access)
        return super().create(identity=identity, data=data)

    @unit_of_work()
    def update_draft(
        self,
        identity,
        id_,
        data=None,
        metadata=Marc21Metadata(),
        revision_id=None,
        access=None,
        uow=None,
    ):
        """Update a draft record.

        :param identity: Identity of user creating the record.
        :type identity: `flask_principal.identity`
        :param data: Input data according to the data schema.
        :type data: dict
        :param metadata: Input data according to the metadata schema.
        :type metadata: `services.record.Marc21Metadata`
        :param files: enable/disable file support for the record.
        :type files: bool
        :param dict access: provide access additional information
        :return: marc21 record item
        :rtype: `invenio_records_resources.services.records.results.RecordItem`
        """
        data = self._create_data(identity, data, metadata, access=access)
        return super().update_draft(
            identity=identity, id_=id_, data=data, revision_id=revision_id
        )

    def _lift_embargo_from(self, record):
        """Lifts embargo from record or draft."""
        if not record.access.lift_embargo():
            raise EmbargoNotLiftedError(record["id"])
        record.access.protection.record = "public"
        record.access.protection.files = "public"

    def _is_draft_access_field_modified(self, draft, record):
        """Returns True if draft's access field was modified."""
        return draft.get("access") == record.get("access")

    @unit_of_work()
    def lift_embargo(self, identity, _id, uow=None):
        """Lifts embargo from the record and updates draft."""
        # Get the record
        record = self.record_cls.pid.resolve(_id)

        self.require_permission(identity, "lift_embargo", record=record)

        lifted_embargo_from_draft = False
        # Check if record has already a draft
        if record.has_draft:
            draft = self.draft_cls.pid.resolve(_id, registered_only=False)

            if self._is_draft_access_field_modified(draft, record):
                # Lifts embargo from draft
                self._lift_embargo_from(draft)
                lifted_embargo_from_draft = True

        # Lifts embargo from record
        self._lift_embargo_from(record)
        # Commit and index
        record.commit()
        if record.has_draft and lifted_embargo_from_draft:
            draft.commit()
        db.session.commit()
        self.indexer.index(record)
        if record.has_draft and lifted_embargo_from_draft:
            self.indexer.index(draft)

    def search_draft_or_record(
        self, identity, id_, params=None, search_preference=None, expand=False, **kwargs
    ):
        """Search for record's or draft."""
        try:
            record = self.record_cls.pid.resolve(id_, registered_only=False)
        except NoResultFound:
            record = self.draft_cls.pid.resolve(id_, registered_only=False)

        self.require_permission(identity, "read", record=record)

        # Prepare and execute the search
        params = params or {}

        search_result = self._search(
            "search_versions",
            identity,
            params,
            search_preference,
            record_cls=self.record_cls,
            search_opts=self.config.search_versions,
            extra_filter=dsl.Q(
                "term", **{"parent.id": str(record.parent.pid.pid_value)}
            ),
            permission_action="read",
            **kwargs
        ).execute()

    def _rebuild_index(self, indexer, model_cls):
        records = (
            db.session.query(model_cls.id)
            .filter(model_cls.is_deleted == False)
            .yield_per(1000)
        )
        for rec in records:
            try:
                indexer.bulk_index(rec.id)
            except Exception:
                pass


    def rebuild_index(self, identity, uow=None):
        """Reindex all records managed by this service.

        Note: Skips (soft) deleted records.
        """
        self._rebuild_index(self.indexer, self.record_cls.model_cls)
        self._rebuild_index(self.draft_indexer, self.draft_cls.model_cls)

        return True

#
# Record files
#
class Marc21RecordFilesService(FileService):
    """Marc21 record files service."""

    config_name = "MARC21_RECORDS_FILES_SERVICE_CONFIG"
    default_config = Marc21RecordFilesServiceConfig


#
# Draft files
#
class Marc21DraftFilesService(FileService):
    """Marc21 draft files service."""

    config_name = "MARC21_DRAFT_FILES_SERVICE_CONFIG"
    default_config = Marc21DraftFilesServiceConfig
