"""init

Revision ID: 78a6bcf56978
Revises: 
Create Date: 2021-02-03 01:40:18.433989

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78a6bcf56978'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('distributor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ip', sa.String(length=64), nullable=True),
    sa.Column('port', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_distributor_ip'), 'distributor', ['ip'], unique=True)
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uri', sa.String(length=1024), nullable=True),
    sa.Column('content', sa.String(length=4096), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('distributor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['distributor_id'], ['distributor.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_message_timestamp'), 'message', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_message_timestamp'), table_name='message')
    op.drop_table('message')
    op.drop_index(op.f('ix_distributor_ip'), table_name='distributor')
    op.drop_table('distributor')
    # ### end Alembic commands ###
