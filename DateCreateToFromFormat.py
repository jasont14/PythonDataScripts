import datetime 
#### Set todays date ####
today = datetime.datetime.now().date()
#### Create to_date by adding or subtracting dates from today's date
to_date = today-datetime.timedelta(1) 
#### Create your from date by subtracting the number of days back #### you want to start
from_date = today-datetime.timedelta(7)
#### Create timestamp of today's date using desired format
todaysdate = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d')

print(today)

print(to_date)

print (from_date)

print (todaysdate)