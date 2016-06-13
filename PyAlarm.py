
# BUGS / TO DO
# -Do not allow timer seconds to be set to more than 59
# -Do not allow any characters except numbers


# Logging
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("Starting PyAlarm")
# Set log level by adjusting level=logging.LEVEL
# Logging levels are: CRITICAL, ERROR, WARNING, INFO, DEBUG

from tkinter import *
from tkinter import ttk
import time
from subprocess import call
from datetime import datetime
from datetime import timedelta
import _thread

def alarmWindow():
    # Alarm Dialog
    logging.debug("Opening alarm dialog")
    global alarmDialog
    alarmDialog = Toplevel()
    alarmDialog.title("Alarm")
    alarmDialog.focus_set()
    
    global alarmTime
    alarmTime = StringVar()
    
    ttk.Label(alarmDialog, text="Alarm", font=("default","20")).grid(column=1, row=1, sticky=W)
    newAlarmTimeEntry = ttk.Entry(alarmDialog, width=16, textvariable=alarmTime)
    newAlarmTimeEntry.grid(column=2, row=2, sticky=(W, E))

    #ttk.Label(configArea, text="Name:").grid(column=3, row=2, sticky=W)
    ttk.Label(alarmDialog, text="Time (dd.mm.yyyy HH:MM):").grid(column=1, row=2, sticky=W)
    #newAlarmTimeEntry.focus()

    saveButton = ttk.Button(alarmDialog, text="Set", command=setAlarm)
    saveButton.grid(column=1, row=3, sticky=(S, E))
    
    for child in alarmDialog.winfo_children(): child.grid_configure(padx=5, pady=5)

    
    

def timerWindow():
    # Timer Dialog
    logging.debug("Opening timer dialog")
    global timerDialog
    timerDialog = Toplevel()
    timerDialog.title("Timer")
    timerDialog.focus_set()
    
    global newTimer
    newTimer = StringVar()
    
    #ttk.Label(timerDialog, text="Set Timer").grid(column=1, row=1, sticky=W)
    
    #timerLabel = ttk.Label(timerDialog, text=timer)
    #timerLabel.grid(column=2, row=2, sticky=W)
    
    newTimer = StringVar()
    timerEntry = ttk.Entry(timerDialog, width=20, textvariable=newTimer)
    timerEntry.grid(column=1, row=1, sticky=(W))
    
    setTimerButton = ttk.Button(timerDialog, text="Set", command=setTimer)
    setTimerButton.grid(column=2, row=1, sticky=(W))
    timerDialog.bind('<Return>', setTimer)
    def cancel():
        timerDialog.destroy()
    
    ttk.Button(timerDialog, text="Cancel", command=cancel).grid(column=1, columnspan=2, row=2)
    
    for child in timerDialog.winfo_children(): child.grid_configure(padx=5, pady=5)

def setTimer(*args):
    # Function for setting a timer and playing sound.mp3 when done.
    
    # Close dialog
    timerDialog.destroy()
    
    logging.debug("setTimer() started")
    timerStartTime = time.strftime("%H:%M:%S")
    logging.debug("Now is {}".format(timerStartTime))
    
    # get duration in mm:ss format
    timerDuration = str(newTimer.get())
    # split duration into minutes and secinds
    logging.debug("raw timerDuration is {}".format(timerDuration))
    # split into list
    timerDurationList = timerDuration.split(':')
    timerDurationMinutes = timerDurationList[0]
    timerDurationSeconds = timerDurationList[1]
    logging.debug("timerDurationMinutes is {}".format(timerDurationMinutes))
    logging.debug("timerDurationSeconds is {}".format(timerDurationSeconds))
    
    # convert minutes to seconds
    # first convert from str to int though
    timerDurationMinutes = int(timerDurationMinutes)
    timerDuration = timerDurationMinutes * 60
    logging.debug("timerDurationMinutes is {} in seconds".format(timerDuration))
    # convert seconds from str to int
    timerDurationSeconds = int(timerDurationSeconds)
    timerDuration = timerDuration + timerDurationSeconds
    logging.debug("timerDuration total is {}".format(timerDuration))

    #timerStartTime = time.strftime("%H:%M:%S")
    #logging.debug("Now is {}".format())
    # Convert to int for timedelta
    #timerDuration = int(timerDuration)
    timerFinish = datetime.now() + timedelta(seconds=timerDuration)
    logging.debug("timerFinish is {}".format(timerFinish))
    # Convert the format of timerFinish from yyyy-MM-DD hh:mm:ss.µµµµµµ to hh:mm:ss:
    # grab character 11 to 19
    timerFinish = format(timerFinish)
    timerFinish = timerFinish[11:19]
    logging.debug("Timer wil finsh at {}".format(timerFinish))
    timerLabel.config(text=timerFinish)

    # Wait for timer to finish
    #import _thread
    
    def waitForAlarm():
        logging.debug("Waiting for alarm to finish in new thread")
        for x in range(1, timerDuration):
            time.sleep(1)
        else:
            logging.info("Timer done!")
            timerLabel.config(text="Done!")
            logging.debug("Playing sound")
            call(["cvlc","-R","sound.mp3"])
            logging.debug("Done playing sound")
    
    _thread.start_new_thread(waitForAlarm, ())
    
def stopTimer():
    logging.info("Stopping timer")
    call(["killall","vlc"])
    logging.debug("Timer stopped.")

def about():
        # Display information about PyAlarm
        logging.debug("About menu item clicked")
        aboutWindow = Toplevel(root)
        ttk.Label(aboutWindow, text="PyAlarm v. 0.1").grid(column=1, row=1)
        Message(aboutWindow, width=350, justify=CENTER, text="Copyright (c) 2016 Till von Elling <till@tillvonelling.ddns.net>\nPyAlarm is released under the terms of the GNU GPL v.3.0").grid(column=1, row=2)
        #Message(aboutWindow, width=350, justify=CENTER, text="Some code is copyright (c) vegaseat from daniweb.com. This is marked in the source code. If you don't want me to use your code plaease contact me.").grid(column=1, row=3)
        def openLicense():
                logging.debug("Opening license in browser")
                import webbrowser
                webbrowser.open("COPYING.html")

        ttk.Button(aboutWindow, text="View License", command=openLicense).grid(column=1, row=4)
        for child in aboutWindow.winfo_children(): child.grid_configure(padx=5, pady=5)


def exit():
    # Exit
    logging.info("Exit. Have a nice day!")
    quit(0)

root = Tk()
root.title("PyAlarm")
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
#root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w, h))
# Menu bar
# disbale dotted lines
root.option_add('*tearOff', FALSE)

######################################
#Create menu
######################################
menu = Menu(root)
root.config(menu=menu)
PyAlarmMenu = Menu(menu)
PyAlarmMenu.add_command(label="About", command=about)
PyAlarmMenu.add_command(label="Exit", command=exit)
menu.add_cascade(label="PyAlarm", menu=PyAlarmMenu)

menu.add_command(label="Timer", command=timerWindow)

menu.add_command(label="Alarm", command=alarmWindow)

######################################
#Set main window padding, resizing, etc
######################################

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)


# CLOCK
clockArea = Frame(mainframe)
clockArea.grid(column=1, row=2)

# The following was modified from https://www.daniweb.com/programming/software-development/code/216785/tkinter-digital-clock-python
time1 = ''
clock = Label(clockArea, fg="black", font=('default', 119, 'bold'))
clock.pack(fil=BOTH, expand=1)

def tick():
    global time1
    # get the current local time from the PC
    time2 = time.strftime('%H:%M:%S')
    # if time string has changed, update it
    if time2 != time1:
        time1 = time2
        clock.config(text=time2)
    # calls itself every 200 milliseconds
    # to update the time display as needed
    # could use >200 ms, but display gets jerky
    clock.after(200, tick)

tick()
# End of modified code from https://www.daniweb.com/programming/software-development/code/216785/tkinter-digital-clock-python

# TIMER / ALARM
configArea = Frame(mainframe)
configArea.grid(column=1, row=3)
# TIMER AREA

timer = '--:--'
ttk.Label(configArea, text="Timer", font=("default","20")).grid(column=1, row=1, sticky=W)
timerLabel = ttk.Label(configArea, text=timer)
timerLabel.grid(column=1, row=2, sticky=W)
cancelTimerButton = ttk.Button(configArea, text="Stop", command=stopTimer)
cancelTimerButton.grid(column=2, row=2, sticky=(W))
# Spacer
ttk.Label(configArea, text="                         ").grid(column=3, row=1)

# ALARM AREA

def setAlarm(*args):
    
    # Close dialog
    alarmDialog.destroy()
    
    alarmTime2 = str (alarmTime.get())
    #alarmTime2 = "01.07.2016 23:59"
    logging.debug("Setting alarm at " + alarmTime2)
    global alarm
    alarmLabel.config(text=alarmTime2)
    now = datetime.now()
    logging.debug("Now is {}".format(now))
    alarmTimeObject = datetime.strptime(alarmTime2, '%d.%m.%Y %H:%M')
    logging.debug("alarmTimeObject is {}".format(alarmTimeObject))
    timeLeft = alarmTimeObject - now
    logging.debug("timeLeft is {}".format(timeLeft))
    secondsLeft = timeLeft.total_seconds()
    # Get rid of decimals
    secondsLeft = int(round(secondsLeft))
    logging.debug("secondsLeft is {}".format(secondsLeft))
    
    def waitForAlarm():
        logging.debug("Waiting for {} in new thread".format(secondsLeft))
        for x in range(1, secondsLeft):
            time.sleep(1)
        else:
            logging.info("Arrr, all hands on deck!")
            alarmLabel.config(text="Done!")
            logging.debug("Playing sound")
            call(["cvlc","-R","sound.mp3"])
            logging.debug("Done playing sound")
    
    _thread.start_new_thread(waitForAlarm, ())
    

alarm  = '--.--.-- --:--'

ttk.Label(configArea, text="Alarm", font=("default","20")).grid(column=4, row=1, sticky=W)

alarmLabel = ttk.Label(configArea, text=alarm)
alarmLabel.grid(column=4, row=2, sticky=W)

ttk.Button(configArea, text="Stop", command=stopTimer).grid(column=5, row=2)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
for child in configArea.winfo_children(): child.grid_configure(padx=5, pady=5)

root.mainloop()