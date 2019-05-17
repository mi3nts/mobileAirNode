#
import serial
import datetime
from mintsXU4 import mintsSensorReader as mSR
from mintsXU4 import mintsDefinitions as mD

dataFolder  = mD.dataFolder
nanoPorts    = mD.nanoPorts

def main():
    if(len(nanoPorts)>0):

        ser = serial.Serial(
        port= nanoPorts[0],\
        baudrate=9600,\
        parity  =serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
        timeout=0)

        print("connected to: " + ser.portstr)

        #this will store the line
        line = []

        while True:
            try:
                for c in ser.read():
                    line.append(chr(c))
                    if chr(c) == '~':
                        dataString     = (''.join(line))
                        dataStringPost = dataString.replace('~', '')
                        print(dataStringPost)
                        mSR.dataSplit(dataStringPost,datetime.datetime.now())
                        line = []
                        break
            except:
                print("Incomplete String Read")
                line = []

        ser.close()








if __name__ == "__main__":
   main()
