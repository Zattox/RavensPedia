"""Add fields in TableTournament

Revision ID: e77f13b7dbc6
Revises: ea4c8abd0373
Create Date: 2025-01-22 23:16:12.841371

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e77f13b7dbc6"
down_revision: Union[str, None] = "ea4c8abd0373"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "tournaments",
        sa.Column(
            "status",
            sa.Enum("SCHEDULED", "IN_PROGRESS", "COMPLETED", name="tournamentstatus"),
            server_default="SCHEDULED",
            nullable=False,
        ),
    )
    op.add_column(
        "tournaments",
        sa.Column(
            "start_date", sa.DateTime(), server_default="2025-01-01", nullable=False
        ),
    )
    op.add_column(
        "tournaments",
        sa.Column(
            "end_date", sa.DateTime(), server_default="2025-02-01", nullable=False
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("tournaments", "end_date")
    op.drop_column("tournaments", "start_date")
    op.drop_column("tournaments", "status")
    # ### end Alembic commands ###
