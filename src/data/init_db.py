#!/usr/bin/env python3
"""
Database Initialization Script
Create all required tables for the Africa-USA Trade Intelligence Platform
"""
import os
from sqlalchemy import create_engine
from src.config.settings import DATABASE_URL
from src.data.models.crm_models import create_tables as create_crm_tables

def init_database():
    """
    Initialize the database with all required tables
    """
    print("Initializing database...")
    
    try:
        # Create database engine
        engine = create_engine(DATABASE_URL)
        
        # Create CRM tables
        create_crm_tables(engine)
        
        # Create tables for data ingestion
        create_data_tables(engine)
        
        # Create tables for arbitrage opportunities
        create_arbitrage_tables(engine)
        
        print("Database initialization completed successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise

def create_data_tables(engine):
    """
    Create tables for ingested data
    """
    from sqlalchemy import Column, Integer, String, Float, DateTime, Text
    from sqlalchemy.ext.declarative import declarative_base
    
    Base = declarative_base()
    
    class CensusData(Base):
        __tablename__ = 'census_data'
        id = Column(Integer, primary_key=True)
        year = Column(String(4))
        month = Column(String(2))
        state = Column(String(50))
        product_code = Column(String(20))
        product_description = Column(Text)
        generic_description = Column(Text)
        value = Column(Float)
        timestamp = Column(DateTime)
    
    class WorldBankData(Base):
        __tablename__ = 'world_bank_data'
        id = Column(Integer, primary_key=True)
        indicator = Column(String(100))
        date = Column(String(10))
        value = Column(Float)
        country = Column(String(100))
        timestamp = Column(DateTime)
    
    class FredData(Base):
        __tablename__ = 'fred_data'
        id = Column(Integer, primary_key=True)
        series_id = Column(String(50))
        series_name = Column(String(255))
        date = Column(String(10))
        value = Column(Float)
        timestamp = Column(DateTime)
    
    class FxRates(Base):
        __tablename__ = 'fx_rates'
        id = Column(Integer, primary_key=True)
        base_currency = Column(String(3))
        target_currency = Column(String(3))
        rate = Column(Float)
        date = Column(String(10))
        timestamp = Column(DateTime)
    
    # Create tables
    Base.metadata.create_all(engine)
    print("Data ingestion tables created successfully")

def create_arbitrage_tables(engine):
    """
    Create tables for arbitrage opportunities
    """
    from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
    from sqlalchemy.ext.declarative import declarative_base
    
    Base = declarative_base()
    
    class ArbitrageOpportunity(Base):
        __tablename__ = 'arbitrage_opportunities'
        id = Column(Integer, primary_key=True)
        product = Column(String(255))
        origin_country = Column(String(100))
        export_price_usd = Column(Float)
        us_market_price_usd = Column(Float)
        gross_margin = Column(Float)
        net_margin_estimate = Column(Float)
        monthly_volume_potential_tons = Column(Float)
        revenue_potential_usd = Column(Float)
        commission_potential_usd = Column(Float)
        agoa_eligible = Column(Boolean)
        certification_premiums = Column(String(255))
        risk_level = Column(String(50))
        action_required = Column(Text)
        buyer_targets = Column(Text)
        timestamp = Column(DateTime)
    
    # Create tables
    Base.metadata.create_all(engine)
    print("Arbitrage opportunity tables created successfully")

if __name__ == "__main__":
    init_database()