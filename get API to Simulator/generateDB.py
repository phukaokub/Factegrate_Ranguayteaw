from datetime import datetime
from urllib import response
import requests
import json
from csv import writer
import urllib3
http = urllib3.PoolManager()

def appendRow(row): # Append data as a new row
    with open('database.csv', 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(row)

def getData(): # Get color from sensor 10
    responseAPI = http.request("GET",
                              f"http://localhost/tss/0/sensor/10")
    data    = responseAPI.data.decode("utf-8")
    parseJson = json.loads(data)

    # Get color
    color =  parseJson['value']
    print(f'Color : {color}')

    # Get date & time
    now = datetime.now()
    year = now.date().year
    month = now.date().month
    day = now.date().day
    print(f'Date : {year} {month} {day}')
    hour = now.time().hour
    min = now.time().minute
    sec = now.time().second
    print(f'Time : {hour} {min} {sec}') 

    # Get factory section
    section = 'Noodle Sorting'

    # Update new data to the next row
    newData = [year, month, day, hour, min, sec, section, color]
    appendRow(newData)

    return color
