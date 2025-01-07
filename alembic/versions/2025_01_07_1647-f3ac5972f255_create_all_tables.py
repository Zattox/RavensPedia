"""create all tables

Revision ID: f3ac5972f255
Revises: 
Create Date: 2025-01-07 16:47:12.441841

"""

from typing import Sequence, Union

import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f3ac5972f255"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "matches",
        sa.Column("first_team_id", sa.Integer(), nullable=False),
        sa.Column("second_team_id", sa.Integer(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("tournament_id", sa.Integer(), nullable=False),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "matches_info",
        sa.Column("faceit_match_id", sa.String(), nullable=False),
        sa.Column("rounds", sa.PickleType(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "players",
        sa.Column("nickname", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("surname", sa.String(), nullable=False),
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column(
            "matches",
            sqlalchemy_utils.types.scalar_list.ScalarListType(),
            nullable=False,
        ),
        sa.Column(
            "tournaments",
            sqlalchemy_utils.types.scalar_list.ScalarListType(),
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "teams",
        sa.Column("team_name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column(
            "players",
            sqlalchemy_utils.types.scalar_list.ScalarListType(),
            nullable=False,
        ),
        sa.Column(
            "matches",
            sqlalchemy_utils.types.scalar_list.ScalarListType(),
            nullable=False,
        ),
        sa.Column(
            "tournaments",
            sqlalchemy_utils.types.scalar_list.ScalarListType(),
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "tournaments",
        sa.Column("tournament_name", sa.String(), nullable=False),
        sa.Column("prize", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column(
            "matches",
            sqlalchemy_utils.types.scalar_list.ScalarListType(),
            nullable=False,
        ),
        sa.Column(
            "teams", sqlalchemy_utils.types.scalar_list.ScalarListType(), nullable=False
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("tournaments")
    op.drop_table("teams")
    op.drop_table("players")
    op.drop_table("matches_info")
    op.drop_table("matches")
    # ### end Alembic commands ###