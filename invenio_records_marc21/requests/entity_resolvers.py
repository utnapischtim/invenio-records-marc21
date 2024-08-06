# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
# Copyright (C) 2023-2024 Graz University of Technology.
# Copyright (C) 2023 TU Wien.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Entity resolver for records aware of drafts and records."""


from invenio_access.permissions import system_identity
from invenio_pidstore.errors import PIDDoesNotExistError, PIDUnregistered
from invenio_records_resources.references.entity_resolvers import (
    RecordProxy,
    RecordResolver,
    ServiceResultProxy,
)
from sqlalchemy.orm.exc import NoResultFound

from ..records.api import Marc21Draft, Marc21Record
from ..services.config import Marc21RecordServiceConfig


class Marc21RecordProxy(RecordProxy):
    """Proxy for resolve Marc21Draft and Marc21Record."""

    def _get_record(self, pid_value):
        """Fetch the published record."""
        return Marc21Draft.pid.resolve(pid_value)

    def _resolve(self):
        """Resolve the Record from the proxy's reference dict."""
        pid_value = self._parse_ref_dict_id()

        draft = None
        try:
            draft = Marc21Draft.pid.resolve(pid_value, registered_only=False)
        except (PIDUnregistered, NoResultFound, PIDDoesNotExistError):
            # try checking if it is a published record before failing
            record = self._get_record(pid_value)
        else:
            # no exception raised. If published, get the published record instead
            record = draft if not draft.is_published else self._get_record(pid_value)

        return record

    def ghost_record(self, record):
        """Ghost reprensentation of a record.

        Drafts at the moment cannot be resolved, service.read_many() is searching on
        public records, thus the `ghost_record` method will always kick in!
        """
        return {"id": record}


class Marc21RecordResolver(RecordResolver):
    """RDM Record entity resolver."""

    type_id = "marcrecord"

    def __init__(self):
        """Initialize the resolver."""
        super().__init__(
            Marc21Draft,
            Marc21RecordServiceConfig.service_id,
            type_key=self.type_id,
            proxy_cls=Marc21RecordProxy,
        )

    def matches_entity(self, entity):
        """Check if the entity is a draft or a record."""
        return isinstance(entity, (Marc21Draft, Marc21Record))
