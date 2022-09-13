import time
from time import sleep
import sim
from datetime import datetime
import json
import urllib3
import RanGuayTaewAPI
http = urllib3.PoolManager()
delay = 0
haveOrder = False

def getLatency(): # Check latency between API and TeleSort
    global delay
    responseAPI = http.request("GET",
                              f"http://localhost/tss/0/latency")
    data    = responseAPI.data.decode("utf-8")
    parseJson = json.loads(data)

    latency = parseJson['value']
    unit = parseJson['unit']
    print(f'Latency = {latency} {unit}')

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

def ActuatorPushPull(num, delay): # push and pull actuator
    # Activate
    time.sleep(delay)
    data_json = {"action" : 1}
    data_encode = json.dumps(data_json).encode("utf-8")
    ts = time.time()
    res = http.request("Post",
                        f"http://localhost/tss/0/actuator/{num}",
                        body=data_encode,
                        headers={"content-Type" : "application/json"})
    #text = res.data.decode("utf-8")
    #print(text)
    afterPost1 = time.time() - ts
    print(f'Activate Actuator at Sensor #{num} Time = {afterPost1}')
    sleep(0.35)
      
    # Deactivate
    data_json = {"action" : 0}     
    data_encode = json.dumps(data_json).encode("utf-8")
    ts = time.time()
    res = http.request("POST",
                            f"http://localhost/tss/0/actuator/{num}",
                            body=data_encode,
                            headers={"Content-Type" : "application/json"})
    
    #text    = res.data.decode("utf-8")
    #print(text)
    afterPost2 = time.time() - ts
    print(f'Deactivate Actuator at Sensor #{num} Time = {afterPost2}')
    sleep(0.2)

def getDataFromAPI(num) : # Get position previous Box by Sensor #num
    global delay, haveOrder
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
        if (haveOrder and currentOrder[color.lower()] > 0):
            # don't push
            currentOrder[color.lower()] -= 1
            requiredBox = currentOrder['purple'] + currentOrder['green']  + currentOrder['red'] + currentOrder['blue'] + currentOrder['yellow']
            print(f'>>>>>>>> Require : {requiredBox}')
            if (requiredBox == 0): # if all color is sorted > set success & get new order
                haveOrder = False
                RanGuayTaewAPI.setOrderStatus(currentOrder['rowid'], 'success')
            
            status = 'Sorted'
        else:
            # push actuator number 2
            ts = time.time()
            # ActuatorPushPull(2, 2.5)
            ActuatorPushPull(0, 0)
            afterAct = time.time() - ts
            print(f'Time Used: {afterAct}')
            # TestActuatorPushPull(2)
            status = 'Unsorted'

        # update database
        updateNewBox(color, status)

        print('Finish!\n')

    time.sleep(0.5)

def genTSS(): # generate fake TSS API data
    import random
    activeCase = random.randint(0, 1)
    if (activeCase == 1):
        color = random.choice(('PURPLE', 'GREEN', 'RED', 'BLUE', 'YELLOW'))
    else:
        color = ''
    return activeCase, color

def TestActuatorPushPull(num): # for testing 
    print(f'########\nActivate Actuator at Sensor #{num}')
# c = 0

printCheck = False

while(True):
    ########################################################
    # generate fake data & insert new data
    # activeCase, color = genTSS()
    # if (c < 10): print('waiting... ' + str(c))
    # if (c == 10):
    #     RanGuayTaewAPI.sendUserData('Phukao', 0, 3, 2, 0, 0, 'waiting')
    #     print(RanGuayTaewAPI.getUserData())
    #     printCheck = True
    # if (c == 20):
    #     RanGuayTaewAPI.sendUserData('Tin', 1, 0, 2, 3, 0, 'waiting')
    #     print(RanGuayTaewAPI.getUserData())
    #     printCheck = True
    ########################################################

    if (not haveOrder): # check for new order
        currentOrder = RanGuayTaewAPI.getNewOrder()

    if (currentOrder): # if there is on-going order = have order
        ##########################################
        if (printCheck):
            print(RanGuayTaewAPI.getUserData())
            printCheck = False
        ##########################################
        haveOrder = True

    # get new box
    # getDataFromAPI(0, activeCase, color)
    getDataFromAPI(0)
    # c += 1

