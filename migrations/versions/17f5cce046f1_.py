"""empty message

Revision ID: 17f5cce046f1
Revises: 59c30355dac3
Create Date: 2015-05-10 15:14:46.164262

"""

# revision identifiers, used by Alembic.
revision = '17f5cce046f1'
down_revision = '59c30355dac3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('mobispot_user_email', sa.String(length=128), nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'mobispot_user_email')
    ### end Alembic commands ###