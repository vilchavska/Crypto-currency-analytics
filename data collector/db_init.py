from sqlalchemy import create_engine
from db_create_db import create_testuser_and_database, create_schema
from db_model import CoinsHist, create_table_from_class
from db_config import DATABASE_URL, SCHEMA_NAME
from Flask_create import db
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

if __name__ == '__main__':
        create_testuser_and_database()
        engine = create_engine(DATABASE_URL)
        create_schema(engine, SCHEMA_NAME)
        # wait creating schema
        create_table_from_class(engine, db, CoinsHist)