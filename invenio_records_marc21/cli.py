# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Command-line tools for demo module."""
import datetime
import random
import uuid

import click
from edtf.parser.grammar import level0Expression
from faker import Faker
from flask.cli import with_appcontext
from flask_principal import Identity
from invenio_access import any_user
from invenio_db import db
from invenio_indexer.api import RecordIndexer
from invenio_pidstore import current_pidstore
from invenio_search import current_search

from .services import Marc21RecordService
from .vocabularies import Vocabularies


def fake_access_right():
    """Generates a fake resource_type."""
    vocabulary = Vocabularies.get_vocabulary("access_right")
    _type = random.choice(list(vocabulary.data.keys()))
    return _type


def create_fake_record():
    """Create records for demo purposes."""
    fake = Faker()
    data_to_use = {
        "access": {
            "metadata": False,
            "files": False,
            "owned_by": [1],
            "access_right": fake_access_right(),
            "embargo_date": fake.future_date(end_date="+1y").strftime("%Y-%m-%d"),
        },
        "metadata": {
            "ref": "reference to marc21 schema",
            "record": "<record> \
            <controlfield tag='001'>990079940640203331</controlfield> \
            <controlfield tag='003'>AT-OBV</controlfield> \
            <controlfield tag='005'>20170703041800.0</controlfield> \
            <controlfield tag='007'>cr</controlfield> \
            <controlfield tag='008'>100504|1932</controlfield> \
            <controlfield tag='009'>AC08088803</controlfield> \
            <datafield tag='035' ind1=' ' ind2=' '> \
            <subfield code='a'>AC08088803</subfield> \
            </datafield> \
            <datafield tag='035' ind1=' ' ind2=' '> \
            <subfield code='a'>(AT-OBV)AC08088803</subfield> \
            <subfield code='a'>(Aleph)007994064ACC01</subfield> \
            <subfield code='a'>(DE-599)OBVAC08088803</subfield> \
            </datafield> \
            <datafield tag='245' ind1='0' ind2='0'> \
		    <subfield code='a'>&lt;&lt;Die&gt;&gt; Internationale Werkbundsiedlung Wien 1932</subfield> \
		    <subfield code='c'>hrsg. von Josef Frank</subfield> \
	        </datafield> \
	        <datafield tag='264' ind1=' ' ind2='55'> \
            <subfield code='a'>Wien</subfield>\
            <subfield code='b'>Schroll</subfield> \
            <subfield code='c'>1932</subfield>\
	        </datafield>\
            </record>"
        },
    }

    # identity providing `any_user` system role
    identity = Identity(1)
    identity.provides.add(any_user)

    service = Marc21RecordService()

    draft = service.create(data=data_to_use, identity=identity)

    record = service.publish(id_=draft.id, identity=identity)

    return record


@click.group()
def marc21():
    """InvenioMarc21 records commands."""
    pass


@marc21.command("demo")
@with_appcontext
def demo():
    """Create 10 fake records for demo purposes."""
    click.secho("Creating demo records...", fg="blue")

    for _ in range(10):
        create_fake_record()

    click.secho("Created records!", fg="green")
