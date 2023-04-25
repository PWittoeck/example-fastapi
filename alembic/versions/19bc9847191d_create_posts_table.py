"""create posts table

Revision ID: 19bc9847191d
Revises: 
Create Date: 2023-04-22 12:41:01.653013

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19bc9847191d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',
                     sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
                     sa.Column('title', sa.String(), nullable=False)
                     )
    pass


def downgrade():
    op.drop_table('posts')
    pass
