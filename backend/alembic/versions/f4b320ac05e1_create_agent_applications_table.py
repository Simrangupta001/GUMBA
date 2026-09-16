"""create agent applications table

Revision ID: f4b320ac05e1
Revises: fddc7e7acd42
Create Date: 2026-08-31 15:42:18.680343

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'f4b320ac05e1'
down_revision: Union[str, Sequence[str], None] = 'fddc7e7acd42'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('agent_applications', sa.Column('gumba_id', sa.Integer(), nullable=True))
    op.add_column('agent_applications', sa.Column('gumba_application_type', sa.String(length=20), nullable=False))
    op.add_column('agent_applications', sa.Column('new_gumba_name', sa.String(length=100), nullable=True))
    op.add_column('agent_applications', sa.Column('new_gumba_description', sa.Text(), nullable=True))
    op.add_column('agent_applications', sa.Column('new_gumba_address', sa.String(length=255), nullable=True))
    op.add_column('agent_applications', sa.Column('new_gumba_district', sa.String(length=100), nullable=True))
    op.add_column('agent_applications', sa.Column('new_gumba_municipality', sa.String(length=100), nullable=True))
    op.add_column('agent_applications', sa.Column('new_gumba_ward_no', sa.String(length=20), nullable=True))
    op.add_column('agent_applications', sa.Column('new_gumba_contact_phone', sa.String(length=20), nullable=True))
    op.add_column('agent_applications', sa.Column('new_gumba_contact_email', sa.String(length=255), nullable=True))
    op.add_column('agent_applications', sa.Column('new_gumba_website', sa.String(length=255), nullable=True))
    op.add_column('agent_applications', sa.Column('new_gumba_latitude', sa.Float(), nullable=True))
    op.add_column('agent_applications', sa.Column('new_gumba_longitude', sa.Float(), nullable=True))
    op.create_index('ix_agent_applications_gumba_id', 'agent_applications', ['gumba_id'])
    op.create_foreign_key(
        'fk_agent_applications_gumba_id',
        'agent_applications', 'gumbas',
        ['gumba_id'], ['id']
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_agent_applications_gumba_id', 'agent_applications', type_='foreignkey')
    op.drop_index('ix_agent_applications_gumba_id', table_name='agent_applications')
    op.drop_column('agent_applications', 'new_gumba_longitude')
    op.drop_column('agent_applications', 'new_gumba_latitude')
    op.drop_column('agent_applications', 'new_gumba_website')
    op.drop_column('agent_applications', 'new_gumba_contact_email')
    op.drop_column('agent_applications', 'new_gumba_contact_phone')
    op.drop_column('agent_applications', 'new_gumba_ward_no')
    op.drop_column('agent_applications', 'new_gumba_municipality')
    op.drop_column('agent_applications', 'new_gumba_district')
    op.drop_column('agent_applications', 'new_gumba_address')
    op.drop_column('agent_applications', 'new_gumba_description')
    op.drop_column('agent_applications', 'new_gumba_name')
    op.drop_column('agent_applications', 'gumba_application_type')
    op.drop_column('agent_applications', 'gumba_id')