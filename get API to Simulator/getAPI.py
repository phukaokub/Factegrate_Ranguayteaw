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
import PostActuator
import urllib3
http    = urllib3.PoolManager()
delay = 0
global num
global color 
color = ""

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
    responseAPI = http.request("GET",
                              "http://localhost/tss/0/sensor/10")
    data    = responseAPI.data.decode("utf-8")
    parseJson = json.loads(data)

    color =  parseJson['value']
    # delay = 1.055
    # transferData(activeCase)
    #print('Color : ',activeCase)
    return color

def getDataFromAPI(num) : # Get position previous Box by Sensor #num
    i=i%2
    global delay, color
    responseAPI = http.request("GET",
                              f"http://localhost/tss/0/sensor/{num}")
    data    = responseAPI.data.decode("utf-8")
    parseJson = json.loads(data)

    activeCase =  parseJson['value']
    
    if(activeCase == 1) : # If sensor detected --> insert new box
        # color = generateDB.getData()
        color = getColorNewBox()
        #transferData(color)

        print(f'Delay : {delay}')
        print(f'Sensor #{num} : {activeCase}')
        print(f'Color : {color}')

        # getLatency()
        PostActuator.ActuatorByColor(color)
        # getLatency()

        generateDB.sorted(color)
        print('Finish!\n')
        time.sleep(0.5)
    if(i==1):
        PostActuator.ActuatorGet()
    i+=1
    time.sleep(1)

def getLatency(): # Check latency between API and TeleSort
    global delay
    responseAPI = http.request("GET",
                              f"http://localhost/tss/0/latency")
    data    = responseAPI.data.decode("utf-8")
    parseJson = json.loads(data)

    latency = parseJson['value']
    unit = parseJson['unit']
    print(f'Latency = {latency} {unit}')

while(True):
    # print('Scanning...')
    i=0
    getDataFromAPI(0)
    # time.sleep(delay)

