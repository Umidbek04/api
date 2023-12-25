"""add users table

Revision ID: b72d4f5bf966
Revises: 5287cc699a70
Create Date: 2023-12-23 01:03:07.748067

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b72d4f5bf966'
down_revision: Union[str, None] = '5287cc699a70'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer, nullable=False),
                    sa.Column('email', sa.String(100), nullable=False),
                    sa.Column('password', sa.Integer, nullable=False),
                    sa.Column('made_at', sa.TIMESTAMP(timezone=True), 
                              server_default=sa.text('now()'), nullable=False),

                              sa.PrimaryKeyConstraint('id'),
                              sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
