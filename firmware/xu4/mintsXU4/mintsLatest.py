

# import serial
# ser = serial.Serial('/dev/ttyACM3')
import serial
import datetime
import os
import csv
import deepdish as dd
import time
import json
import numpy as np
from mintsXU4 import mintsDefinitions as mD
import requests
import json
import datetime



dataFolder           = mD.dataFolder
dataFolderUnpublished= mD.dataFolderUnplublished
macAddress           = mD.macAddress
latestDisplayOn      = mD.latestDisplayOn
streamURL            = mD.streamURL
streamOn             = mD.streamON

def streamJSONLatest(sensorDictionary,sensorName):
    if(streamOn):
        try:
            sendURL = streamURL +"/"+sensorName
            print(sendURL)
            sensorDictionary['nodeID']     = macAddress
            sensorDictionary['sensorID']   = sensorName
            print("-----------------")

            # if(len(str(sensorDictionary))>64000):
            #     print("Data Too Large, Data Length: "+ str(len(str(sensorDictionary))))
            #     dateTime = sensorDictionary['dateTime']
            #     sensorDictionary.clear()
            #     sensorDictionary['dateTime'] = str(dateTime)
            #     sensorDictionary['nodeID']   = macAddress
            #     sensorDictionary['sensorID'] = sensorName



            r = requests.post(url =sendURL,\
                                  json=sensorDictionary,\
                                  auth=('algolook', 'safeai123'))
            print("Status Code:" + str(r.status_code))
        except Exception as e:
            print(e)
            print("Data Not Streamed")


def writeJSONLatest(sensorDictionary,sensorName):
    # print(writePath)
    if(latestDisplayOn):
        directoryIn  = dataFolder+"/"+macAddress+"/"+sensorName+".json"
        # print(directoryIn)
        try:
        	with open(directoryIn,'w') as fp:
        	    json.dump(sensorDictionary, fp)
        except:
            print("Data Conflict!")

def writeJSONLatestUnpublished(sensorDictionary,sensorName):
    # print(writePath)
    if(latestDisplayOn):
        directoryIn  = dataFolderUnpublished+"/"+macAddress+"/"+sensorName+".json"
        # print(directoryIn)
        try:
        	with open(directoryIn,'w') as fp:
        	    json.dump(sensorDictionary, fp)
        except:
            print("Data Conflict!")


def readJSONLatestAll(sensorName):
    try:
        directoryIn  = dataFolder+"/"+macAddress+"/"+sensorName+".json"
        with open(directoryIn, 'r') as myfile:
            # dataRead=myfile.read()
            dataRead=json.load(myfile)

        time.sleep(0.01)
        return dataRead, True
    except:
        print("Data Conflict!")
        return "NaN", False
