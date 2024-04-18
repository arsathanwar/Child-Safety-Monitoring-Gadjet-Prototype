import time
import sys
import ibmiotf.application
import ibmiotf.device
import random as r


#Provide your IBM Watson Device Credentials
organization = "rdegyk"
deviceType = "weather1"
deviceId = "weather1"
authMethod = "token"
authToken = "_oa-3bajxqvCrO(6kW"

# Initialize GPIO

def myCommandCallback(cmd):
    print("Command received: %s" % cmd.data['command'])
    print(cmd)
        


try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        #Get Sensor Data from DHT11
        temp=r.randint(0,100)
        humidity=r.randint(0,100)
        pulse=r.randint(0,100)
        oxygen= r.randint(0,100)
        lat =  17
        lon = 18
        
        data = {"d":{ 'temp' : temp, 'humidity' : humidity, 'pulse': pulse ,'oxygen': oxygen,"lat":lat,"lon":lon}}
        #print data
        def myOnPublishCallback():
            print ("Published Temperature = %s C" % temp, "Humidity = %s %%" % humidity, "to IBM Watson")

        success = deviceCli.publishEvent("IoTSensor", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(1)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
