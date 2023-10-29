"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
	with open("${up_revision}_upgrades.sql") as file_:
		for statement in file_.read().split(";\n"):  # or however we want to split
		    op.execute(statement)


def downgrade():
	with open("${up_revision}_downgrades.sql") as file_:
		for statement in file_.read().split(";\n"):  # or however we want to split
		    op.execute(statement)
