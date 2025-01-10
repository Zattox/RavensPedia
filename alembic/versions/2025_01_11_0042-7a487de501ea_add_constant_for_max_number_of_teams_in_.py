"""Add constant for max number of teams in tournament

Revision ID: 7a487de501ea
Revises: 853f042101cd
Create Date: 2025-01-11 00:42:51.920122

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7a487de501ea"
down_revision: Union[str, None] = "853f042101cd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("tournaments")
    op.create_table(
        "tournaments",
        sa.Column("max_count_of_teams", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("prize", sa.String(length=50), nullable=True),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("tournaments")
    op.create_table(
        "tournaments",
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("prize", sa.String(length=50), nullable=True),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    # ### end Alembic commands ###
