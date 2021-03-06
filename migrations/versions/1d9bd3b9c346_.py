"""empty message

Revision ID: 1d9bd3b9c346
Revises: 43aaabba1c7e
Create Date: 2015-03-29 16:53:53.018490

"""

# revision identifiers, used by Alembic.
revision = '1d9bd3b9c346'
down_revision = '43aaabba1c7e'

import sqlalchemy as sa
from alembic import op


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cards_history',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('card_id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('before', sa.Text(), nullable=True),
                    sa.Column('after', sa.Text(), nullable=True),
                    sa.Column('action_date', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['card_id'], ['cards.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cards_history')
    ### end Alembic commands ###
