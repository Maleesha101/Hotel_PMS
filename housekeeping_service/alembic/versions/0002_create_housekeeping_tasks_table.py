"""Create housekeeping_tasks table"""

# revision identifiers, used by Alembic.
revision = "0002"
 down_revision = "0001"
 branch_labels = None
 depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade() -> None:
    op.create_table(
        "housekeeping_tasks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("room_id", sa.String(length=50), nullable=False),
        sa.Column("room_number", sa.String(length=20), nullable=False),
        sa.Column("booking_ref", sa.String(length=100)),
        sa.Column("task_type", sa.String(length=50), nullable=False),
        sa.Column("assigned_staff", sa.String(length=100)),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="PENDING"),
        sa.Column("priority", sa.String(length=20), nullable=False, server_default="NORMAL"),
        sa.Column("scheduled_for", sa.DateTime()),
        sa.Column("started_at", sa.DateTime()),
        sa.Column("completed_at", sa.DateTime()),
        sa.Column("cleaning_notes", sa.Text()),
        sa.Column("damaged_item_notes", sa.Text()),
        sa.Column("missing_item_notes", sa.Text()),
        sa.Column("supplies_replaced", postgresql.JSONB),
        sa.Column("linked_complaint_id", sa.String(length=100)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
    )
    op.create_index("idx_ht_room_id", "housekeeping_tasks", ["room_id"], unique=False)
    op.create_index("idx_ht_status", "housekeeping_tasks", ["status"], unique=False)
    op.create_index("idx_ht_staff", "housekeeping_tasks", ["assigned_staff"], unique=False)

def downgrade() -> None:
    op.drop_index("idx_ht_staff", table_name="housekeeping_tasks")
    op.drop_index("idx_ht_status", table_name="housekeeping_tasks")
    op.drop_index("idx_ht_room_id", table_name="housekeeping_tasks")
    op.drop_table("housekeeping_tasks")
