"""add made_at column to posts table

Revision ID: a451037a2934
Revises: ffc008de5eb6
Create Date: 2023-12-23 01:38:08.757462

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a451037a2934'
down_revision: Union[str, None] = 'ffc008de5eb6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("made_at", sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "made_at")
    pass
