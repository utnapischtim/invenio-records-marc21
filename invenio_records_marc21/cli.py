# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Command-line tools for demo module."""

import json
import random
from datetime import timedelta
from os.path import dirname, join

import arrow
import click
from flask.cli import with_appcontext
from flask_principal import Identity
from invenio_access import any_user

from .errors import log_exceptions
from .proxies import current_records_marc21
from .records.systemfields.access import AccessStatusEnum
from .services.record import Marc21Metadata


def system_identity():
    """System identity."""
    identity = Identity(1)
    identity.provides.add(any_user)
    return identity


def fake_access_right():
    """Generates a fake access_right."""
    _type = random.choice(list(AccessStatusEnum)).value
    return _type


def fake_feature_date(days=365):
    """Generates a fake feature_date."""
    start_date = arrow.utcnow().datetime
    random_number_of_days = random.randrange(1, days)
    _date = start_date + timedelta(days=random_number_of_days)
    return _date.strftime("%Y-%m-%d")


def _load_file(filename):
    with open(join(dirname(__file__), filename), "rb") as fp:
        input = fp.read()
        return input.decode("utf-8")


def _load_json(filename):
    with open(join(dirname(__file__), filename), "rb") as fp:
        return json.load(fp)


def create_fake_metadata(filename):
    """Create records for demo purposes."""
    metadata = Marc21Metadata()
    metadata.xml = _load_file(filename)
    metadata_access = fake_access_right()
    data_acces = {
        "owned_by": [{"user": system_identity().id}],
        "files": "public",
        "metadata": metadata_access,
    }
    if metadata_access == AccessStatusEnum.EMBARGOED.value:
        embargo = {
            "embargo": {
                "until": fake_feature_date(),
                "active": True,
                "reason": "Because I can!",
            }
        }
        data_acces.update(embargo)

    service = current_records_marc21.records_service
    draft = service.create(
        metadata=metadata,
        identity=system_identity(),
        access=data_acces,
    )

    record = service.publish(id_=draft.id, identity=system_identity())

    return record


def create_fake_record(filename):
    """Create records for demo purposes."""
    data_to_use = _load_json(filename)
    metadata_access = fake_access_right()
    data_acces = {
        "owned_by": [{"user": system_identity().id}],
        "files": AccessStatusEnum.PUBLIC.value,
        "metadata": metadata_access,
    }
    if metadata_access == AccessStatusEnum.EMBARGOED.value:
        data_acces.update({"embargo_date": fake_feature_date()})

    service = current_records_marc21.records_service

    draft = service.create(
        data=data_to_use, identity=system_identity(), access=data_acces
    )

    record = service.publish(id_=draft.id, identity=system_identity())

    return record


@click.group()
def marc21():
    """InvenioMarc21 records commands."""
    pass


@marc21.command("demo")
@with_appcontext
@click.option(
    "--number",
    "-n",
    default=10,
    show_default=True,
    type=int,
    help="Number of records will be created.",
)
@click.option(
    "--file",
    "-f",
    default="data/fake-metadata.xml",
    show_default=True,
    type=str,
    help="Relative path to file",
)
@click.option(
    "--metadata-only",
    "-m",
    default="True",
    type=bool,
    help="Provided metadata only in file",
)
@with_appcontext
@log_exceptions
def demo(number, file, metadata_only):
    """Create number of fake records for demo purposes."""
    click.secho("Creating demo records...", fg="blue")
    for _ in range(number):
        if metadata_only:
            create_fake_metadata(file)
        else:
            create_fake_record(file)

    click.secho("Created records!", fg="green")
