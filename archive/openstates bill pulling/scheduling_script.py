# %%
from crontab import CronTab

# Create a new crontab object
cron = CronTab(user='username')

# Add a new cron job to run the script every day at 6 AM
job = cron.new(command='python /path/to/script.py')
job.setall('0 6 *')

# Write the job to the user's crontab
cron.write()