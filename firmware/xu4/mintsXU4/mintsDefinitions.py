
from getmac import get_mac_address
import serial.tools.list_ports

def findPort(find):
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        currentPort = str(p)
        if(currentPort.endswith(find)):
            return(currentPort.split(" ")[0])


def findDuePort():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        currentPort = str(p[2])
        if(currentPort.find("PID=2341")>=0):
            return(p[0])



def findNanoPorts():
    ports = list(serial.tools.list_ports.comports())
    outPorts = []
    for p in ports:
        currentPort = str(p)
        if(currentPort.endswith("FT232R USB UART")):
            outPorts.append(currentPort.split(" ")[0])

    return outPorts



dataFolder            = "/home/teamlary/mintsData/raw"
duePort               = findDuePort()
nanoPorts             = findNanoPorts()
show2Port             = findPort("CP2104 USB to UART Bridge Controller")

macAddress          = get_mac_address(interface="docker0").replace(":","")  #LAB Machine
# macAddress          = get_mac_address(interface="enp1s0").replace(":","")
# macAddress            = get_mac_address(interface="eth0").replace(":","") # XU4
latestOff             = True
gpsPort               = findPort("GPS/GNSS Receiver")


# print(length(findNansPorts))
