#!/usr/bin/env python3
"""
CRM Database Models
Tables for suppliers, buyers, leads/opportunities, quotes, and shipments
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Supplier(Base):
    """
    Supplier model for African agricultural product suppliers
    """
    __tablename__ = 'suppliers'
    
    id = Column(Integer, primary_key=True)
    company_name = Column(String(255), nullable=False)
    contact_person = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    country = Column(String(100))
    region = Column(String(100))
    products = Column(Text)  # Comma-separated list of products
    certification = Column(String(255))  # Organic, Fair Trade, etc.
    reliability_score = Column(Float)  # 0.0 to 1.0
    payment_terms = Column(String(100))  # Net 30, COD, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Buyer(Base):
    """
    Buyer model for US agricultural product buyers
    """
    __tablename__ = 'buyers'
    
    id = Column(Integer, primary_key=True)
    company_name = Column(String(255), nullable=False)
    contact_person = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    industry = Column(String(100))  # Retail, Manufacturing, etc.
    target_products = Column(Text)  # Comma-separated list of products
    annual_volume = Column(Float)  # Estimated annual volume in tons
    credit_rating = Column(String(50))  # AAA, AA, A, etc.
    payment_terms = Column(String(100))  # Net 30, Net 60, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Lead(Base):
    """
    Lead/Opportunity model for potential deals
    """
    __tablename__ = 'leads'
    
    id = Column(Integer, primary_key=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'))
    buyer_id = Column(Integer, ForeignKey('buyers.id'))
    product = Column(String(255), nullable=False)
    description = Column(Text)
    estimated_value = Column(Float)  # USD
    probability = Column(Float)  # 0.0 to 1.0
    status = Column(String(50))  # New, Contacted, Proposal, Negotiation, Closed-Won, Closed-Lost
    next_action = Column(String(255))
    next_action_date = Column(DateTime)
    assigned_to = Column(String(255))  # User responsible
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    supplier = relationship("Supplier")
    buyer = relationship("Buyer")

class Quote(Base):
    """
    Quote model for price quotations
    """
    __tablename__ = 'quotes'
    
    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer, ForeignKey('leads.id'))
    supplier_id = Column(Integer, ForeignKey('suppliers.id'))
    buyer_id = Column(Integer, ForeignKey('buyers.id'))
    product = Column(String(255), nullable=False)
    quantity = Column(Float)  # In tons or units
    unit_price = Column(Float)  # USD per unit
    total_price = Column(Float)  # USD
    currency = Column(String(10), default="USD")
    validity_period = Column(Integer)  # Days
    terms = Column(Text)  # Payment terms, delivery terms, etc.
    status = Column(String(50))  # Draft, Sent, Accepted, Rejected, Expired
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    lead = relationship("Lead")
    supplier = relationship("Supplier")
    buyer = relationship("Buyer")

class Shipment(Base):
    """
    Shipment model for tracking deliveries
    """
    __tablename__ = 'shipments'
    
    id = Column(Integer, primary_key=True)
    quote_id = Column(Integer, ForeignKey('quotes.id'))
    supplier_id = Column(Integer, ForeignKey('suppliers.id'))
    buyer_id = Column(Integer, ForeignKey('buyers.id'))
    tracking_number = Column(String(100))
    carrier = Column(String(100))  # Maersk, CMA CGM, etc.
    origin_port = Column(String(100))
    destination_port = Column(String(100))
    departure_date = Column(DateTime)
    arrival_date = Column(DateTime)
    status = Column(String(50))  # Scheduled, In Transit, Delivered, Delayed
    quantity = Column(Float)  # In tons or units
    weight_kg = Column(Float)
    volume_cbm = Column(Float)  # Cubic meters
    shipping_cost = Column(Float)  # USD
    insurance_cost = Column(Float)  # USD
    customs_clearance_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    quote = relationship("Quote")
    supplier = relationship("Supplier")
    buyer = relationship("Buyer")

# Create tables function
def create_tables(engine):
    """
    Create all CRM tables
    """
    Base.metadata.create_all(engine)
    print("CRM tables created successfully")

if __name__ == "__main__":
    # This is just for testing the model definitions
    from sqlalchemy import create_engine
    from src.config.settings import DATABASE_URL
    
    engine = create_engine(DATABASE_URL)
    create_tables(engine)