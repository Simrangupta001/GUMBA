"""add user profile fields

Revision ID: 9f1c2a7b3d44
Revises: f4b320ac05e1
Create Date: 2026-09-16 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '9f1c2a7b3d44'
down_revision: Union[str, Sequence[str], None] = 'f4b320ac05e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('profile_photo', sa.String(length=500), nullable=True))
    op.add_column('users', sa.Column('address', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('district', sa.String(length=100), nullable=True))
    op.add_column('users', sa.Column('municipality', sa.String(length=100), nullable=True))
    op.add_column('users', sa.Column('ward_no', sa.String(length=20), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'ward_no')
    op.drop_column('users', 'municipality')
    op.drop_column('users', 'district')
    op.drop_column('users', 'address')
    op.drop_column('users', 'profile_photo')