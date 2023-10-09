"""create messages table

Revision ID: 41fb9eb8bce1
Revises:
Create Date: 2023-10-09 13:49:20.194076

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "41fb9eb8bce1"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "messages",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("content", sa.String),
    )


def downgrade() -> None:
    op.drop_table("messages")
