"""index-kernel-timestamps

Revision ID: 0c5733f80e4d
Revises: 9bd986a75a2a
Create Date: 2019-09-24 15:58:58.932029

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0c5733f80e4d"
down_revision = "9bd986a75a2a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "kernels",
        "status",
        existing_type=postgresql.ENUM(
            "PENDING",
            "PREPARING",
            "BUILDING",
            "PULLING",
            "RUNNING",
            "RESTARTING",
            "RESIZING",
            "SUSPENDED",
            "TERMINATING",
            "TERMINATED",
            "ERROR",
            "CANCELLED",
            name="kernelstatus",
        ),
        nullable=False,
        existing_server_default=sa.text("'PENDING'::kernelstatus"),
    )
    op.alter_column(
        "kernels",
        "type",
        existing_type=postgresql.ENUM("INTERACTIVE", "BATCH", name="sessiontypes"),
        nullable=False,
        existing_server_default=sa.text("'INTERACTIVE'::sessiontypes"),
    )
    op.create_index(op.f("ix_kernels_status_changed"), "kernels", ["status_changed"], unique=False)
    op.create_index(
        "ix_kernels_updated_order",
        "kernels",
        ["created_at", "terminated_at", "status_changed"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_kernels_updated_order", table_name="kernels")
    op.drop_index(op.f("ix_kernels_status_changed"), table_name="kernels")
    op.alter_column(
        "kernels",
        "type",
        existing_type=postgresql.ENUM("INTERACTIVE", "BATCH", name="sessiontypes"),
        nullable=True,
        existing_server_default=sa.text("'INTERACTIVE'::sessiontypes"),
    )
    op.alter_column(
        "kernels",
        "status",
        existing_type=postgresql.ENUM(
            "PENDING",
            "PREPARING",
            "BUILDING",
            "PULLING",
            "RUNNING",
            "RESTARTING",
            "RESIZING",
            "SUSPENDED",
            "TERMINATING",
            "TERMINATED",
            "ERROR",
            "CANCELLED",
            name="kernelstatus",
        ),
        nullable=True,
        existing_server_default=sa.text("'PENDING'::kernelstatus"),
    )
    # ### end Alembic commands ###
