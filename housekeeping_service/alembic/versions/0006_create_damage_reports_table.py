"""Create damage_reports table"""

# revision identifiers, used by Alembic.
revision = "0006"
down_revision = "0005"
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade() -> None:
    op.create_table(
        "damage_reports",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("room_id", sa.String(length=50), nullable=False),
        sa.Column("task_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("booking_ref", sa.String(length=100)),
        sa.Column("item_description", sa.String(length=500), nullable=False),
        sa.Column("damage_type", sa.String(length=30), nullable=False),
        sa.Column("reported_by", sa.String(length=100), nullable=False),
        sa.Column("is_guest_chargeable", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("requires_repair", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("estimated_cost", sa.Numeric(10,2)),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="OPEN"),
        sa.Column("photo_urls", postgresql.ARRAY(sa.Text)),
        sa.Column("maintenance_request_id", sa.String(length=100)),
        sa.Column("invoice_charge_id", sa.String(length=100)),
        sa.Column("admin_notes", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        sa.ForeignKeyConstraint(["task_id"], ["housekeeping_tasks.id"], ),
    )
    op.create_index("idx_dr_room_id", "damage_reports", ["room_id"], unique=False)
    op.create_index("idx_dr_status", "damage_reports", ["status"], unique=False)
    op.create_index("idx_dr_task_id", "damage_reports", ["task_id"], unique=False)

def downgrade() -> None:
    op.drop_index("idx_dr_task_id", table_name="damage_reports")
    op.drop_index("idx_dr_status", table_name="damage_reports")
    op.drop_index("idx_dr_room_id", table_name="damage_reports")
    op.drop_table("damage_reports")
