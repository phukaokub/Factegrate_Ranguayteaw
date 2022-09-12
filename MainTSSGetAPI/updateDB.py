from datetime import datetime
import json
import urllib3
import RanGuayTaewAPI
http = urllib3.PoolManager()

def updateNewBox(color, status): # Add new box to the database
    # Get date & time
    now = datetime.now()
    year = now.date().year
    month = now.date().month
    day = now.date().day
    #print(f'Date : {year} {month} {day}')
    hour = now.time().hour
    min = now.time().minute
    sec = now.time().second
    #print(f'Time : {hour} {min} {sec}') 

    # Get factory section
    section = 'Noodle Sorting'
    
    # Update new box data to sortingSystem table
    RanGuayTaewAPI.sendSortingSystemData(year, month, day, hour, min, sec, section, color, status)

