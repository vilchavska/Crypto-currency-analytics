from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Boolean, DateTime, ForeignKey
import requests
import json
from datetime import datetime
from Flask_create import db
from db_config import DATABASE_URL, SCHEMA_NAME
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# connect to db
engine = create_engine(DATABASE_URL)

# Define the table structure as a Python class
class CoinsHist(db.Model):
    __tablename__ = 'coins_hist'
    __table_args__ = {'schema': SCHEMA_NAME }
    # columns
    id = Column(String, primary_key=True)
    symbol = Column(String)
    name = Column(String)
    image = Column(String)
    current_price = Column(Float)
    market_cap = Column(Float)
    market_cap_rank = Column(Integer)
    total_volume = Column(Float)
    high_24h = Column(Float)
    low_24h = Column(Float)
    price_change_24h = Column(Float)
    price_change_percentage_24h = Column(Float)
    market_cap_change_24h = Column(Float)
    market_cap_change_percentage_24h = Column(Float)
    circulating_supply = Column(Float)
    total_supply = Column(Float)
    max_supply = Column(Float)
    ath = Column(Float)
    ath_change_percentage = Column(Float)
    ath_date = Column(String)
    atl = Column(Float)
    atl_change_percentage = Column(Float)
    atl_date = Column(String)
    last_updated = Column(String)

def create_table_from_class(engine, base, table_class):
    try:
        # Bind the engine to the metadata of the Base class
        base.metadata.create_all(engine, tables=[table_class.__table__])
        logger.info(f"Table {table_class.__tablename__} created successfully in schema {table_class.__table_args__['schema']}.")
    except Exception as e:
        logger.critical(f"Error in create_table_from_class: {e}")
        raise


