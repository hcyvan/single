"""empty message

Revision ID: c598a8e77c3c
Revises: ba3670d0566b
Create Date: 2018-03-08 13:45:23.684642

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c598a8e77c3c'
down_revision = 'ba3670d0566b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notice', sa.Column('receiver_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('notice', 'receiver_id')
    # ### end Alembic commands ###
