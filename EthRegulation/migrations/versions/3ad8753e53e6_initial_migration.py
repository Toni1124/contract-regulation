"""Initial migration

Revision ID: 3ad8753e53e6
Revises: 
Create Date: 2025-02-22 15:30:25.849111

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ad8753e53e6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('black_white_list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=42), nullable=False),
    sa.Column('operate_time', sa.DateTime(), nullable=False),
    sa.Column('operator', sa.String(length=50), nullable=False),
    sa.Column('type', sa.SmallInteger(), nullable=False),
    sa.Column('organization', sa.String(length=100), nullable=False),
    sa.Column('region', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('address')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('black_white_list')
    # ### end Alembic commands ###
