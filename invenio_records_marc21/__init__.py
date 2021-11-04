# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio-Records-Marc21 datamodel.

This guide will show you how to get started with
Invenio-Records-Marc21. It assumes that you already have knowledge of
Flask applications and Invenio modules.

It will then explain key topics and concepts of this module.

Getting started
---------------

You will learn how to create a new Marc21 records, upload a File and accosiate with the record
using the programmatic APIs of Invenio-Records-Marc21.


This is the initial configuration needed to have things running:

:py:data:`invenio_records_marc21.config`


Service operations
------------------

Creation
~~~~~~~~


Let's **create** a very simple record:

>>> from flask import Flask, g
>>> app = Flask(__name__)

>>> from invenio_records_marc21 import InvenioRecordsMARC21
>>> ext = InvenioRecordsMARC21(app)

>>> from invenio_records_marc21.proxies import current_records_marc21
>>> service = current_records_marc21.record_resource
>>> draft = service.create(identity=g.identity,data={"metadata": {"title": "The title of the record"}})


A new row has been added to the database, in the table ``marc21_drafts_metadata``:
this corresponds to the record metadata, first version (version 1).


Publish
~~~~~~~~


Let's **publish** our very simple record:


>>> record = service.publish(identity=g.identity,id_=draft.id)

A new row has been added to the database, in the table ``marc21_records_metadata``:
this corresponds to the record metadata, second version (version 2). The created
Draft from before has been deleted.


Service Advanced
----------------

The Invenio-Records-Marc21 service provides advanced Record creation functionality.

>>> def create(self, identity, data=None, metadata=Marc21Metadata(), files=False, access=None) -> RecordItem:

    :data: Input data according to the data schema.
    :metadata: Input data according to the metadata schema.
    :files: enable/disable file support for the record.
    :access: provide access additional information

The api does not only takes  a json like object e.q. `data`. The Records can be created with only the metadata.

Marc21Metadata
~~~~~~~~~~~~~~

>>> from invenio_records_marc21.services.record import Marc21Metadata
>>> metadata = Marc21Metadata()
>>> metadata.emplace_field(tag="245", ind1="1", ind2="0", value="nulla sunt laborum")

or set a whole Marc21 xml string

>>> metadata.xml = "<record><leader>00000nam a2200000zca4500</leader></record>"

Access
~~~~~~

The access dict structure required for Invenio-Records-Marc21 records:

>>> access = {
...     "record": "open/restricted",
...     "files": "open/restricted",
...     "embargo": {
...         "active": True/False,
...         "until": "YYYY-MM-DD",
...         "reason": "Reason",
...    }
... }

See :doc:`api` for extensive API documentation.

"""

from __future__ import absolute_import, print_function

from .ext import InvenioRecordsMARC21
from .proxies import current_records_marc21
from .version import __version__

__all__ = (
    "__version__",
    "InvenioRecordsMARC21",
    "current_records_marc21",
)
