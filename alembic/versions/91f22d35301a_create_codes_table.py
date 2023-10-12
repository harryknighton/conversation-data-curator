"""create codes table

Revision ID: 91f22d35301a
Revises: 41fb9eb8bce1
Create Date: 2023-10-12 13:36:41.613095

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "91f22d35301a"
down_revision: Union[str, None] = "41fb9eb8bce1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "codes",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("code", sa.String, unique=True),
    )


def downgrade() -> None:
    op.drop_table("codes")
