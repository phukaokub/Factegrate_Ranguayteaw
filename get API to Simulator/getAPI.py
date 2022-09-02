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
delay = 0

def transferData(color) : # transfer data in API to CoppeliaSim
    sim.simxFinish(-1)
    clientID = sim.simxStart('127.0.0.1',19997,True,True,5000,5)
    inputInts = []
    inputFloats = []
    inputStrings = color
    inputBuffer = bytearray()
    res,retInts,retFloats,retStrings,retBuffer = sim.simxCallScriptFunction(clientID,'ConveyorBelt',sim.sim_scripttype_childscript,'fromPython',inputInts,inputFloats,inputStrings,inputBuffer,sim.simx_opmode_blocking)
    

def getColorNewBox() : # Get color from Sensor #10
    global delay
    responseAPI = requests.get('http://localhost/tss/0/sensor/10')
    #print(response_API.status_code)

    data = responseAPI.text
    parseJson = json.loads(data)

    activeCase =  parseJson['value']
    delay = 1.055
    transferData(activeCase)
    print('Color : ',activeCase)

    

def getDataFromAPI(num) : # Get position previous Box by Sensor #num
    global delay
    responseAPI = http.request("GET",
                                f"http://localhost/tss/0/sensor/{num}")
    #print(response_API.status_code)

    data    = responseAPI.data.decode("utf-8")
    parseJson = json.loads(data)

    activeCase =  parseJson['value']
    
    if(activeCase == 1) : # If sensor detected --> insert new box
        # getColorNewBox()
        # generateDB.getData()

        print('Delay : ',delay)
        print(f'Sensor #{num} : {activeCase}')
        print('Finish!')
        delay = 0.5
    else :
        delay = 0.5
    # pytime.sleep(1)

def getLatency(): # Check latency between API and TeleSort
    global delay
    responseAPI = requests.get('http://localhost/tss/0/latency')
    #print(responseAPI.text)

    data = responseAPI.text
    parseJson = json.loads(data)

    latency = parseJson['value']
    unit = parseJson['unit']
    print(f'Latency = {latency} {unit}')

def Actuator(color): #send actuator an act
    print()





while(True):
    #now = datetime.datetime.now()
    getDataFromAPI(0)
    #getLatency()
    #usedTime = datetime.datetime.now() - now
    time.sleep(delay)
    #print('Time : ',usedTime)
    # print('Delay : ',delay)
    # print('Finish!')

