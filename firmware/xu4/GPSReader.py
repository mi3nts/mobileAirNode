
import serial
import datetime
from mintsXU4 import mintsSensorReader as mSR
from mintsXU4 import mintsDefinitions as mD
import time
import serial
import pynmea2
from collections import OrderedDict


dataFolder = mD.dataFolder
# duePort    = mD.duePort
gpsPort    =  mD.gpsPort
#




def main():

    reader = pynmea2.NMEAStreamReader()
    ser = serial.Serial(
    port= gpsPort,\
    baudrate=9600,\
    parity  =serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout=0)

    lastGPRMC = time.time()
    lastGPGGA = time.time()
    delta  = 2
    print("connected to: " + ser.portstr)

    #this will store the line
    line = []
    while True:

        for c in ser.read():
            line.append(chr(c))
            if chr(c) == '\n':
                dataString     = (''.join(line))
                dateTime  = datetime.datetime.now()
                if (dataString.startswith("$GPGGA") and mSR.getDeltaTime(lastGPGGA,delta)):
                    mSR.GPSGPGGAWrite(dataString,dateTime)
                    lastGPGGA = time.time()
                if (dataString.startswith("$GPRMC") and mSR.getDeltaTime(lastGPGGA,delta)):
                    mSR.GPSGPRMCWrite(dataString,dateTime)
                    lastGPRMC = time.time()
                    # # mSR.dataSplit(dataStringPost,datetime.datetime.now())
                line = []
                break

    ser.close()



if __name__ == "__main__":
   main()
