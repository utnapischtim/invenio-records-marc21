# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""DataCite Serializers for Invenio Marc21 Records."""

from flask_resources.serializers import JSONSerializer, MarshmallowSerializer

from .schema import Marc21DataCite43Schema


class Marc21DataCite43JSONSerializer(MarshmallowSerializer):
    """Marshmallow based DataCite serializer for records."""

    def __init__(self) -> None:
        """Constructor."""
        super().__init__(
            format_serializer_cls=JSONSerializer,
            object_schema_cls=Marc21DataCite43Schema,
        )

    # TODO: Remove when invenio_rdm_records.services.pids.providers.datacite.DataCitePIDProvider
    # uses the new MarshmallowSerializer class
    def dump_one(self, obj: dict) -> dict:
        """Dump the object with extra information."""
        return self.dump_obj(obj)
