from datetime import datetime
import time
from time import sleep
import datetime
# from turtle import color
import sim
from urllib import response
import requests
import json
import generateDB
import urllib3
http    = urllib3.PoolManager()

def ActuatorPushPull(num): #send actuator an act
    # Activete
    time.sleep(0.1)
    data_json = {"action" : 1}
    data_encode = json.dumps(data_json).encode("utf-8")

    res = http.request("Post",
                        f"http://localhost/tss/0/actuator/{num}",
                        body=data_encode,
                        headers={"content-Type" : "application/json"})
    #text = res.data.decode("utf-8")
    #print(text)
    print(f'Activate Actuator at Sensor #{num}')
    sleep(0.5)
      
    # Deactivate
    data_json = {"action" : 0}     
    data_encode = json.dumps(data_json).encode("utf-8")

    res = http.request("POST",
                            f"http://localhost/tss/0/actuator/{num}",
                            body=data_encode,
                            headers={"Content-Type" : "application/json"})
    
    #text    = res.data.decode("utf-8")
    #print(text)
    print(f'Deactivate Actuator at Sensor #{num}')
    sleep(0.2)
    
def ActuatorByColor(color):
    if(color == "GREEN"):
        ActuatorPushPull(0)
    elif(color == "BLUE"):
        sleep(1.3)
        ActuatorPushPull(1)
    elif(color == "RED"):
        sleep(2.5)
        ActuatorPushPull(2)
    elif(color == "YELLOW"):
        ActuatorPushPull(0)
    elif(color == "PURPLE"):
        sleep(1.3)
        ActuatorPushPull(1)

def ActuatorGet():
    data_json = {"action" : 1}
    data_encode = json.dumps(data_json).encode("utf-8")

    res = http.request("GET",
                        f"http://localhost/tss/0/actuator/4",
                        body=data_encode,
                        headers={"content-Type" : "application/json"})
    text = res.data.decode("utf-8")
    print(text)