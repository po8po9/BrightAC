#!/usr/bin/env python
# coding=utf-8
import subprocess
import time

class BrightnessScale:
    def __init__(self):
        # get active monitor and current brightness
        self.monitor = self.getActiveMonitor()
        self.currB = self.getCurrentBrightness()


    def initStatus(self):
        if(self.monitor == "" or self.currB == ""):
            return False
        return True

    def getActiveMonitor(self):
        #Find display monitor
        monitor = subprocess.check_output("xrandr -q | grep ' connected' | cut -d ' ' -f1", shell=True)
        if(monitor != ""):
            monitor = monitor.split('\n')[0]
        return monitor

    def getCurrentBrightness(self):
        #Find current brightness
        currB = subprocess.check_output("xrandr --verbose | grep -i brightness | cut -f2 -d ' '", shell=True)
        if(currB != ""):
            currB = currB.split('\n')[0]
            currB = int(float(currB) * 100)
        else:
            currB = ""
        return currB

    def ac_daemon(self):
        estado=subprocess.check_output ("acpi -a | cut -d ':' -f2", shell=True)

        if estado.find("on-line") != -1:
            ac_on=1  
        else:
            ac_on=0
        
        return ac_on

    



    def bjr_brillo(self, op):
        #Change brightness
        if op==1:
            newBrightness = float(90)/100
            newBacklight= int(25)
        else:
            newBrightness = float(100)/100
            newBacklight= int(92)

        cmdb = "xrandr --output %s --brightness %.2f" % (self.monitor, newBrightness)
        cmdB = "xrandr --output %s --set BACKLIGHT %d" % (self.monitor,newBacklight) 
        cmdbStatus = subprocess.check_output(cmdb, shell=True)
        cmdBStatus = subprocess.check_output(cmdB, shell=True)
        
if __name__ == "__main__":
   
    brcontrol=BrightnessScale ()
    while brcontrol.initStatus():
            while True:
                if brcontrol.ac_daemon() == 0:
                    brcontrol.bjr_brillo(1)
                    break
                else: 
                    brcontrol.bjr_brillo(2)
           




