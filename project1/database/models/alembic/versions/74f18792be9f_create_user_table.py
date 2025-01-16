"""Create user table

Revision ID: 74f18792be9f
Revises: 
Create Date: 2025-01-16 21:04:50.852629

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74f18792be9f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('common_item',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('ownership_form', sa.TEXT(), nullable=False),
    sa.Column('economic_activity', sa.TEXT(), nullable=False),
    sa.Column('association', sa.TEXT(), nullable=False),
    sa.Column('organization', sa.TEXT(), nullable=False),
    sa.Column('inn', sa.TEXT(), nullable=False),
    sa.Column('kpp', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_common_item_inn'), 'common_item', ['inn'], unique=False)
    op.create_index(op.f('ix_common_item_kpp'), 'common_item', ['kpp'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_common_item_kpp'), table_name='common_item')
    op.drop_index(op.f('ix_common_item_inn'), table_name='common_item')
    op.drop_table('common_item')
    # ### end Alembic commands ###