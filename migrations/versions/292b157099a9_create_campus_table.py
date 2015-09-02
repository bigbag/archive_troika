"""create campus table

Revision ID: 292b157099a9
Revises: 3b348d995e9c
Create Date: 2015-08-27 17:53:51.676146

"""

# revision identifiers, used by Alembic.
revision = '292b157099a9'
down_revision = '3b348d995e9c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('campus',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=128), nullable=False),
                    sa.Column(
                        'address', sa.String(length=128), nullable=False),
                    sa.Column('zip', sa.String(length=16), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )

    op.add_column(
        'cards', sa.Column('campus_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        'fk_cards_campus', 'cards', 'campus', ['campus_id'], ['id'])


def downgrade():
    op.drop_constraint('fk_cards_campus', 'cards', type_='foreignkey')
    op.drop_column('cards', 'campus_id')
    op.drop_table('campus')
