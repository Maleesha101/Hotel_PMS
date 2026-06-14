"""Create inventory_items table"""

# revision identifiers, used by Alembic.
revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade() -> None:
    op.create_table(
        "inventory_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("sku", sa.String(length=100), unique=True),
        sa.Column("available_qty", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("min_stock_level", sa.Integer(), nullable=False, server_default="5"),
        sa.Column("unit", sa.String(length=30)),
        sa.Column("unit_cost", sa.Numeric(10,2)),
        sa.Column("supplier_name", sa.String(length=255)),
        sa.Column("supplier_contact", sa.String(length=255)),
        sa.Column("location", sa.String(length=100)),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("last_restocked_at", sa.DateTime()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
    )
    op.create_index("idx_inv_category", "inventory_items", ["category"], unique=False)
    op.create_index("idx_inv_low_stock", "inventory_items", ["available_qty", "min_stock_level"], unique=False)

def downgrade() -> None:
    op.drop_index("idx_inv_low_stock", table_name="inventory_items")
    op.drop_index("idx_inv_category", table_name="inventory_items")
    op.drop_table("inventory_items")
