"""Create inventory_transactions table"""

# revision identifiers, used by Alembic.
revision = "0005"
 down_revision = "0004"
 branch_labels = None
 depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade() -> None:
    op.create_table(
        "inventory_transactions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("item_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("transaction_type", sa.String(length=20), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("balance_after", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.String(length=50)),
        sa.Column("task_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("performed_by", sa.String(length=100)),
        sa.Column("notes", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        sa.ForeignKeyConstraint(["item_id"], ["inventory_items.id"], ),
        sa.ForeignKeyConstraint(["task_id"], ["housekeeping_tasks.id"], ),
    )
    op.create_index("idx_it_item_id", "inventory_transactions", ["item_id"], unique=False)
    op.create_index("idx_it_task_id", "inventory_transactions", ["task_id"], unique=False)
    op.create_index("idx_it_room_id", "inventory_transactions", ["room_id"], unique=False)

def downgrade() -> None:
    op.drop_index("idx_it_room_id", table_name="inventory_transactions")
    op.drop_index("idx_it_task_id", table_name="inventory_transactions")
    op.drop_index("idx_it_item_id", table_name="inventory_transactions")
    op.drop_table("inventory_transactions")
