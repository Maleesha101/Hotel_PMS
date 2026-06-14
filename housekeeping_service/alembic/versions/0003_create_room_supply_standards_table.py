"""Create room_supply_standards table"""

# revision identifiers, used by Alembic.
revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade() -> None:
    op.create_table(
        "room_supply_standards",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("room_type", sa.String(length=50), nullable=False),
        sa.Column("item_name", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("quantity", sa.SmallInteger(), nullable=False, server_default="1"),
        sa.Column("unit", sa.String(length=30)),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("notes", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        sa.UniqueConstraint("room_type", "item_name", name="uq_room_type_item_name"),
    )
    op.create_index("idx_rss_room_type", "room_supply_standards", ["room_type"], unique=False)

def downgrade() -> None:
    op.drop_index("idx_rss_room_type", table_name="room_supply_standards")
    op.drop_table("room_supply_standards")
