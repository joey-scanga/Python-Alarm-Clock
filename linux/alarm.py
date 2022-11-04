import time, json, subprocess
from datetime import datetime
from playsound import playsound
from tkinter import *

currentAlarms = []
currentTime = None
timeFormatStr = "%H:%M:%S"
defaultSoundPath = "data/sounds/sound1.wav"

running = True

def init():
    initAlarms()
    updateCurrentTime()

def initAlarms():
    alarmFile = open("data/alarms.json", "r")
    alarmData = json.load(alarmFile)

    for alarm in alarmData["data"]:
        currentAlarms.append(alarm)
        if alarm.get("intervals"):
            for interval in alarm.get("intervals"):
                currentAlarms.append(interval)

    print(currentAlarms)

def stopClock():
    global running
    running = False

def startClock():
    global running
    running = True

def resetClock():
    stopClock()
    init()

def updateCurrentTime():
    while(running):
        currentTime = time.strftime(timeFormatStr)
        for alarm in currentAlarms:
            if(alarm.get("alarmTime") == currentTime):
                createAlert(alarm)
        time.sleep(1)

def createAlert(alarm):
    dt = datetime.now()
    weekday = alarm.get("weekday")
    if(weekday and weekday != dt.weekday()):
        return
    alertMethod = alarm.get("alertMethod")
    if alertMethod == "sound":
        playsound(defaultSoundPath)
    elif alertMethod == "screensound":
        playsound(defaultSoundPath)
        drawAlertScreen(alarm.get("alarmTitle"))
    elif alertMethod == "screen":
        drawAlertScreen(alarm.get("alarmTitle"))

def drawAlertScreen(text):
    root = Tk()
    root.configure(bg='Black')
    root.geometry("600x600")
    root.wm_title("Alarm went off!")

    app = Frame(root)

    text = Label(root, text=text, fg="White", bg="Black", font=("Helvetica", 16))
    text.pack()
    app.mainloop()

init()

