"""create initial tables

Revision ID: aebb6827d602
Revises: 
Create Date: 2023-10-29 10:27:30.934740

"""
import os

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "aebb6827d602"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with open("./migrations/versions/aebb6827d602_upgrades.sql") as file_:
        for statement in file_.read().split(";\n"):  # or however we want to split
            op.execute(statement)


def downgrade():
    with open("./migrations/versions/aebb6827d602_downgrades.sql") as file_:
        for statement in file_.read().split(";\n"):  # or however we want to split
            op.execute(statement)
