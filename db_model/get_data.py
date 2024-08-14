import requests
import logging
from time import sleep
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from db_model import CoinsHist
from db_model.db_config import DATABASE_URL

logger = logging.getLogger()

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

class APIClient:
    @staticmethod
    def fetch_data(api_url):
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching data: {e}")
            return None

class Parser:
    @staticmethod
    def validate_data(data):
        if isinstance(data, list):
            return data
        else:
            logger.error("Invalid data format")
            return None

class DataStore:
    @staticmethod
    def store_data(data):
        try:
            for coin in data:
                coin_record = CoinsHist(
                    id=coin['id'],
                    symbol=coin['symbol'],
                    name=coin['name'],
                    image=coin['image'],
                    current_price=coin['current_price'],
                    market_cap=coin['market_cap'],
                    market_cap_rank=coin['market_cap_rank'],
                    total_volume=coin['total_volume'],
                    high_24h=coin['high_24h'],
                    low_24h=coin['low_24h'],
                    price_change_24h=coin['price_change_24h'],
                    price_change_percentage_24h=coin['price_change_percentage_24h'],
                    market_cap_change_24h=coin['market_cap_change_24h'],
                    market_cap_change_percentage_24h=coin['market_cap_change_percentage_24h'],
                    circulating_supply=coin['circulating_supply'],
                    total_supply=coin['total_supply'],
                    max_supply=coin['max_supply'],
                    ath=coin['ath'],
                    ath_change_percentage=coin['ath_change_percentage'],
                    ath_date=coin['ath_date'],
                    atl=coin['atl'],
                    atl_change_percentage=coin['atl_change_percentage'],
                    atl_date=coin['atl_date'],
                    last_updated=coin['last_updated']
                )
                session.add(coin_record)
            
            session.commit()
            logger.info("Data stored successfully.")
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Error storing data: {e}")

def fetch_and_store_data(api_url):
    api_client = APIClient()
    parser = Parser()
    data_store = DataStore()