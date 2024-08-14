import psycopg2
from sqlalchemy import text
from sqlalchemy.schema import CreateSchema
from sqlalchemy.exc import SQLAlchemyError
from db_model.db_config import config 
import logging

logger = logging.getLogger()

# creating user and data base:
def create_testuser_and_database():

    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user=config['DB_ADMIN'],
            password=config['DB_ADMIN_PASSWORD'],
            host=config['DB_HOST'],
            port=config['DB_PORT']
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Create testuser if it doesn't exist
        cursor.execute(f"""
                         DO $$ 
                         BEGIN 
                            IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '{config['DB_USER']}') THEN 
                               CREATE ROLE {config['DB_USER']} WITH LOGIN PASSWORD '{config['DB_PASSWORD']}'; 
                            END IF; 
                         END $$;
                         """)
        logger.info(f"User '{config['DB_USER']}' checked/created successfully.")

        # Create the database if it doesn't exist
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{config['DB_NAME']}';")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f'CREATE DATABASE {config["DB_NAME"]};')
            logger.info(f"Database '{config['DB_NAME']}' created successfully.")
        else:
            logger.info(f"Database '{config['DB_NAME']}' already exists.")

        # Grant privileges on the database to the user
        cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {config['DB_NAME']} TO {config['DB_USER']};")
        
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f'Error in create_testuser_and_database: {e}')
        raise

def check_schema_exists(engine, schema_name):
    try:
        with engine.connect() as connection:
             result = connection.execute(text(f"""
                                               SELECT schema_name 
                                                 FROM information_schema.schemata 
                                                WHERE schema_name = :schema_name
                                              """
                                              ), 
                                            {'schema_name': schema_name}
                                        )
             return result.fetchone() is not None
    except SQLAlchemyError as e:
        logger.error(f"Error checking schema existence: {e}")
        return False

def create_schema(engine, schema_name):
    result = check_schema_exists(engine, schema_name)
    if result:
        logger.info(f"Schema {schema_name} already exists.")
        return
    
    with engine.connect() as connection:   
        try:
            logger.info(f"Creating schema {schema_name}.")
            connection.execute(CreateSchema(schema_name, if_not_exists=True))
            connection.commit()
            result = check_schema_exists(engine, schema_name)
            if result:
                logger.info(f"Schema {schema_name} created successfully.")
                return
        except SQLAlchemyError as e:
            logger.error(f"Error in create_schema: {e}")
            raise