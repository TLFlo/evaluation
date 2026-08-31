"""add statut to examen

Revision ID: fe903aa20b95
Revises: 49b1499e12f5
Create Date: 2026-08-31 05:27:36.669223

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "fe903aa20b95"
down_revision: Union[str, Sequence[str], None] = "49b1499e12f5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    statut_enum = postgresql.ENUM(
        "PROGRAMMEE", "PUBLIEE", "TERMINEE", name="statutexamen"
    )

    statut_enum.create(op.get_bind(), checkfirst=True)

    op.add_column("examen", sa.Column("statut", statut_enum, nullable=True))


def downgrade() -> None:
    op.drop_column("examen", "statut")

    statut_enum = postgresql.ENUM(
        "PROGRAMMEE", "PUBLIEE", "TERMINEE", name="statutexamen"
    )

    statut_enum.drop(op.get_bind(), checkfirst=True)
