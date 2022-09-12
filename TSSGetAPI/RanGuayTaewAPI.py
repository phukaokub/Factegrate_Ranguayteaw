import urllib3
import json

http = urllib3.PoolManager()
url = "http://localhost:8080"

def getUserData():
    response = http.request("GET", 
                            url+'/user')
    try:
        parseJson = json.loads(response.data)

        #print(parseJson[0]['user'])
        return parseJson
    except:
        print('no table')

def getSortingSystemData():
    response = http.request("GET", 
                            url+'/sorting-system')
    parseJson = json.loads(response.data)

    #print(parseJson[0]['user'])
    return parseJson

def getNumRowOfUserData():
    response = http.request("GET", 
                            url+'/user/count')
    try:
        parseJson = json.loads(response.data)
        num = parseJson[0]['COUNT(id)']
        return num
    except:
        print('error')

def getNumRowOfSortingSystemData():
    response = http.request("GET", 
                            url+'/sorting-system/count')
    parseJson = json.loads(response.data)
    num = parseJson[0]['COUNT(id)']
    return num

def sendUserData(user, time, purple, green, red, blue, yellow, status):
    global userID
    data = {
        "id"        : userID, 
        "user"      : user, 
        "time"      : time,
        "purple"    : purple, 
        "green"     : green, 
        "red"       : red,
        "blue"      : blue, 
        "yellow"    : yellow, 
        "status"    : status
    }
    data_json = json.dumps(data)
    response = http.request("POST", 
                            url+'/user',
                            body=data_json,
                            headers={"content-Type" : "application/json"})
    userID += 1
    # print(json.loads(response.data)['lastInsertRowid'])

def sendSortingSystemData(year, month, day, hour, min, sec, section, color, status):
    global sortSysID
    data = {
        "id"        : sortSysID, 
        "year"      : year, 
        "month"     : month, 
        "day"       : day, 
        "hour"      : hour, 
        "min"       : min, 
        "sec"       : sec, 
        "section"   : section, 
        "color"     : color, 
        "status"    : status
    }
    data_json = json.dumps(data)
    response = http.request("POST", 
                            url+'/sorting-system',
                            body=data_json,
                            headers={"content-Type" : "application/json"})
    sortSysID += 1

def initID():
    global userID, sortSysID
    userID = getNumRowOfUserData() + 1
    sortSysID = getNumRowOfSortingSystemData() + 1

def getNewOrder():
    response = http.request("GET", 
                            url+'/user/order')
    try:
        parseJson = json.loads(response.data)
        # print(parseJson)
        order = parseJson[0]
        print(order['id'])
        setOrderStatus(order['id'], 'in-progress')
        return order
    except: # if there is 0 row
        return False
    # return num

def setOrderStatus(id, status):
    response = http.request("POST", 
                            url+'/user/order/'+str(id)+'/'+status)

getNewOrder()
print(getNumRowOfUserData())
#print(getUserData())

# initID()
# user, time, purple, green, red, blue, yellow, status = 'Mek', '16:00:01', 10, 0, 0, 23, 30, 'waiting'
# sendUserData(user, time, purple, green, red, blue, yellow, status)
# print(getUserData())

# year, month, day, hour, min, sec, section, color, status = 2022, 8, 21, 15, 17, 39, 'Noodle Sorting', 'PURPLE', 'Sorted'
# sendSortingSystemData(year, month, day, hour, min, sec, section, color, status)
# print(getSortingSystemData())


