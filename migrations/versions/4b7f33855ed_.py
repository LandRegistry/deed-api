# flake8: noqa
"""empty message

Revision ID: 4b7f33855ed
Revises: eb2745f554
Create Date: 2017-05-09 12:21:18.320826

"""

# revision identifiers, used by Alembic.
revision = '4b7f33855ed'
down_revision = 'eb2745f554'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('verify_match', sa.Column('confidence_level', sa.Integer(), nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('verify_match', 'confidence_level')
    ### end Alembic commands ###
