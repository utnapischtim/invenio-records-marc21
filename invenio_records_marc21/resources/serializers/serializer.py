# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2022 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 record response serializers."""

import json
from xml.etree.ElementTree import tostring

from flask_resources.serializers import JSONSerializer, MarshmallowSerializer

from .schema import Marc21Schema


class Marc21XMLMixin:
    """Marc21 XML converter class."""

    controlfields = [
        "001",
        "003",
        "005",
        "006",
        "007",
        "008",
        "009",
    ]

    def convert_metadata(self, data, root=False):
        """Convert the metadata to Marc21 xml."""
        fields = []
        for key, value in data.get("fields").items():
            if key in self.controlfields:
                fields.append(
                    {"id": key, "ind1": None, "ind2": None, "subfield": value}
                )
            else:
                for field in value:
                    subfield = [
                        f"$${key} {' '.join(value)}"
                        for key, value in field["subfields"].items()
                    ]
                    fields.append(
                        {
                            "id": key,
                            "ind1": field["ind1"],
                            "ind2": field["ind2"],
                            "subfield": " ".join(subfield),
                        }
                    )

        return {"fields": fields, "leader": data.get("leader", "")}


class Marc21BASESerializer(MarshmallowSerializer):
    """Marc21 Base serializer implementation."""

    def __init__(
        self,
        format_serializer_cls=JSONSerializer,
        object_schema_cls=Marc21Schema,
        **options,
    ):
        """Marc21 Base Serializer Constructor.

        :param schema_cls: Default Marc21Schema
        :param options: Json encoding options.
        """
        super().__init__(
            format_serializer_cls=format_serializer_cls,
            object_schema_cls=object_schema_cls,
            **options,
        )

    def dump_obj(self, obj):
        """Dump the object into a JSON string."""
        return self.object_schema_cls().dump(obj)

    def dump_list(self, obj_list):
        """Serialize a list of records.

        :param obj_list: List of records instance.
        """
        records = obj_list["hits"]["hits"]
        obj_list["hits"]["hits"] = [self.dump_obj(obj) for obj in records]
        return obj_list


class Marc21JSONSerializer(Marc21BASESerializer):
    """Marc21 JSON export serializer implementation."""

    def serialize_object_list(self, obj_list):
        """Serialize a list of records.

        :param records: List of records instance.
        """
        obj_list = self.dump_list(obj_list)
        return json.dumps(obj_list, cls=self.format_serializer_cls.encoder)


class Marc21XMLSerializer(Marc21BASESerializer, Marc21XMLMixin):
    """Marc21 XML export serializer implementation."""

    def dump_obj(self, obj):
        """Serialize a single record.

        :param record: Record instance.
        """
        return self.convert_metadata(super().dump_obj(obj))

    def serialize_object(self, obj):
        """Serialize a single record.

        :param record: Record instance.
        """
        return self.dump_obj(obj)

    def serialize_object_list(self, obj_list):
        """Dump the object list into a JSON string."""
        list = []
        for obj in obj_list["hits"]["hits"]:
            list.append(self.serialize_object(obj))

        return "\n".join(list)
