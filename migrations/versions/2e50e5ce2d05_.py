"""empty message

Revision ID: 2e50e5ce2d05
Revises: 92518294fbba
Create Date: 2018-06-30 17:37:58.404074

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e50e5ce2d05'
down_revision = '92518294fbba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('banner', sa.Column('create_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('banner', 'create_time')
    # ### end Alembic commands ###