"""empty message

Revision ID: 07910a8627b6
Revises: bb5f13879887
Create Date: 2020-06-02 17:03:18.803000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07910a8627b6'
down_revision = 'bb5f13879887'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'user', ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    # ### end Alembic commands ###
