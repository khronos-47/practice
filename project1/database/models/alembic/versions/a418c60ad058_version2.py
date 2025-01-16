"""version2

Revision ID: a418c60ad058
Revises: 74f18792be9f
Create Date: 2025-01-16 21:56:06.712851

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a418c60ad058'
down_revision: Union[str, None] = '74f18792be9f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('common_item', sa.Column('number', sa.TEXT(), nullable=False))
    op.add_column('common_item', sa.Column('address', sa.TEXT(), nullable=True))
    op.add_column('common_item', sa.Column('region', sa.TEXT(), nullable=True))
    op.drop_column('common_item', 'association')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('common_item', sa.Column('association', sa.TEXT(), autoincrement=False, nullable=False))
    op.drop_column('common_item', 'region')
    op.drop_column('common_item', 'address')
    op.drop_column('common_item', 'number')
    # ### end Alembic commands ###