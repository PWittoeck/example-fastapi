"""add foreign key to posts table

Revision ID: 380ab41c9622
Revises: 5452c66a8790
Create Date: 2023-04-24 16:25:59.453288

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '380ab41c9622'
down_revision = '5452c66a8790'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users",
                           local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
