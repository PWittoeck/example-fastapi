"""add content column to posts table

Revision ID: e6787945ef6d
Revises: 19bc9847191d
Create Date: 2023-04-23 17:56:26.232665

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6787945ef6d'
down_revision = '19bc9847191d'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass

def downgrade():
    op.drop_column('posts', 'content')
    pass
