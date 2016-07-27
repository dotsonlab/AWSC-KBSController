'''
David Rodriguez

Goal: Continuously looping while to perform valve actions at specified times, 

Inputs: A schedule of events based on entered times.

Outputs: Sequence of events to a screen as they happen. 
daily flow rate data
'''
#An object for events

import datetime
import time

import Adafruit_BBIO.GPIO as GPIO

class Event:
    startTime = datetime.time()
    endTime = datetime.time()
    eventTag = ""
    GPIO.setup("P8_8", GPIO.OUT)#kitchen sink switch
    GPIO.setup("P8_7", GPIO.IN)#kitchen sink closed limit
    GPIO.setup("P8_9", GPIO.IN)#kitchen sink open limit
    GPIO.setup("P8_10", GPIO.OUT)#bathroom sink switch
    GPIO.setup("P8_11", GPIO.IN)#bathroom sink closed limit
    GPIO.setup("P8_14", GPIO.IN)#bathroom sink open limit
    GPIO.setup("P8_12", GPIO.OUT)#shower switch
    GPIO.setup("P8_15", GPIO.IN)#shower closed limit
    GPIO.setup("P8_17", GPIO.IN)#shower open limit
    
    def __init__(self, start, end, tag):
        self.startTime = start
        self.endTime = end
        self.eventTag = tag
    
    def displayEvent(self):
        return "%s - %s %s" % (str(self.startTime), str(self.endTime), self.eventTag)
    
    def storeEvent(self):
        saveEvent = "%s %s %s" % (str(self.startTime), str(self.endTime), self.eventTag)
        return saveEvent
    
    def valveTrigger(self, tag):
        limitCount = 0
        if tag == "kitchen_sink":
            GPIO.output("P8_8", GPIO.HIGH)
        elif tag == "bathroom_sink":
            GPIO.output("P8_10", GPIO.HIGH)
        elif tag == "shower":
            GPIO.output("P8_12", GPIO.HIGH)
        print "%s valve open triggered" % tag
        while not self.Open(tag):
            if limitCount == 5:
                limitCount = 0
                if tag == "kitchen_sink":
                    GPIO.output("P8_8", GPIO.HIGH)
                elif tag == "bathroom_sink":
                    GPIO.output("P8_10", GPIO.HIGH)
                elif tag == "shower":
                    GPIO.output("P8_12", GPIO.HIGH)
                time.sleep(7)
                if not self.Open():
                    print "!!! Either the sensors are having issues or the valve is not opening fully. !!!"
                else:
                    print "There was an issue with the valve opening but it cleared on a second attempt."
                break
            time.sleep(2)
            limitCount = limitCount + 1
            

    def valveStop(self, tag):
        limitCount = 0
        if tag == "kitchen_sink":
            GPIO.output("P8_8", GPIO.LOW)
        elif tag == "bathroom_sink":
            GPIO.output("P8_10", GPIO.LOW)
        elif tag == "shower":
            GPIO.output("P8_12", GPIO.LOW)
        print "%s valve close triggered" % tag
        while not self.Closed(tag):
            if limitCount == 5:#if after ~10 seconds if not closed attempt to close again 
                limitCount = 0
                if tag == "kitchen_sink":#cycle the correct valve
                    GPIO.output("P8_8", GPIO.HIGH)
                    time.sleep(5)
                    GPIO.output("P8_8", GPIO.LOW)
                elif tag == "bathroom_sink":
                    GPIO.output("P8_10", GPIO.HIGH)
                    time.sleep(5)
                    GPIO.output("P8_10", GPIO.LOW)
                elif tag == "shower":
                    GPIO.output("P8_12", GPIO.HIGH)
                    time.sleep(5)
                    GPIO.output("P8_12", GPIO.LOW)
                time.sleep(7)
                if not self.Closed(tag):#check if the problem was fixed
                    print "!!! There is a problem with the valve or the limit sensors. !!!"
                else:
                    print "There was an issue with the valve but it cleared on a open/close cycle."
                break
            time.sleep(2)
            limitCount = limitCount + 1
    
    def Open(self, tag):
        if tag == "kitchen_sink":
            if GPIO.input("P8_9") and not GPIO.input("P8_7"):
                print "%s valve is OPEN" % tag
                return True
            elif not GPIO.input("P8_9") and GPIO.input("P8_7"):
                print "%s valve is CLOSED" % tag
                return False
        if tag == "bathroom_sink":
            if GPIO.input("P8_14") and not GPIO.input("P8_11"):
                print "%s valve is OPEN" % tag
                return True
            elif not GPIO.input("P8_14") and GPIO.input("P8_11"):
                print "%s valve is CLOSED" % tag
                return False
        if tag == "shower":
            if GPIO.input("P8_17") and not GPIO.input("P8_15"):
                print "%s valve is OPEN" % tag
                return True
            elif not GPIO.input("P8_17") and GPIO.input("P8_15"):
                print "%s valve is CLOSED" % tag
                return False
        else:
            print "%s valve is in progress"% tag
            return False
            
    def Closed(self, tag):
        if tag == "kitchen_sink":
            if GPIO.input("P8_9") and not GPIO.input("P8_7"):
                print "%s valve is OPEN" % tag
                return False
            elif not GPIO.input("P8_9") and GPIO.input("P8_7"):
                print "%s valve is CLOSED" % tag
                return True
        if tag == "bathroom_sink":
            if GPIO.input("P8_14") and not GPIO.input("P8_11"):
                print "%s valve is OPEN" % tag
                return False
            elif not GPIO.input("P8_14") and GPIO.input("P8_11"):
                print "%s valve is CLOSED" % tag
                return True
        if tag == "shower":
            if GPIO.input("P8_17") and not GPIO.input("P8_15"):
                print "%s valve is OPEN" % tag
                return False
            elif not GPIO.input("P8_17") and GPIO.input("P8_15"):
                print "%s valve is CLOSED" % tag
                return True
        else:
            print "%s valve is in progress" % tag
            return False