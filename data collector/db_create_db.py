import logging
import psycopg2
from sqlalchemy import text
from sqlalchemy.schema import CreateSchema
from sqlalchemy.exc import SQLAlchemyError
from db_config import DB_ADMIN_USER, DB_ADMIN_PASSWORD, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

# logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# creating user and data base:
def create_testuser_and_database():
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user=DB_ADMIN_USER,
            password=DB_ADMIN_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # create testuser
        cursor.execute(f"DO $$ BEGIN IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '{DB_USER}') THEN CREATE ROLE {DB_USER} WITH LOGIN PASSWORD '{DB_PASSWORD}'; END IF; END $$;")
        logger.info(f'User {DB_USER} checked/created successfully.')

        # create data base
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_NAME}'")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f'CREATE DATABASE {DB_NAME}')
            logger.info(f'Database {DB_NAME} created successfully.')
        else:
            logger.info(f'Database {DB_NAME} already exists.')

        cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {DB_USER}")
        
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f'Error in create_user_and_database: {e}')
        raise

def create_schema(engine, schema_name):
    query = text("SELECT schema_name FROM information_schema.schemata WHERE schema_name=:schema_name")
    
    with engine.connect() as connection:
        result = connection.execute(query, {"schema_name": schema_name})
        if result.scalar():
            logger.info(f"Schema {schema_name} already exists.")
            return
        
        try:
            connection.execute(CreateSchema(schema_name))
            logger.info(f"Schema {schema_name} created successfully.")
        except SQLAlchemyError as e:
            logger.error(f"Error in create_schema: {e}")
            raise