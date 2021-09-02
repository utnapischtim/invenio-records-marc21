# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Routes for record-related pages provided by Invenio-App-RDM."""

from flask import abort, current_app, render_template
from invenio_base.utils import obj_or_import_string

from ...resources.serializers.ui import Marc21UIJSONSerializer
from .decorators import pass_record, user_permissions


#
# Views
#
@pass_record
@user_permissions(actions=["update_draft"])
def record_detail(record=None, files=None, pid_value=None, permissions=None):
    """Record detail page (aka landing page)."""
    files_dict = None if files is None else files.to_dict()
    return render_template(
        "invenio_records_marc21/record.html",
        record=Marc21UIJSONSerializer().dump_one(record.to_dict()),
        pid=pid_value,
        files=files_dict,
        permissions=permissions,
    )


@pass_record
def record_export(record=None, export_format=None, pid_value=None, permissions=None):
    """Export marc21 record page view."""
    exporter = current_app.config.get("INVENIO_MARC21_RECORD_EXPORTERS", {}).get(
        export_format
    )
    if exporter is None:
        abort(404)

    options = current_app.config.get(
        "INVENIO_MARC21_RECORD_EXPORTER_OPTIONS",
        {
            "indent": 2,
            "sort_keys": True,
        },
    )

    serializer = obj_or_import_string(exporter["serializer"])(options=options)
    exported_record = serializer.serialize_object(record.to_dict())

    return render_template(
        "invenio_records_marc21/records/export.html",
        export_format=exporter.get("name", export_format),
        exported_record=exported_record,
        record=Marc21UIJSONSerializer().dump_one(record.to_dict()),
        permissions=permissions,
    )
