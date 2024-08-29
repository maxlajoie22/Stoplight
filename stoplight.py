# stoplight-us.py : Example code for a stoplight for a N-S US style stoplight
#
# Name(s): Max Lajoie, Max Iliff
# E-mail(s): mlajoie@nd.edu  miliff@nd.edu
#

import time 
from sense_hat import SenseHat
import mqtt_link as mqttnd


# Your functions go here

# Set the stoplight to a specific setting
#   theHAT - the SenseHat object
#   theSetting - the setting to set the stoplight to
#     which is either red, yellow, or green
def setStoplight_NS (theHAT, theSetting):
    if theSetting == 'Red':
        # Turn the red light on
        sense.set_pixel(2, 5, (255, 0, 0)) 
        # Turn off the yellow and green lights       
        sense.set_pixel(2, 6, (0, 0, 0))
        sense.set_pixel(2, 7, (0, 0, 0))
    elif theSetting == 'Yellow':
        # Turn the yellow light on
        sense.set_pixel(2, 6, (255, 255, 0))
        # Turn off the red and green lights       
        sense.set_pixel(2, 5, (0, 0, 0)) 
        sense.set_pixel(2, 7, (0, 0, 0))
    elif theSetting == 'Green':
        # Turn the green light on
        sense.set_pixel(2, 7, (0, 255, 0))
        # Turn off the red and yellow lights       
        sense.set_pixel(2, 5, (0, 0, 0)) 
        sense.set_pixel(2, 6, (0, 0, 0))
    elif theSetting == 'RedYellow':
        # Turn Red and Yellow on
        sense.set_pixel(2,5,(255,0,0))
        sense.set_pixel(2,6,(255,255,0))
        # Turn off green light
        sense.set_pixel(2,7,(0,0,0))
        


def setStoplight_EW (theHAT, theSetting):
    if theSetting == 'Red':
        # Turn the red light on
        sense.set_pixel(5, 2, (255, 0, 0)) 
        # Turn off the yellow and green lights       
        sense.set_pixel(6, 2, (0, 0, 0))
        sense.set_pixel(7, 2, (0, 0, 0))
    elif theSetting == 'Yellow':
        # Turn the yellow light on
        sense.set_pixel(6, 2, (255, 255, 0))
        # Turn off the red and green lights       
        sense.set_pixel(5, 2, (0, 0, 0)) 
        sense.set_pixel(7, 2, (0, 0, 0))
    elif theSetting == 'Green':
        # Turn the green light on
        sense.set_pixel(7, 2, (0, 255, 0))
        # Turn off the red and yellow lights       
        sense.set_pixel(5, 2, (0, 0, 0)) 
        sense.set_pixel(6, 2, (0, 0, 0))
    elif theSetting == 'RedYellow':
        # Turn Red and Yellow on
        sense.set_pixel(5,2,(255,0,0))
        sense.set_pixel(6,2,(255,255,0))
        # Turn off green light
        sense.set_pixel(7,2,(0,0,0))
        
def DoCrossNS(LoopDelay):
    sense.set_pixel(0,0,(0,0,0))
    sense.set_pixel(0,3,(0,0,0))
    sense.set_pixel(0,6,(0,0,0))       
    # NS crosswalk on
    sense.set_pixel(0,1,(0,255,0))
    sense.set_pixel(0,4,(0,255,0))
    sense.set_pixel(0,7,(0,255,0))
    for i in range(LoopDelay):
        time.sleep(.25)
        sense.set_pixel(1,1,(0,0,255))
        sense.set_pixel(1,4,(0,0,255))
        sense.set_pixel(1,7,(0,0,255))
        time.sleep(.25)
        sense.set_pixel(1,1,(0,0,0))
        sense.set_pixel(1,4,(0,0,0))
        sense.set_pixel(1,7,(0,0,0))
    #turns off green crosswalk
    #sense.set_pixel(0,1,(0,0,0))
    #sense.set_pixel(0,4,(0,0,0))
    sense.set_pixel(0,7,(0,0,0))
    #turns on red crosswalk
    #sense.set_pixel(0,0,(255,0,0))
    #sense.set_pixel(0,3,(255,0,0))
    sense.set_pixel(0,6,(255,0,0))

##################################################
# Main Code is Here

sense = SenseHat()

LoopDelay = 0 

# Start at Red, go to Green, then Yellow, then back to Red
#
# State         Means What                   Next State      Ticks
# 
# Light-Red     Stay red for 35 seconds      Light-Green     35*4
# Light-Green   Stay green for 30 seconds    Light-Yellow    30*4
# Light-Yellow  Stay yellow for 5 seconds    Light-Red        5*4


TheStateNS = 'Light-Red'
TheStateEW = 'Light-Green' # TheStateEW does nothing just for understanding of its current state



# Start with Crosswalks off
sense.set_pixel(0,0,(255,0,0))
sense.set_pixel(0,3,(255,0,0))
sense.set_pixel(0,6,(255,0,0))
sense.set_pixel(6,0,(255,0,0))

# Connect to the MQTT Broker at Notre Dame
theClient = mqttnd.connect_mqtt()
while True:
    mqttnd.send_mqtt(theClient, "cse34468-su24/MaxGroup/lab-03/stoplight/json", "{'traffic-ns' :" + str(TheStateNS) +", 'traffic-ew' : " + str(TheStateEW) + " }")
    mqttnd.send_mqtt(theClient, "cse34468-su24/MaxGroup/lab-03/stoplight/traffic-ns", "The State of NS: " + str(TheStateNS))
    mqttnd.send_mqtt(theClient, "cse34468-su24/MaxGroup/lab-03/stoplight/traffic-ew", "The State of EW: " +str(TheStateEW))
    if TheStateNS == 'Light-Red':
        setStoplight_NS(sense, 'Red')
        setStoplight_EW(sense,'Green')
        LoopDelay = 6
        
        # turns off red crosswalk
        sense.set_pixel(6,0,(0,0,0))
        # EW crosswalk on
        sense.set_pixel(7,0,(0,255,0))
        for i in range(LoopDelay*2):
            time.sleep(.25)
            sense.set_pixel(7,1,(0,0,255))
            time.sleep(.25)
            sense.set_pixel(7,1,(0,0,0))
        #turns off green crosswalk
        sense.set_pixel(7,0,(0,0,0))
        #turns on red crosswalk
        sense.set_pixel(6,0,(255,0,0))
            
        TheStateNS = 'Light-RedYellow'
        TheStateEW = 'Light-Yellow'
    elif TheStateNS == 'Light-RedYellow': 
        setStoplight_NS(sense,'RedYellow')
        setStoplight_EW(sense,'Yellow')
        LoopDelay = 1
        TheStateNS = 'Light-Green'
        TheStateEW = 'Light-Red'
    elif TheStateNS == 'Light-Green':
        setStoplight_NS(sense, 'Green')
        setStoplight_EW(sense, 'Red')
        LoopDelay = 6
        
        DoCrossNS(LoopDelay*2)
        
        #starts staggering process
        for i in range(3):
            sense.set_pixel(1,1,(0,0,255))
            sense.set_pixel(1,4,(0,0,255))
            time.sleep(.25)
            sense.set_pixel(1,1,(0,0,0))
            sense.set_pixel(1,4,(0,0,0))
            time.sleep(.25)
        sense.set_pixel(0,4,(0,0,0))
        sense.set_pixel(0,3,(255,0,0))
        
        
        #finishs staggering
        for j in range(3):
            sense.set_pixel(1,1,(0,0,255))
            time.sleep(.25)
            sense.set_pixel(1,1,(0,0,0))
            time.sleep(.25)
        sense.set_pixel(0,1,(0,0,0))
        sense.set_pixel(0,0,(255,0,0))
        
       
        TheStateNS = 'Light-Yellow'
        TheStateEW = 'Light-RedYellow'
    elif TheStateNS == 'Light-Yellow':
        setStoplight_NS(sense, 'Yellow')
        setStoplight_EW(sense, 'RedYellow')
        LoopDelay = 1
        TheStateNS = 'Light-Red'
        TheStateEW = 'Light-Green'

    # All done - sleep and keep counting
    
    # Leave this code here
    time.sleep(LoopDelay)