from db_create_db import create_testuser_and_database, create_schema, check_schema_exists
from db_model.db_config import config, admin_config,  DATABASE_URL
from sqlalchemy import create_engine, insert
from sqlalchemy.exc import SQLAlchemyError
from Flask_create import db
from db_model import CoinsHist, Coins, JobsSchedule, create_tables_from_classes, check_table_exists, insert_into_table
import logging
import time
from datetime import date

# logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
#config = load_config('development') # Load the db 'crypto' configuration from the config file

if __name__ == '__main__':
    # Step 1: Create the user and the database
    create_testuser_and_database()

    
    # Connect to the database
    engine = create_engine(DATABASE_URL)
                    
    # Step 2: Create develop schemas based on the configuration
    create_schema(engine, config['DB_SCHEMA'])

    schema_exists = False
    attempts = 0
    max_attempts = 3
    while attempts < max_attempts:
        if check_schema_exists(engine, config['DB_SCHEMA']):
            schema_exists = True
            break
        attempts += 1
        logger.info(f"Schema {config['DB_SCHEMA']} not found. Retrying in 5 seconds... ({attempts}/{max_attempts})")
        time.sleep(5)
        create_schema(engine, config['DB_SCHEMA'])

    if schema_exists:
        # Step 4: Create develop tables
        tables_classes = [CoinsHist, Coins, JobsSchedule]
        create_tables_from_classes(engine, db, tables_classes)
    else:
        logger.error(f"Schema {config['DB_SCHEMA']}  was not created after {max_attempts} attempts.")

if check_table_exists(engine, 'jobs_schedule', config['DB_SCHEMA']):
    logger.info(f"Table jobs_schedule exists.")

    try:
        with engine.connect() as conn:
            with conn.begin():
                # Создаем объект вставки
                stmt = insert(JobsSchedule).values([
                    {
                        "job_name": "fetch_and_store_data", 
                        "cron": "2 * * * *", 
                        "call_command": "fetch_and_store_data()", 
                        "last_call": date.today(), 
                        "enabled": True
                    }
                ])
                conn.execute(stmt)
                logger.info(f"Data inserted into table jobs_schedule successfully.")
    except SQLAlchemyError as e:
        logger.error(f"Error inserting data into jobs_schedule: {e}")
else:
    logger.error(f"Table jobs_schedule could not be filled.")

    # Step 5: Create admin schemas based on the configuration
    create_schema(engine, admin_config['DB_SCHEMA'])
    