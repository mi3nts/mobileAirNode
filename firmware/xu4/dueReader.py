
import serial
import datetime
from mintsXU4 import mintsSensorReader as mSR
from mintsXU4 import mintsDefinitions as mD

dataFolder = mD.dataFolder
duePort    = mD.duePort

def main():

    ser = serial.Serial(
    port= duePort,\
    baudrate=9600,\
    parity  =serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout=0)

    print("connected to: " + ser.portstr)

    #this will store the line
    line = []

    while True:
        for c in ser.read():
            line.append(chr(c))
            if chr(c) == '~':
                dataString     = (''.join(line))
                dataStringPost = dataString.replace('~', '')
                mSR.dataSplit(dataStringPost,datetime.datetime.now())
                line = []
                break

    ser.close()


if __name__ == "__main__":
   main()
