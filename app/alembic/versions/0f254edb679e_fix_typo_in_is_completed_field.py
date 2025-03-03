"""Fix typo in is_completed field

Revision ID: 0f254edb679e
Revises: 95e1f4fa1022
Create Date: 2025-03-03 15:35:11.846317

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0f254edb679e'
down_revision: Union[str, None] = '95e1f4fa1022'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('is_completed', sa.Boolean(), nullable=False))
    op.drop_column('tasks', 'is_compledted')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('is_compledted', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_column('tasks', 'is_completed')
    # ### end Alembic commands ###
