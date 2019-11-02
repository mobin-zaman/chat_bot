"""empty message

Revision ID: 7f6dd077c9df
Revises: 301959773946
Create Date: 2019-10-28 21:00:51.071369

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7f6dd077c9df'
down_revision = '301959773946'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('class_products',
    sa.Column('id', mysql.BIGINT(unsigned=True), nullable=False),
    sa.Column('cart_id', sa.Integer(), nullable=False),
    sa.Column('product_id', mysql.BIGINT(unsigned=True), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cart_id'], ['cart.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('class_products')
    # ### end Alembic commands ###
