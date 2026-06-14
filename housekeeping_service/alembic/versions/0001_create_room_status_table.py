"""Create room_status table"""

# revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade() -> None:
    op.create_table(
        "room_status",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("room_id", sa.String(length=50), nullable=False, unique=True),
        sa.Column("room_number", sa.String(length=20), nullable=False),
        sa.Column("floor", sa.SmallInteger()),
        sa.Column("room_type", sa.String(length=50)),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="VACANT"),
        sa.Column("previous_status", sa.String(length=30)),
        sa.Column("updated_by", sa.String(length=100)),
        sa.Column("status_note", sa.Text()),
        sa.Column("last_checkout", sa.DateTime()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
    )
    op.create_index("idx_rs_status", "room_status", ["status"], unique=False)
    op.create_index("idx_rs_room_id", "room_status", ["room_id"], unique=False)

def downgrade() -> None:
    op.drop_index("idx_rs_room_id", table_name="room_status")
    op.drop_index("idx_rs_status", table_name="room_status")
    op.drop_table("room_status")
