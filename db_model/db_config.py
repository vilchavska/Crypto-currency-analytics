import configparser
import os

def load_config(env='development'):
    config = configparser.ConfigParser()
    config_path = 'db_config.ini'

    # Read the config file
    config.read(config_path)

    if env not in config:
        raise ValueError(f"Environment '{env}' not found in the config file.")

    return {
        'DB_ADMIN' : config.get(env, 'DB_ADMIN_USER'),
        'DB_ADMIN_PASSWORD' : config.get(env, 'DB_ADMIN_PASSWORD'),
        'DB_HOST': config.get(env, 'DB_HOST'),
        'DB_PORT': config.getint(env, 'DB_PORT'),
        'DB_NAME': config.get(env, 'DB_NAME'),
        'DB_USER': config.get(env, 'DB_USER'),
        'DB_PASSWORD': config.get(env, 'DB_PASSWORD'),
        'DB_SCHEMA': config.get(env, 'SCHEMA_NAME')
    }

# Load configuration for the desired environment
environment = 'development'
config = load_config(environment)
admin_config = load_config('admin_db')

# url to connect to db
DATABASE_URL = f"postgresql://{config['DB_USER']}:{config['DB_PASSWORD']}@{config['DB_HOST']}:{config['DB_PORT']}/{config['DB_NAME']}"
