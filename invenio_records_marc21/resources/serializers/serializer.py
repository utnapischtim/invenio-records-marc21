# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 record response serializers."""

import json

from dojson._compat import iteritems, string_types
from dojson.contrib.to_marc21 import to_marc21
from dojson.contrib.to_marc21.utils import MARC21_NS
from dojson.utils import GroupableOrderedDict
from flask_resources.serializers import MarshmallowJSONSerializer
from lxml import etree
from lxml.builder import E, ElementMaker

from .schema import Marc21Schema


class Marc21BASESerializer(MarshmallowJSONSerializer):
    """Marc21 Base serializer implementation."""

    def __init__(self, schema_cls=Marc21Schema, **options):
        """Marc21 Base Serializer Constructor.

        :param schema_cls: Default Marc21Schema
        :param options: Json encoding options.
        """
        super().__init__(schema_cls=schema_cls, **options)

    def dump_one(self, obj):
        """Dump the object into a JSON string."""
        return self._schema_cls(context=self.ctx).dump(obj)

    def dump_many(self, obj_list):
        """Serialize a list of records.

        :param obj_list: List of records instance.
        """
        records = obj_list["hits"]["hits"]
        obj_list["hits"]["hits"] = [self.dump_one(obj) for obj in records]
        return obj_list


class Marc21JSONSerializer(Marc21BASESerializer):
    """Marc21 JSON export serializer implementation."""

    ctx = {
        "remove_order": True,
    }

    def serialize_object_list(self, obj_list):
        """Serialize a list of records.

        :param records: List of records instance.
        """
        obj_list = self.dump_many(obj_list)
        return json.dumps(obj_list, cls=self.encoder, **self.dumps_options)


class Marc21XMLSerializer(Marc21BASESerializer):
    """Marc21 XML export serializer implementation."""

    ctx = {
        "remove_order": False,
    }

    def serialize_object(self, obj):
        """Serialize a single record.

        :param record: Record instance.
        """
        return self.convert_record(self.dump_one(obj))

    def serialize_object_list(self, obj_list):
        """Dump the object list into a JSON string."""
        list = []
        for obj in obj_list["hits"]["hits"]:
            list.append(self.serialize_object(obj))

        return "\n".join(list)

    def _convert(self, key, data):
        root = etree.Element(key)
        if isinstance(data, dict):
            for k, v in data.items():
                root.append(self._convert(k, v))
        elif isinstance(data, (list, tuple)):
            for item in data:
                root.append(self._convert(key, item))
        else:
            root.text = str(data)
        return root

    def convert_record(self, data):
        """Convert marc21 record to xml."""
        E = ElementMaker(namespace=MARC21_NS, nsmap={"prefix": MARC21_NS})
        record = E.record()
        for key, value in data.items():
            if "metadata" in key:
                record.append(self.convert_metadata(to_marc21.do(value["json"])))
                continue
            record.append(self._convert(key, value))
        return etree.tostring(
            record,
            pretty_print=True,
            xml_declaration=True,
            encoding="UTF-8",
        ).decode("UTF-8")

    def convert_metadata(self, data):
        """Convert the metadata to Marc21 xml."""
        rec = E.metadata()

        leader = data.get("leader")
        if leader:
            rec.append(E.leader(leader))

        if isinstance(data, GroupableOrderedDict):
            items = data.iteritems(with_order=False, repeated=True)
        else:
            items = iteritems(data)

        for df, subfields in items:
            # Control fields
            if len(df) == 3:
                if isinstance(subfields, string_types):
                    controlfield = E.controlfield(subfields)
                    controlfield.attrib["tag"] = df[0:3]
                    rec.append(controlfield)
                elif isinstance(subfields, (list, tuple, set)):
                    for subfield in subfields:
                        controlfield = E.controlfield(subfield)
                        controlfield.attrib["tag"] = df[0:3]
                        rec.append(controlfield)
            else:
                # Skip leader.
                if df == "leader":
                    continue

                if not isinstance(subfields, (list, tuple, set)):
                    subfields = (subfields,)

                df = df.replace("_", " ")
                for subfield in subfields:
                    if not isinstance(subfield, (list, tuple, set)):
                        subfield = [subfield]

                    for s in subfield:
                        datafield = E.datafield()
                        datafield.attrib["tag"] = df[0:3]
                        datafield.attrib["ind1"] = df[3]
                        datafield.attrib["ind2"] = df[4]

                        if isinstance(s, GroupableOrderedDict):
                            items = s.iteritems(with_order=False, repeated=True)
                        elif isinstance(s, dict):
                            items = iteritems(s)
                        else:
                            datafield.append(E.subfield(s))

                            items = tuple()

                        for code, value in items:
                            if not isinstance(value, string_types):
                                for v in value:
                                    datafield.append(E.subfield(v, code=code))
                            else:
                                datafield.append(E.subfield(value, code=code))

                        rec.append(datafield)
        return rec
