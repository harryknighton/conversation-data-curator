"""create annotations relationship

Revision ID: 997b8a992b91
Revises: 91f22d35301a
Create Date: 2023-10-12 23:45:25.544437

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "997b8a992b91"
down_revision: Union[str, None] = "91f22d35301a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "annotations",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("message_id", sa.Integer, sa.ForeignKey("messages.id")),
        sa.Column("code_id", sa.Integer, sa.ForeignKey("codes.id")),
        sa.Column("start_idx", sa.Integer),
        sa.Column("end_idx", sa.Integer),
    )


def downgrade() -> None:
    op.drop_table("annotations")
