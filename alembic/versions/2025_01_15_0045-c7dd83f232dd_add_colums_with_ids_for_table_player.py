"""Add colums with ids for table_player

Revision ID: c7dd83f232dd
Revises: 7a487de501ea
Create Date: 2025-01-15 00:45:32.486804

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c7dd83f232dd"
down_revision: Union[str, None] = "7a487de501ea"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("players")
    op.create_table(
        "players",
        sa.Column("nickname", sa.String(length=12), nullable=False),
        sa.Column("name", sa.String(length=15), nullable=True),
        sa.Column("surname", sa.String(length=30), nullable=True),
        sa.Column("steam_id", sa.String(), nullable=False),
        sa.Column("faceit_id", sa.String(), nullable=True),
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["teams.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nickname"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("players")
    op.create_table(
        "players",
        sa.Column("nickname", sa.String(length=12), nullable=False),
        sa.Column("name", sa.String(length=15), nullable=True),
        sa.Column("surname", sa.String(length=30), nullable=True),
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["teams.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nickname"),
    )
    # ### end Alembic commands ###
