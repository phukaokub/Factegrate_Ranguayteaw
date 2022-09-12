from argparse import Action
from datetime import datetime
import time
from time import sleep
import datetime
# from turtle import color
import sim
from urllib import response
import json
import generateDB
import PostActuator
import urllib3
import RanGuayTaewAPI
http    = urllib3.PoolManager()
delay = 0
global num
global color 
color = ""
i = 0
haveOrder = False

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
    return color

def getDataFromAPI(num) : # Get position previous Box by Sensor #num
    global delay, color, i, haveOrder
    responseAPI = http.request("GET",
                              f"http://localhost/tss/0/sensor/{num}")
    data    = responseAPI.data.decode("utf-8")
    parseJson = json.loads(data)

    activeCase =  parseJson['value']
    
    if(activeCase == 1) : # If sensor detected --> insert new box
        color = getColorNewBox()
        # transferData(color) # send data to simulator

        print(f'Delay : {delay}')
        print(f'Sensor #{num} : {activeCase}')
        print(f'Color : {color}')

        # check if there is order AND current color is required
        if (haveOrder and currentOrder[color] > 0):
            PostActuator.ActuatorByColor(color)
            currentOrder[color] -= 1
            if (): # if all color is sorted > set success & get new order
                haveOrder = False
                RanGuayTaewAPI.setOrderStatus(currentOrder['id'], 'success')
            
        # update database

        print('Finish!\n')
        time.sleep(0.5)
    # if(i==1):
    #     PostActuator.ActuatorGet()
    #     i=0
    # i+=1
    time.sleep(0.5)


def getLatency(): # Check latency between API and TeleSort
    global delay
    responseAPI = http.request("GET",
                              f"http://localhost/tss/0/latency")
    data    = responseAPI.data.decode("utf-8")
    parseJson = json.loads(data)

    latency = parseJson['value']
    unit = parseJson['unit']
    print(f'Latency = {latency} {unit}')

RanGuayTaewAPI.initID()
while(True):
    # print('Scanning...')
    # i=0
    if (not haveOrder): # check for new order
        currentOrder = RanGuayTaewAPI.getNewOrder()

    if (currentOrder): # if there is on-going order
        haveOrder = True
            
           
    # getDataFromAPI(0)
    # time.sleep(delay)

