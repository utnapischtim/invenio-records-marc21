# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Marc21 Record Service."""


from invenio_drafts_resources.services.records import RecordService
from invenio_records_resources.services.files.service import FileService
from invenio_records_resources.services.records.results import RecordItem

from ..records.systemfields.access import AccessStatusEnum
from .config import (
    Marc21DraftFilesServiceConfig,
    Marc21RecordFilesServiceConfig,
    Marc21RecordServiceConfig,
)
from .record import Marc21Metadata


class Marc21RecordService(RecordService):
    """Marc21 record service."""

    config_name = "MARC21_RECORDS_SERVICE_CONFIG"
    default_config = Marc21RecordServiceConfig

    def _create_data(self, identity, data, metadata, access=None):
        """Create a data json.

        :param identity: Identity of user creating the record.
        :param Metadata metadata: Input data according to the metadata schema.
        :param dict access: provide access additional information
        :return data: marc21 record data
        """
        if data is None:
            data = {"metadata": {"xml": metadata.xml, "json": metadata.json}}
        if "access" not in data:
            default_access = {
                "access": {
                    "owned_by": [{"user": identity.id}],
                    "metadata": AccessStatusEnum.PUBLIC.value,
                    "files": AccessStatusEnum.PUBLIC.value,
                },
            }
            if access is not None:
                default_access["access"].update(access)
            data.update(default_access)
        return data

    def create(
        self, identity, data=None, metadata=Marc21Metadata(), access=None
    ) -> RecordItem:
        """Create a draft record.

        :param identity: Identity of user creating the record.
        :param dict data: Input data according to the data schema.
        :param Metadata metadata: Input data according to the metadata schema.
        :param links_config: Links configuration.
        :param dict access: provide access additional information
        """
        data = self._create_data(identity, data, metadata, access)
        return super().create(identity, data)

    def update_draft(
        self,
        id_,
        identity,
        data=None,
        metadata=Marc21Metadata(),
        revision_id=None,
        access=None,
    ):
        """Update a draft record.

        :param identity: Identity of user creating the record.
        :param dict data: Input data according to the data schema.
        :param Metadata metadata: Input data according to the metadata schema.
        :param links_config: Links configuration.
        :param dict access: provide access additional information
        """
        data = self._create_data(identity, data, metadata, access)
        return super().update_draft(id_, identity, data, revision_id)


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
