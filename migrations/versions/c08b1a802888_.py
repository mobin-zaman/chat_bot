"""empty message

Revision ID: c08b1a802888
Revises: 7f6dd077c9df
Create Date: 2019-11-03 02:38:02.413147

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c08b1a802888'
down_revision = '7f6dd077c9df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cart', sa.Column('ordered', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cart', 'ordered')
    # ### end Alembic commands ###
