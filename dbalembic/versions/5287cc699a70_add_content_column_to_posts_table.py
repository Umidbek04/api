"""add content column to posts table

Revision ID: 5287cc699a70
Revises: 1e4171fc1bec
Create Date: 2023-12-23 00:52:59.411724

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5287cc699a70'
down_revision: Union[str, None] = '1e4171fc1bec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(100), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
