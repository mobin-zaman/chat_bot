"""empty message

Revision ID: 3f023b6a7702
Revises: 9116e9f0c65e
Create Date: 2019-10-28 20:11:38.908746

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f023b6a7702'
down_revision = '9116e9f0c65e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'cart', 'messenger_user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'cart', type_='foreignkey')
    # ### end Alembic commands ###
