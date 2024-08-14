import psycopg2
from datetime import datetime, date
from croniter import croniter
import subprocess
from sqlalchemy import create_engine
from db_config import DATABASE_URL, config

# Connect to the database
engine = create_engine(DATABASE_URL)

# Database connection setup
connection = psycopg2.connect(
    dbname='crypto',
    user=config['DB_USER'],
    password=config['DB_PASSWORD'],
    host=config['DB_HOST'],
    port=config['DB_PORT']
)
cursor = connection.cursor()

# Fetch all jobs
cursor.execute("SELECT job_name, cron, last_call, call_command FROM crypto_tenant.jobs_schedule")
jobs = cursor.fetchall()

for job_name, cron, last_call, call_command in jobs:
    # Convert last_call to datetime if it's not already
    if isinstance(last_call, date) and not isinstance(last_call, datetime):
        last_call = datetime.combine(last_call, datetime.min.time())
    
    # Check if job was called today
    if last_call.date() < date.today():
        print(last_call)
        print(date.today())
        # Check if the job should run according to its cron schedule
        cron_schedule = croniter(cron, last_call)
        next_run = cron_schedule.get_next(datetime)
        print(next_run)
        
        if next_run.date() == date.today():
            # Execute the job
            subprocess.call(call_command, shell=True)
            print(f"Executed job: {job_name}")
            
            # Update last_call in the database
            now = datetime.now()
            cursor.execute("UPDATE crypto_tenant.jobs_schedule SET last_call = %s WHERE job_name = %s", (now, job_name))
            connection.commit()

# Close the database connection
cursor.close()
connection.close()
