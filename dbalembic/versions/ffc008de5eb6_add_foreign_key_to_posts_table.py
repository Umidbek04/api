"""add foreign key to posts table

Revision ID: ffc008de5eb6
Revises: b72d4f5bf966
Create Date: 2023-12-23 01:28:52.527496

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ffc008de5eb6'
down_revision: Union[str, None] = 'b72d4f5bf966'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer, nullable=False))
    op.create_foreign_key("posts_users_fk", source_table="posts", referent_table="users",
                          local_cols=['owner_id'], remote_cols=['id'], ondelete='Cascade')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    
    pass
