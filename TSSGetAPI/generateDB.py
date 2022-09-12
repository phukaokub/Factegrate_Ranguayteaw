from datetime import datetime
import json
from csv import writer
import urllib3
import RanGuayTaewAPI
http = urllib3.PoolManager()

def updateNewBox(): # Add new box to the database
    responseAPI = http.request("GET",
                              f"http://localhost/tss/0/sensor/10")
    data    = responseAPI.data.decode("utf-8")
    parseJson = json.loads(data)

    # Get color
    color =  parseJson['value']
    #print(f'Color : {color}')

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
    status = 'Unsort'
    
    # Update new box data to sortingSystem table
    RanGuayTaewAPI.sendSortingSystemData(year, month, day, hour, min, sec, section, color, status)
def sorted(color): # Update new sorted noodle to the csv
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
    status = 'Sorted'

    # # Update new data to the next row
    # newData = [year, month, day, hour, min, sec, section, color, status]
    # appendRow(newData)

