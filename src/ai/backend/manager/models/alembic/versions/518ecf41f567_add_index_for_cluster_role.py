"""add-index-for-cluster_role

Revision ID: 518ecf41f567
Revises: dc9b66466e43
Create Date: 2021-01-07 00:04:53.794638

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '518ecf41f567'
down_revision = 'dc9b66466e43'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_kernels_cluster_role'), 'kernels', ['cluster_role'], unique=False)
    op.create_index('ix_kernels_status_role', 'kernels', ['status', 'cluster_role'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_kernels_status_role', table_name='kernels')
    op.drop_index(op.f('ix_kernels_cluster_role'), table_name='kernels')
    # ### end Alembic commands ###
