# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 TU Wien.
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Protection class for the access system field."""


class Protection:
    """Protection class for the access system field."""

    def __init__(self, metadata="public", files="public"):
        """Create a new protection levels instance."""
        self.set(metadata=metadata, files=files)

    def _validate_protection_level(self, level):
        return level in ("public", "embargoed", "restricted")

    @property
    def metadata(self):
        """Get the record's overall protection level."""
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        """Set the record's overall protection level."""
        if not self._validate_protection_level(value):
            raise ValueError("unknown metadata protection level: {}".format(value))

        if value == "restricted":
            self._files = "restricted"

        self._metadata = value

    @property
    def files(self):
        """Get the record's files protection level."""
        return self._files

    @files.setter
    def files(self, value):
        """Set the record's files protection level."""
        if not self._validate_protection_level(value):
            raise ValueError("unknown files protection level: {}".format(value))

        if self.metadata == "restricted":
            self._files = "restricted"
        else:
            self._files = value

    def set(self, metadata, files=None):
        """Set the protection level for record and files."""
        self.metadata = metadata
        if files is not None:
            self.files = files

    def __get__(self):
        """Get the protection level of the record and its files."""
        return {
            "metadata": self.metadata,
            "files": self.files,
        }

    def __repr__(self):
        """Return repr(self)."""
        return "<{} (metadata: {}, files: {})>".format(
            type(self).__name__,
            self.metadata,
            self.files,
        )
