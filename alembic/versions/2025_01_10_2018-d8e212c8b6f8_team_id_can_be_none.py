"""Team_id can be None

Revision ID: d8e212c8b6f8
Revises: 110623a4ccd8
Create Date: 2025-01-10 20:18:34.406329

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d8e212c8b6f8"
down_revision: Union[str, None] = "110623a4ccd8"
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
        sa.Column("team_id", sa.Integer(), nullable=True),
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
