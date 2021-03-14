from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
import datetime
import random
from dateutil.tz import tzoffset

AllowedActions = ['both', 'publish', 'subscribe']

host = '<IOT_API_ENDPOINT>'
rootCAPath = '<ROOT_CA_CERTIFICATE>'
certificatePath = '<THING_CERTIFICATE_PEM>'
privateKeyPath = '<THING_PRIVATE_PEM>'
useWebsocket = False
clientId = 'basicPubSub'
topic = 'sdk/test/Python'

# Port defaults
if useWebsocket:  # When no port override for WebSocket, default to 443
    port = 443
if not useWebsocket:  # When no port override for non-WebSocket, default to 8883
    port = 8883

# Configure logging
'''
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)
'''

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
if useWebsocket:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()

time.sleep(2)

loopCount = 0


def getData():
    messageJson={}
    station=random.randint(0,1)
    if station==0:
        messageJson['stationID']='ST102'
        messageJson['latitude']=33.717950
        messageJson['longitude']=-84.454540
    elif station==1:
        messageJson['stationID']='ST105'
        messageJson['latitude']=33.933337
        messageJson['longitude']=-84.357290
    
    now=datetime.datetime.utcnow()
    messageJson['timestamp']=int(time.time())
    #messageJson['dataTime']=str(now.strftime("%Y-%m-%dT:%H:%M:%S"))
    messageJson['pm2_5']=random.randint(0,5004)/10.0
    messageJson['pm10']=random.randint(0,6040)/10.0
    #messageJson['o3']=random.randint(0,604)/1000.0
    #messageJson['no2']=random.randint(65,204)/100.0
    messageJson['so2']=random.randint(0,1004)/1000.0
    messageJson['co']=random.randint(0,504)/100.0
    
    return messageJson

while True:        
    message = getData()
    messageJson = json.dumps(message)
    myAWSIoTMQTTClient.publish(topic, messageJson, 1)
    print('Published topic %s: %s\n' % (topic, messageJson))
    loopCount += 1
    time.sleep(1)
