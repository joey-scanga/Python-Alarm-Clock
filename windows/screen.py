from tkinter import *
import subprocess, time, os, signal, json
import alarmsettings

timeFormatStr = "%I:%M:%S %p"
proc = None

root = Tk()
root.configure(bg='Black')
root.geometry("600x600")
root.wm_title("Cool Alarm")

app = Frame(root)

currentWidgets = []

'''Get directory of this file'''
path = os.path.realpath(__file__)
dirpath = os.path.dirname(path)

'''Process Handling (home screen)'''
def closeOnlyWindow():
    root.destroy()

def closeEntireApp():
    killAlarmProcess()
    root.destroy()

'''Alarm Subprocess'''
def spawnAlarmProcess():
    global proc
    if os.stat(dirpath+"\.tmp\pid.txt").st_size == 0:
        proc = subprocess.Popen(["python3", dirpath+"\\alarm.py"]) 
        with open(dirpath+"\.tmp\pid.txt", "r+") as f:
            f.write(str(proc.pid))     

def resetAlarmProcess():
    killAlarmProcess()
    spawnAlarmProcess()

def killAlarmProcess():
    if os.stat(dirpath+"\.tmp\pid.txt").st_size != 0:
        with open(".tmp\pid.txt", "r+") as f:
            pid = int(f.read())
            try:
                os.kill(pid, signal.SIGSTOP)
            except:
                pass
            f.truncate(0)

'''Window Creation, Widget Functions'''
def initializeFrame():
    resetAlarmProcess()
    drawHomeScreen()

def createLabel(master, string):
    return Label(master, text=string, fg="White", bg="Black", font=("Helvetica", 16))

def createButton(master, string, function):
    return Button(master, text=string, command=function, activeforeground="Black",
        activebackground="White", fg="White", bg="Black", padx="20",
            pady="10", anchor="center", width=20)

def clearWidgets():
    for widget in currentWidgets:
        if widget:
            widget.destroy()

'''Home Screen'''
def drawHomeScreen():
    clearWidgets()
    addAlarmBtn = createButton(root, "Add Alarm", drawAddAlarm) 
    addAlarmBtn.pack(ipady="10")
    editAlarmsBtn = createButton(root, "Edit Alarms", drawEditAlarms)
    editAlarmsBtn.pack(ipady="10")
    closeOnlyWindowBtn = createButton(root, "Close This Window", closeOnlyWindow)
    closeOnlyWindowBtn.pack(ipady="10")
    closeEntireAppBtn = createButton(root, "Close Entire App", closeEntireApp)
    closeEntireAppBtn.pack(ipady="10")


    currentWidgets.append(addAlarmBtn)
    currentWidgets.append(editAlarmsBtn)
    currentWidgets.append(closeOnlyWindowBtn)
    currentWidgets.append(closeEntireAppBtn)

'''Add Alarm Screen'''
def constructMinSbxValues():
    values = []

    for i in range(60):
        if i < 10:
            values.append("0"+str(i))

        else:
            values.append(str(i))

    return values

def constructHourSbxValues():
    values = []

    for i in range(1, 13):
        if i < 10:
            values.append("0"+str(i))

        else:
            values.append(str(i))

    return values
def drawAddAlarm():
    clearWidgets()

    backBtn = createButton(root, "Back", drawHomeScreen)
    backBtn.pack()

    #Alarm title section
    global alarmTitleVar
    alarmTitleVar = StringVar()
    alarmTitleFrame = Frame(root, width="200", bg="Black")
    alarmTitleFrame.pack()
    alarmTitleLbl = createLabel(alarmTitleFrame, "Alarm Name: ").grid(row=0, column=0)
    alarmTitleEnt = Entry(alarmTitleFrame, width="30", textvariable=alarmTitleVar).grid(row=0, column=1)

    #Choose time section
    global ampmVar, hourVar, minVar
    ampmVar = IntVar()
    hourVar = StringVar()
    minVar = StringVar()
    
    chooseTimeFrame = Frame(root, width="200", bg="Black")
    chooseTimeFrame.pack()

    chooseTimeLbl = createLabel(chooseTimeFrame, "Choose Time: ")
    chooseTimeLbl.grid(row=0, column=0, ipady="10")

    hourSbx = Spinbox(chooseTimeFrame, bg="Black", fg="White", width="5", textvariable=hourVar, from_=1, to=12, values=constructHourSbxValues())
    colonLbl = createLabel(chooseTimeFrame, ":")
    minSbx = Spinbox(chooseTimeFrame, bg="Black", fg="White", width="5", textvariable=minVar, from_=0, to=59, values=constructMinSbxValues())

    hourSbx.grid(row=0, column=1, ipady="10")
    colonLbl.grid(row=0, column=2, ipady="10")
    minSbx.grid(row=0, column=3, ipady="10")
    amRad = Radiobutton(chooseTimeFrame, text="AM", variable=ampmVar, value=1).grid(row=0, column=4)
    pmRad = Radiobutton(chooseTimeFrame, text="PM", variable=ampmVar, value=2).grid(row=0, column=5)
    
    #Intervals frame
    global intervalnVar, inthourVar, intminVar
    intervalnVar = StringVar()
    inthourVar = StringVar()
    intminVar = StringVar()

    intervalFrame = Frame(root, width="200", bg="Black") 
    intervalFrame.pack()
    chooseIntervalnLbl = createLabel(intervalFrame, "No. of intervals: ")
    chooseIntervalnLbl.grid(row=0, column=0)
    chooseIntervalnSbx = Spinbox(intervalFrame, textvariable=intervalnVar, bg="Black", fg="White", width="5", from_=0, to=100)
    chooseIntervalnSbx.grid(row=0, column=1)
    chooseIntervaltLbl = createLabel(intervalFrame, "Length of intervals (hours, minutes):")
    chooseIntervaltLbl.grid(row=1, column=0)
    inthourSbx = Spinbox(intervalFrame, textvariable=inthourVar, bg="Black", fg="White", width="5", from_=1, to=12, values=constructHourSbxValues())
    intcolonLbl = createLabel(intervalFrame, ":")
    intminSbx = Spinbox(intervalFrame, textvariable=intminVar, bg="Black", fg="White", width="5", from_=0, to=59, values=constructMinSbxValues())
    inthourSbx.grid(row=1, column=1)
    intcolonLbl.grid(row=1, column=2)
    intminSbx.grid(row=1, column=3)

    #Alert type frame
    global alertTypeVar
    alertTypeVar = IntVar()
    alertFrame = Frame(root, width="200", bg="Black")
    alertFrame.pack()
    alertTypeLbl = createLabel(alertFrame, "Type of alert: ")
    alertTypeLbl.grid(row=0, column=0)
    soundRad = Radiobutton(alertFrame, text="Sound", variable=alertTypeVar, value=1).grid(row=0, column=1)
    screenRad = Radiobutton(alertFrame, text="Screen", variable=alertTypeVar, value=2).grid(row=0, column=2)
    soundscreenRad = Radiobutton(alertFrame, text="Sound+Screen", variable=alertTypeVar, value=3).grid(row=0, column=3)

    #Submit button
    createAlarmBtn = createButton(root, "Create Alarm", createAlarm) 
    createAlarmBtn.pack()

    #append to currentWidgets
    currentWidgets.append(backBtn)
    currentWidgets.append(alarmTitleFrame)
    currentWidgets.append(alarmTitleLbl)
    currentWidgets.append(alarmTitleEnt)
    currentWidgets.append(chooseTimeLbl)
    currentWidgets.append(chooseTimeFrame)
    currentWidgets.append(hourSbx)
    currentWidgets.append(colonLbl)
    currentWidgets.append(minSbx)
    currentWidgets.append(amRad)
    currentWidgets.append(pmRad)
    currentWidgets.append(intervalFrame)
    currentWidgets.append(chooseIntervalnLbl)
    currentWidgets.append(chooseIntervalnSbx)
    currentWidgets.append(chooseIntervaltLbl)
    currentWidgets.append(inthourSbx)
    currentWidgets.append(intcolonLbl)
    currentWidgets.append(intminSbx)
    currentWidgets.append(alertFrame)
    currentWidgets.append(alertTypeLbl)
    currentWidgets.append(soundRad)
    currentWidgets.append(screenRad)
    currentWidgets.append(soundscreenRad)
    currentWidgets.append(createAlarmBtn)

def createAlarm():
    alarmData = [alarmTitleVar.get(), hourVar.get(), minVar.get(), ampmVar.get(), intervalnVar.get(), inthourVar.get(), intminVar.get(), alertTypeVar.get()] 
    #construct readable time string

    hour = int(hourVar.get())
    if hour == 12:
        if ampmVar.get() != 2:
            hour = 0
    else:
        if ampmVar.get() == 2:
            hour = hour + 12
    if hour < 10:
        hour = "0"+str(hour)
    else:
        hour = str(hour)
            
    timeStr = hour+":"+minVar.get()+":"+"00"

    #construct readable alert setting
    if alertTypeVar == 1:
        alertType = "sound"
    elif alertTypeVar == 2:
        alertType = "screen"
    else: 
        alertType = "screensound"

    #construct readable interval time
    initialTime = timeStr
    intervaln = int(intervalnVar.get())
    intervalt = inthourVar.get()+":"+intminVar.get()+":"+"00"
    intervalList = alarmsettings.constructIntervals({"initialTime": initialTime, "intervaln": intervaln, "intervalt": intervalt, "alertType": alertType})
    
    alarmObj = alarmsettings.constructAlarmObj(alarmTitleVar.get(), timeStr, alertType, intervalList)
    alarmsettings.addAlarm(alarmObj)
    resetAlarmProcess()

def drawEditAlarms():
    clearWidgets()

    backBtn = createButton(root, "Back", drawHomeScreen)
    backBtn.pack()

    with open(dirpath+"\data\\alarms.json", "r") as alarmFile:
        alarms = json.load(alarmFile)
    
    for alarm in alarms["data"]:
        print(alarm)
        indAlarmFrame = Frame(root, bg="Black")
        indAlarmFrame.pack() 
        currentWidgets.append(indAlarmFrame)
        alarmLbl = createLabel(indAlarmFrame, alarm["alarmTitle"]+"\t"+alarm["alarmTime"])
        alarmLbl.grid(row=0, column=0)
        currentWidgets.append(alarmLbl)
        removeAlarmBtn = createButton(indAlarmFrame, "Remove", lambda: removeAlarmFromList(alarm))
        removeAlarmBtn.grid(row=0, column=1)
        currentWidgets.append(removeAlarmBtn)
    '''add to currentWidgets'''
    currentWidgets.append(backBtn)

def removeAlarmFromList(alarmObj):
    alarmsettings.removeAlarm(alarmObj)
    drawEditAlarms()


initializeFrame()
app.mainloop()
