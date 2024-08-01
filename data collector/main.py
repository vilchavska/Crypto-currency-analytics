from get_data import fetch_and_store_data
import logging
import schedule
#appschedule
#cron

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
# розділити scheduler та job
def run_daily_job():
    while True:
        fetch_and_store_data()

if __name__ == '__main__':
    run_daily_job()




        schedule.every().day.at("00:00").do(job)
        
        
        while True:
            schedule.run_pending()
            time.sleep(1)