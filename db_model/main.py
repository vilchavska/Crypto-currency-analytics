from get_data import fetch_and_store_data
import logging
import schedule
#appschedule
#cron

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def run_daily_job():