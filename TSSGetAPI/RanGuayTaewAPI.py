import urllib3
import json

http = urllib3.PoolManager()
url = "http://localhost:8080"

def getUserData():
    response = http.request("GET", 
                            url+'/user')
    parseJson = json.loads(response.data)

    #print(parseJson[0]['user'])
    return parseJson

def getSortingSystemData():
    response = http.request("GET", 
                            url+'/sorting-system')
    parseJson = json.loads(response.data)

    #print(parseJson[0]['user'])
    return parseJson

def sendUserData(id, user, time, purple, green, red, blue, yellow, status):
    data = {
        "id"        : id, 
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
    #print(json.loads(response.data)['lastInsertRowid'])

def sendSortingSystemData(id, year, month, day, hour, min, sec, section, color, status):
    data = {
        "id"        : id, 
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

id, user, time, purple, green, red, blue, yellow, status = 14, 'Test', '16:00:01', 0, 5, 9, 13, 0, 'waiting'
sendUserData(id, user, time, purple, green, red, blue, yellow, status)
print(getUserData())

# id, year, month, day, hour, min, sec, section, color, status = 2, 2022, 6, 19, 12, 20, 3, 'Noodle Sorting', 'RED', 'Sorted'
# sendSortingSystemData(id, year, month, day, hour, min, sec, section, color, status)
# print(getSortingSystemData())