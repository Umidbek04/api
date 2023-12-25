"""make posts table

Revision ID: 1e4171fc1bec
Revises: 
Create Date: 2023-12-23 00:30:33.492438

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e4171fc1bec'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts",
                    sa.Column('id', sa.Integer(), primary_key=True),
                    sa.Column('title', sa.String(100), nullable=False),
                    sa.Column('published', sa.Boolean, nullable=False))


def downgrade() -> None:
    op.drop_table('posts')
