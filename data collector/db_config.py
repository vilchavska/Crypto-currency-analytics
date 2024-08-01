# parameters for connection to PostgreSQL
DB_ADMIN_USER = 'postgres'
DB_ADMIN_PASSWORD = '12345' #admin_password
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'crypto'
DB_USER = 'testuser'
DB_PASSWORD = '12345678' #testuser password
SCHEMA_NAME = 'crypto_tenant'

# url to connect to db
DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

currency = 'USD'

# source api
API_URL =  f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={currency}"