"""update team table

Revision ID: 9bb95c34bbfc
Revises: dd821f2418b1
Create Date: 2026-01-22 22:49:49.740518
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '9bb95c34bbfc'
down_revision: Union[str, Sequence[str], None] = 'dd821f2418b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# ✅ define enum ONCE
formation_enum = sa.Enum(
    'F_352',
    'F_343',
    'F_451',
    'F_442',
    'F_433',
    'F_541',
    'F_532',
    'F_523',
    name='formation_enum'
)


def upgrade() -> None:
    # 1️⃣ create enum type in PostgreSQL
    formation_enum.create(op.get_bind(), checkfirst=True)

    # 2️⃣ add column using enum
    op.add_column(
        'Teams',
        sa.Column('formation', formation_enum, nullable=False)
    )


def downgrade() -> None:
    # 1️⃣ drop column first
    op.drop_column('Teams', 'formation')

    # 2️⃣ drop enum type
    formation_enum.drop(op.get_bind(), checkfirst=True)
