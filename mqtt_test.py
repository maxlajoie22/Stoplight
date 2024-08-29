# mqtt-test.py : Code for testing out MQTT
#
# Name(s):
# E-mail(s):
#

import time
import mqtt_link as mqttnd

# Connect to the MQTT Broker at Notre Dame
theClient = mqttnd.connect_mqtt()

mqttnd.send_mqtt(theClient, "cse34468-su24/MaxGroup/lab-03/test/time-alive", "I am alive!")

TheCount = 0
NETID_list = ['mlajoie','miliff']
while True:
    time.sleep(1)
    print('Sending a MQTT message!')
    mqttnd.send_mqtt(theClient, "cse34468-su24/MaxGroup/lab-03/test/status", "I have been alive for " + str(TheCount) + " seconds")
    mqttnd.send_mqtt(theClient, "cse34468-su24/MaxGroup/lab-03/test/time-alive",  str(TheCount))
    mqttnd.send_mqtt(theClient, "cse34468-su24/MaxGroup/lab-03/test/json", "{'NetID' :" + str(NETID_list[TheCount%2]) +", 'TimeAlive' : " + str(TheCount) + " }")
    TheCount += 1




