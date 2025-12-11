"""Update CalculationType enum to include advanced operations

Revision ID: 4609aba8a69c
Revises: b01b1ad235d4
Create Date: 2025-12-11 12:25:52.325228

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4609aba8a69c'
down_revision: Union[str, Sequence[str], None] = 'b01b1ad235d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # SQLite stores enums as VARCHAR, so no schema change is needed
    # The enum expansion from 6 to 9 operations is handled at the application level
    # New operations: PERCENT_OF, NTH_ROOT, LOG_BASE
    # This migration serves as a documentation of the schema evolution
    pass


def downgrade() -> None:
    """Downgrade schema."""
    # Downgrading would require removing calculations using the new operation types
    # This is a data-destructive operation and should be handled carefully
    # For safety, we leave this as a no-op
    pass
