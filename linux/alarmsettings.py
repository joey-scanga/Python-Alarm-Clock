import json, os, shutil


'''Get directory of this file'''
path = os.path.realpath(__file__)
dirpath = os.path.dirname(path)

def constructIntervals(intervalArgs):
    time = intervalArgs.get("initialTime").split(":")
    timeInterval = intervalArgs.get("intervalt").split(":")
    for i in range(0, len(time)):
        time[i] = int(time[i])
        timeInterval[i] = int(timeInterval[i])
    intervalList = [] #replace with alarm["intervals"] = []

    for i in range(0, intervalArgs.get("intervaln")):
       time[0] += timeInterval[0]
       if(time[0] >= 24):
           time[0] %=  24
       time[1] += timeInterval[1]
       if(time[1] >= 60):
           addToHour = time[1] // 60
           time[0] += addToHour 
           time[0] %= 24
           time[1] %= 60
       time[2] += timeInterval[2]
       if(time[2] >= 60):
           addToHour = time[2] // (60 * 24)
           time[0] += addToHour
           time[0] %= 24
           addToMin = time[2] // 60
           time[1] += addToMin
           time[1] %= 60
           time[2] %= 60
       for j in range(len(time)):
           timeStr = str(time[j])
           if time[j] < 10:
               time[j] = "0"+timeStr
           else:
               time[j] = timeStr
              
       intervalList.append({"alarmTime": time[0]+":"+time[1]+":"+time[2], "alertType": intervalArgs.get("alertType")})
       for j in range(len(time)):
           time[j] = int(time[j])
        
    return intervalList

def constructAlarmObj(alarmTitle, alarmTime, alertMethod, intervals):
    alarmObj = {}
    alarmObj["alarmTitle"] = alarmTitle
    alarmObj["alarmTime"] = alarmTime
    alarmObj["alertMethod"] = alertMethod
    alarmObj["intervals"] = intervals
    return alarmObj 

def addAlarm(alarmObj):
    with open(dirpath+"/data/alarms.json", "r+") as alarmFile:
        alarmData = json.load(alarmFile)
        alarmData["data"].append(alarmObj)
        alarmFile.seek(0)
        json.dump(alarmData, alarmFile, indent = 4)

def removeAlarm(alarmObj):
    with open(dirpath+"/data/alarms.json", "r+") as alarmFile:
        alarmData = json.load(alarmFile)
        for i in range(len(alarmData["data"])):
            if alarmData["data"][i] == alarmObj:
                alarmData["data"].pop(i)
                break
        alarmFile.seek(0)
    with open(dirpath+"/data/new_alarms.json", "w") as newAlarmFile:
        json.dump(alarmData, newAlarmFile, indent = 4)
    shutil.move(dirpath+"/data/new_alarms.json", dirpath+"/data/alarms.json")
    

def removeAlarmWithIndex(index):
    with open(dirpath+"/data/alarms.json", "r+") as alarmFile:
        alarmData = json.load(alarmFile)
        alarmData["data"].pop(index)
        alarmFile.seek(0)
        json.dump(alarmData, alarmFile, indent = 4)

def changeAlarm(alarmObj, newAlarmObj):
    with open(dirpath+"/data/alarms.json", "r+") as alarmFile:
        alarmData = json.load(alarmFile)
        removeAlarm(alarmObj)
        addAlarm(newAlarmObj)
        alarmFile.seek(0)
        json.dump(alarmData, alarmFile, indent = 4)


