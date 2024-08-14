from sqlalchemy import UniqueConstraint, Sequence, Column, Integer, String, Date, MetaData, Float, Boolean, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from db_model.db_config import config, admin_config,  DATABASE_URL
import logging
from Flask_create import db

logger = logging.getLogger()

# Metadata object with the specified schema
#metadata = MetaData(schema = config['DB_SCHEMA'])

# Base class for declarative models
#Base = declarative_base(metadata=metadata)

# Define the table structure as a Python class
class CoinsHist(db.Model): #CoinsHist(Base):  - does not worki
    __tablename__ = 'coins_hist'
    __table_args__ = {'schema': config['DB_SCHEMA'] }
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

class Coins(db.Model):
    __tablename__ = 'coins'
    __table_args__ = (
        UniqueConstraint('id_coin', name='uq_id_coin'),
        {'schema': config['DB_SCHEMA']}
    )

    # columns
    id = Column(Integer, Sequence('coins_id_seq', schema=config['DB_SCHEMA']), primary_key=True)
    id_coin = Column(String)

class JobsSchedule(db.Model):
    __tablename__ = 'jobs_schedule'
    __table_args__ = {'schema': config['DB_SCHEMA']}

    # columns
    job_name = Column(String, primary_key=True)
    cron = Column(String)
    call_command = Column(String)
    last_call = Column(Date)
    enabled = Column(Boolean)

def create_tables_from_classes(engine, base, tables_classes):
    try:
        # Bind the engine to the metadata of the Base class
        for table_class in tables_classes:
            base.metadata.create_all(engine, tables=[table_class.__table__])
            logger.info(f"Table {table_class.__tablename__} created successfully.")
    except SQLAlchemyError as e:
        logger.critical(f"Error in create_tables_from_classes: {e}")
        raise

def check_table_exists(engine, table_name, schema_name):
    try:
        with engine.connect() as connection:
             result = connection.execute(text(f"""
                                               SELECT table_name 
                                                 FROM information_schema.tables 
                                                WHERE table_schema = :schema_name
                                                  AND table_name = :table_name
                                              """
                                              ), 
                                            {'schema_name': schema_name, 'table_name': table_name}
                                        )
             return result.fetchone() is not None
    except SQLAlchemyError as e:
        logger.error(f"Error checking table_name existence: {e}")
        return False
