# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 TU Wien.
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Access system field."""

from invenio_records.systemfields import SystemField

from ..owners import Owners


class ParentRecordAccess:
    """Access management for all versions of a record."""

    owners_cls = Owners

    def __init__(
        self,
        owned_by=None,
        owners_cls=None,
    ):
        """Create a new Access object for a record.

        If ``owned_by`` are not specified,
        a new instance of ``owners_cls``
        will be used, respectively.
        :param owned_by: The set of record owners
        """
        owners_cls = owners_cls or ParentRecordAccess.owners_cls
        self.owned_by = owned_by if owned_by else owners_cls()
        self.errors = []

    @property
    def owners(self):
        """An alias for the owned_by property."""
        return self.owned_by

    def dump(self):
        """Dump the field values as dictionary."""
        access = {
            "owned_by": self.owned_by.dump(),
        }

        return access

    def refresh_from_dict(self, access_dict):
        """Re-initialize the Access object with the data in the access_dict."""
        new_access = self.from_dict(access_dict)
        self.errors = new_access.errors
        self.owned_by = new_access.owned_by

    @classmethod
    def from_dict(
        cls,
        access_dict,
        owners_cls=None,
    ):
        """Create a new Access object from the specified 'access' property.

        The new ``ParentRecordAccess`` object will be populated with new
        instances from the configured classes.
        If ``access_dict`` is empty, the ``ParentRecordAccess`` object will
        be populated with new instances of ``owners_cls``.
        """
        owners_cls = owners_cls or cls.owners_cls
        errors = []

        owners = owners_cls()

        if access_dict:
            for owner_dict in access_dict.get("owned_by", []):
                try:
                    owners.add(owners.owner_cls(owner_dict))
                except Exception as e:
                    errors.append(e)

        access = cls(
            owned_by=owners,
        )
        access.errors = errors
        return access

    def __repr__(self):
        """Return repr(self)."""
        return ("<{} (owners: {})>").format(
            type(self).__name__,
            len(self.owners or []),
        )


class ParentRecordAccessField(SystemField):
    """System field for managing record access."""

    def __init__(self, key="access", access_obj_class=ParentRecordAccess):
        """Create a new ParentRecordAccessField instance."""
        self._access_obj_class = access_obj_class
        super().__init__(key=key)

    def obj(self, instance):
        """Get the access object."""
        data = self.get_dictkey(instance)
        obj = self._get_cache(instance)
        if obj is not None and data is None:
            return obj

        if data:
            obj = self._access_obj_class.from_dict(data)
        else:
            obj = self._access_obj_class()

        self._set_cache(instance, obj)
        return obj

    def set_obj(self, record, obj):
        """Set the access object."""
        if isinstance(obj, dict):
            obj = self._access_obj_class.from_dict(obj)

        assert isinstance(obj, self._access_obj_class)

        self._set_cache(record, obj)

    def __get__(self, record, owner=None):
        """Get the record's access object."""
        if record is None:
            return self

        return self.obj(record)

    def __set__(self, record, obj):
        """Set the records access object."""
        self.set_obj(record, obj)

    def pre_commit(self, record):
        """Dump the configured values before the record is committed."""
        obj = self.obj(record)
        if obj is not None:
            record["access"] = obj.dump()
