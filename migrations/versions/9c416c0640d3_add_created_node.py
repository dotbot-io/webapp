"""add created node



Revision ID: 9c416c0640d3
Revises: ff1dbf33852f
Create Date: 2016-03-04 22:38:31.056032

"""

# revision identifiers, used by Alembic.
revision = '9c416c0640d3'
down_revision = 'ff1dbf33852f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('nodes', sa.Column('created', sa.DateTime(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('nodes', 'created')
    ### end Alembic commands ###
