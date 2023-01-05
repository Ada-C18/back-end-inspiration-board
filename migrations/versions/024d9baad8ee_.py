"""empty message

Revision ID: 024d9baad8ee
Revises: 38c988e1c1f7
Create Date: 2023-01-04 12:46:56.744933

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '024d9baad8ee'
down_revision = '38c988e1c1f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('card', sa.Column('board_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'card', 'board', ['board_id'], ['board_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'card', type_='foreignkey')
    op.drop_column('card', 'board_id')
    # ### end Alembic commands ###
