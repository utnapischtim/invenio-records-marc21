# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2024 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Create Marc21 Tables."""

import sqlalchemy as sa
from alembic import op
from sqlalchemy_utils import UUIDType

# revision identifiers, used by Alembic.
revision = "8025c60c8465"
down_revision = "ed55fea7131e"
branch_labels = ()
depends_on = None


def upgrade():
    """Upgrade database."""
    op.create_table(
        "marc21_parents_community",
        sa.Column("community_id", UUIDType(), nullable=False),
        sa.Column("record_id", UUIDType(), nullable=False),
        sa.Column("request_id", UUIDType(), nullable=True),
        sa.ForeignKeyConstraint(
            ["community_id"],
            ["communities_metadata.id"],
            name=op.f("fk_marc21_parents_community_community_id_communities_metadata"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["record_id"],
            ["marc21_parents_metadata.id"],
            name=op.f("fk_r_parents_community_record_id_marc21_parents_metadata"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["request_id"],
            ["request_metadata.id"],
            name=op.f("fk_marc21_parents_community_request_id_request_metadata"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint(
            "community_id", "record_id", name=op.f("pk_marc21_parents_community")
        ),
    )


def downgrade():
    """Downgrade database."""
    op.drop_table("marc21_parents_community")
