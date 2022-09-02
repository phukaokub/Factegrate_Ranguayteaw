from datetime import datetime
import time
import datetime
from turtle import color
import sim
from urllib import response
import requests
import json
import generateDB
import urllib3
http    = urllib3.PoolManager()

def Actuator(color): #send actuator an act
    # Activete
    data_json = {"action" : 1}
    data_encode = json.dumps(data_json).encode("utf-8")

    res = http.request("Post",
                        "http://localhost/tss/0/actuator/0",
                        body=data_encode,
                        headers={"content-Type" : "application/json"})
    text = res.data.decode("utf-8")
    print(text)

    sleep(1)

    # Deactivate
    data_json = {"action" : 0}


# def getCOlor()
