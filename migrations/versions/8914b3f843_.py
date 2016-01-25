# flake8: noqa
"""empty message

Revision ID: 8914b3f843
Revises: 7aff0b2340
Create Date: 2015-11-18 17:11:56.366577

"""

# revision identifiers, used by Alembic.
revision = '8914b3f843'
down_revision = '7aff0b2340'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # commands auto generated by Alembic - please adjust!
    op.add_column('deed', sa.Column('token', sa.String(), nullable=False))
    # end Alembic commands


def downgrade():
    # commands auto generated by Alembic - please adjust!
    op.drop_column('deed', 'token')
    # end Alembic commands
