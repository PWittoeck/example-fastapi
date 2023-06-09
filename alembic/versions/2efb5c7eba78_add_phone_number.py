"""add phone number

Revision ID: 2efb5c7eba78
Revises: 656f1e150397
Create Date: 2023-04-24 21:02:50.318450

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2efb5c7eba78'
down_revision = '656f1e150397'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###
