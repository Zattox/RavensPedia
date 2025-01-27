"""Add constants for max number of teams and players

Revision ID: ecb0211fe58b
Revises: d8e212c8b6f8
Create Date: 2025-01-10 22:30:54.631880

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ecb0211fe58b"
down_revision: Union[str, None] = "d8e212c8b6f8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("matches")
    op.create_table(
        "matches",
        sa.Column("max_number_of_teams", sa.Integer(), nullable=False),
        sa.Column("max_number_of_players", sa.Integer(), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("tournament_id", sa.Integer(), nullable=False),
        sa.Column(
            "date",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["tournament_id"],
            ["tournaments.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("matches")
    op.create_table(
        "matches",
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("tournament_id", sa.Integer(), nullable=False),
        sa.Column(
            "date",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["tournament_id"],
            ["tournaments.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###
