"""Initial migration with census_data, world_bank_data, fred_data, fx_rates, and arbitrage_opportunities tables

Revision ID: 5b8da4bd8d7c
Revises: 
Create Date: 2025-09-03 15:32:28.073735

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b8da4bd8d7c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create census_data table
    op.create_table(
        'census_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        # Add other columns as needed based on actual data structure
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create world_bank_data table
    op.create_table(
        'world_bank_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('indicator', sa.String(), nullable=True),
        sa.Column('date', sa.String(), nullable=True),
        sa.Column('value', sa.Float(), nullable=True),
        sa.Column('country', sa.String(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create fred_data table
    op.create_table(
        'fred_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('series_id', sa.String(), nullable=True),
        sa.Column('series_name', sa.String(), nullable=True),
        sa.Column('date', sa.String(), nullable=True),
        sa.Column('value', sa.Float(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create fx_rates table
    op.create_table(
        'fx_rates',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('base_currency', sa.String(), nullable=True),
        sa.Column('target_currency', sa.String(), nullable=True),
        sa.Column('rate', sa.Float(), nullable=True),
        sa.Column('date', sa.String(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create arbitrage_opportunities table
    op.create_table(
        'arbitrage_opportunities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('product', sa.String(), nullable=True),
        sa.Column('origin_country', sa.String(), nullable=True),
        sa.Column('export_price_usd', sa.Float(), nullable=True),
        sa.Column('us_market_price_usd', sa.Float(), nullable=True),
        sa.Column('gross_margin', sa.Float(), nullable=True),
        sa.Column('net_margin_estimate', sa.Float(), nullable=True),
        sa.Column('monthly_volume_potential_tons', sa.Float(), nullable=True),
        sa.Column('revenue_potential_usd', sa.Float(), nullable=True),
        sa.Column('commission_potential_usd', sa.Float(), nullable=True),
        sa.Column('agoa_eligible', sa.Boolean(), nullable=True),
        sa.Column('certification_premiums', sa.String(), nullable=True),
        sa.Column('risk_level', sa.String(), nullable=True),
        sa.Column('action_required', sa.String(), nullable=True),
        sa.Column('buyer_targets', sa.String(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('arbitrage_opportunities')
    op.drop_table('fx_rates')
    op.drop_table('fred_data')
    op.drop_table('world_bank_data')
    op.drop_table('census_data')