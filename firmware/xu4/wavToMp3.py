import os
import time
import sys
import shutil
import datetime
from mintsXU4 import mintsSensorReader as mSR
from mintsXU4 import mintsDefinitions as mD
from os import listdir,walk
from os.path import isfile, join
#
dataFolder    = mD.dataFolder
macAddress    = mD.macAddress
minutesBefore = 3

def main():

    try:
        allWavPaths,wavExist = getConvertPath(minutesBefore)

        print("-----------------")
        print(allWavPaths)
        print("-----------------")
        print(wavExist)
        print("-----------------")

        if(wavExist):
            for wavPath in allWavPaths:
                mp3Path   =  wavPath.replace("wav", "mp3")
                commandIn = "ffmpeg -i "+ wavPath +" "+ mp3Path
                os.system(commandIn)
                time.sleep(2)
                os.remove(wavPath)

    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))


def getConvertPath(minutesBefore):
    dateTime =  datetime.datetime.now() -  datetime.timedelta(minutes=minutesBefore)

    wavFolder = dataFolder+"/"+macAddress+"/"+str(dateTime.year).zfill(4)  + \
    "/" + str(dateTime.month).zfill(2)+ "/"+str(dateTime.day).zfill(2)+  \
    "/audioSnaps/"

    fileName = "MINTS_"+ macAddress+ "_" +"MI305"+ "_" + \
    str(dateTime.year).zfill(4) + "_" +str(dateTime.month).zfill(2) + "_" +str(dateTime.day).zfill(2)+ "_" + \
    str(dateTime.hour).zfill(2) + "_" +str(dateTime.minute).zfill(2) + "_"
    # # directory = os.listdir(convertPathWav)
    allFiles    = []
    allWavPaths = []
    print(fileName)
    for file in os.listdir(wavFolder):
        if file.endswith(".wav") and (file.find(fileName)== 0):
            wavPath =  wavFolder + str(file)
            allWavPaths.append(wavPath)

    wavExist = len(allWavPaths)>0


    return allWavPaths,wavExist;


if __name__ == '__main__':
  main()
