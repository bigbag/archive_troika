"""empty message

Revision ID: dd3e88c4b43
Revises: 571bc3798427
Create Date: 2015-05-13 13:41:14.061307

"""

# revision identifiers, used by Alembic.
revision = 'dd3e88c4b43'
down_revision = '571bc3798427'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cards', 'update_date',
               existing_type=mysql.DATETIME(),
               nullable=True,
               existing_server_default=sa.text(u'CURRENT_TIMESTAMP'))
    op.add_column('orders', sa.Column('image', sa.String(length=512), nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'image')
    op.alter_column('cards', 'update_date',
               existing_type=mysql.DATETIME(),
               nullable=False,
               existing_server_default=sa.text(u'CURRENT_TIMESTAMP'))
    ### end Alembic commands ###