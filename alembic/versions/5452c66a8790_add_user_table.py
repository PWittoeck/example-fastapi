"""add user table

Revision ID: 5452c66a8790
Revises: e6787945ef6d
Create Date: 2023-04-23 18:38:28.556430

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5452c66a8790'
down_revision = 'e6787945ef6d'
branch_labels = None
depends_on = None

def upgrade():
     op.create_table('users',
                     sa.Column('id', sa.Integer(), nullable=False),
                     sa.Column('email', sa.String(), nullable=False),
                     sa.Column('password', sa.String(), nullable=False),
                     sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                               server_default=sa.text('now()'),nullable=False),
                     sa.PrimaryKeyConstraint('id'),
                     sa.UniqueConstraint('email')
                     )
     pass


def downgrade():
    op.drop_table('users')
    pass
