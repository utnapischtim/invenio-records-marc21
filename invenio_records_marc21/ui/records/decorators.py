# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2021 CERN.
# Copyright (C) 2019-2021 Northwestern University.
# Copyright (C)      2021 TU Wien.
# Copyright (C)      2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Routes for record-related pages provided by Invenio-Records-Marc21."""

from functools import wraps

from flask import g
from invenio_records_resources.services.errors import PermissionDeniedError

from ...proxies import current_records_marc21


def links_config():
    """Get the record links config."""
    return current_records_marc21.record_resource.config.links_config


def draft_links_config():
    """Get the drafts links config."""
    return current_records_marc21.record_resource.config.draft_links_config


def service():
    """Get the record service."""
    return current_records_marc21.records_service


def pass_record_or_draft(f):
    """Decorate to retrieve the record or draft using the record service."""

    @wraps(f)
    def view(**kwargs):
        pid_value = kwargs.get("pid_value")
        is_preview = kwargs.get("is_preview")

        def get_record():
            """Retrieve record."""
            return service().read(id_=pid_value, identity=g.identity)

        if is_preview:
            try:
                record = service().read_draft(id_=pid_value, identity=g.identity)
            except NoResultFound:
                record = get_record()
        else:
            record = get_record()
        kwargs["record"] = record
        return f(**kwargs)

    return view


def pass_draft(f):
    """Decorator to retrieve the draft using the record service."""

    @wraps(f)
    def view(**kwargs):
        pid_value = kwargs.get("pid_value")
        draft = service().read_draft(id_=pid_value, identity=g.identity)
        draft._record.relations.dereference()
        kwargs["draft"] = draft
        return f(**kwargs)

    return view


def user_permissions(actions=[]):
    """Decorate a view to pass user's permissions for the provided actions.

    :param actions: The action list to check permissions against.
    """

    def _wrapper_func(f):
        @wraps(f)
        def view(**kwargs):
            action_args = {}
            if "record" in kwargs:
                action_args["record"] = kwargs["record"]._record
            elif "draft" in kwargs:
                action_args["record"] = kwargs["draft"]._record
            permissions = {}
            for action in actions:
                action_can = (
                    service()
                    .permission_policy(action, **action_args)
                    .allows(g.identity)
                )
                permissions[f"can_{action}"] = action_can
            kwargs["permissions"] = permissions
            return f(**kwargs)

        return view

    return _wrapper_func
