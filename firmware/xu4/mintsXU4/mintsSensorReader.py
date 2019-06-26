# ***************************************************************************
#  mintsXU4
#   ---------------------------------
#   Written by: Lakitha Omal Harindha Wijeratne
#   - for -
#   Mints: Multi-scale Integrated Sensing and Simulation
#   ---------------------------------
#   Date: February 4th, 2019
#   ---------------------------------
#   This module is written for generic implimentation of MINTS projects
#   --------------------------------------------------------------------------
#   https://github.com/mi3nts
#   http://utdmints.info/
#  ***************************************************************************

import serial
import hdf5storage
import datetime
import os
import csv
import deepdish as dd
from mintsXU4 import mintsLatest as mL
from mintsXU4 import mintsDefinitions as mD
from getmac import get_mac_address
import time
import serial
import pynmea2
from collections import OrderedDict
import numpy as np
import netifaces as ni
from scipy.io import savemat
import wave

macAddress              = mD.macAddress
dataFolder              = mD.dataFolder
dataFolderUnpublished   = mD.dataFolderUnplublished
latestDisplayOn         = mD.latestDisplayOn

def sensorFinisherUnpublished(dateTime,sensorName,sensorDictionary):
    #Getting Write Path
    writePath = getWritePathUnpublished(sensorName,dateTime)
    print(writePath)
    exists = directoryCheck(writePath)
    # writeCSV2(writePath,sensorDictionary,exists)
    # mL.streamJSONLatest(sensorDictionary,sensorName)
    mL.writeJSONLatestUnpublished(sensorDictionary,sensorName)

    print("-----------------------------------")
    print(sensorName)
    # print(sensorDictionary)

def sensorFinisher(dateTime,sensorName,sensorDictionary):
    #Getting Write Path
    writePath = getWritePath(sensorName,dateTime)
    print(writePath)
    exists = directoryCheck(writePath)
    writeCSV2(writePath,sensorDictionary,exists)
    mL.streamJSONLatest(sensorDictionary,sensorName)
    mL.writeJSONLatest(sensorDictionary,sensorName)

    print("-----------------------------------")
    print(sensorName)
    # print(sensorDictionary)

def sensorFinisherIP(dateTime,sensorName,sensorDictionary):
    #Getting Write Path
    writePath = getWritePathIP(sensorName,dateTime)
    exists = directoryCheck(writePath)
    writeCSV2(writePath,sensorDictionary,exists)
    print(writePath)
    if(latestDisplayOn):
       print("writePath in Latest ")
       print(writePath)
       mL.writeJSONLatest(sensorDictionary,sensorName)

    print("-----------------------------------")
    print(sensorName)
    print(sensorDictionary)


def sensorFinisherAudio(dateTime,sensorName,audioDataWav,CHANNELS,FORMAT,RATE,audio):

    writePath = getWritePathAudio(sensorName,dateTime)
    print(writePath)
    exists = directoryCheck(writePath)
    waveFile = wave.open(writePath, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(audioDataWav))
    waveFile.close()
    # flir001 = {}
    # flir001['thermalImage'] = dataCelcius
    # hdf5storage.write(flir001, '.', writePath, store_python_metadata=False, matlab_compatible=True)


def getWritePathAudio(labelIn,dateTime):
    #Example  : MINTS_0061_OOPCN3_2019_01_04.csv
    writePath = dataFolder+"/"+macAddress+"/"+str(dateTime.year).zfill(4)  + \
    "/" + str(dateTime.month).zfill(2)+ "/"+str(dateTime.day).zfill(2)+  \
    "/audioSnaps/"+ "MINTS_"+ macAddress+ "_" +labelIn + "_" + \
    str(dateTime.year).zfill(4) + "_" +str(dateTime.month).zfill(2) + "_" +str(dateTime.day).zfill(2)+ "_" + \
    str(dateTime.hour).zfill(2) + "_" +str(dateTime.minute).zfill(2) + "_" +str(dateTime.second).zfill(2)\
     +".wav"
    return writePath;


def sensorFinisherSummaryOnly(dateTime,sensorName,sensorDictionary):
    #Getting Write Path
    writePath = getWritePath(sensorName,dateTime)
    print(writePath)
    exists = directoryCheck(writePath)
    writeCSV2(writePath,sensorDictionary,exists)
    mL.writeJSONLatest(sensorDictionary,sensorName)

    print("-----------------------------------")
    print(sensorName)

def sensorFinisherThermal(dateTime,sensorName,dataCelcius):
    writePath = getWritePathThermal(sensorName,dateTime)
    exists = directoryCheck(writePath)

    flir001 = {}
    flir001['thermalImage'] = dataCelcius
    hdf5storage.write(flir001, '.', writePath, store_python_metadata=False, matlab_compatible=True)

    sensorDictionary =  OrderedDict([
                ("dateTime"     , str(dateTime)),\
                ("thermalImage"  , dataCelcius.tolist())\
                ])
    mL.streamJSONLatest(sensorDictionary,sensorName)



def getWritePathThermal(labelIn,dateTime):
    #Example  : MINTS_0061_OOPCN3_2019_01_04.csv
    writePath = dataFolder+"/"+macAddress+"/"+str(dateTime.year).zfill(4)  + \
    "/" + str(dateTime.month).zfill(2)+ "/"+str(dateTime.day).zfill(2)+  \
    "/thermalSnaps/"+ "MINTS_"+ macAddress+ "_" +labelIn + "_" + \
    str(dateTime.year).zfill(4) + "_" +str(dateTime.month).zfill(2) + "_" +str(dateTime.day).zfill(2)+  "_" + \
    str(dateTime.hour).zfill(2) + "_" +str(dateTime.minute).zfill(2) + "_" +str(dateTime.second).zfill(2)\
     +".mat"

    return writePath;

def dataSplit(dataString,dateTime):
    dataOut   = dataString.split('!')
    if(len(dataOut) == 2):
        tag       = dataOut[0]
        dataQuota = dataOut[1]
        if(tag.find("#mintsO")==0):
            sensorSplit(dataQuota,dateTime)

def sensorSplit(dataQuota,dateTime):
    dataOut    = dataQuota.split('>')
    if(len(dataOut) == 2):
        sensorID   = dataOut[0]
        sensorData = dataOut[1]
        sensorSend(sensorID,sensorData,dateTime)

def sensorSend(sensorID,sensorData,dateTime):
    if(sensorID=="BME280"):
        BME280Write(sensorData,dateTime)
    if(sensorID=="MGS001"):
        MGS001Write(sensorData,dateTime)
    if(sensorID=="SCD30"):
        SCD30Write(sensorData,dateTime)
    if(sensorID=="VEML6075"):
        VEML6075Write(sensorData,dateTime)
    if(sensorID=="AS7262"):
        AS7262Write(sensorData,dateTime)
    if(sensorID=="PPD42NSDuo"):
        PPD42NSDuoWrite(sensorData,dateTime)
    if(sensorID=="OPCN2"):
        OPCN2Write(sensorData,dateTime)
    if(sensorID=="OPCN3"):
        OPCN3Write(sensorData,dateTime)
    if(sensorID=="VEML6070"):
        VEML6070Write(sensorData,dateTime)
    if(sensorID=="TSL2591"):
        TSL2591Write(sensorData,dateTime)
    if(sensorID=="LIBRAD"):
        LIBRADWrite(sensorData,dateTime)
    if(sensorID=="HTU21D"):
        HTU21DWrite(sensorData,dateTime)
    if(sensorID=="BMP280"):
        BMP280Write(sensorData,dateTime)
    if(sensorID=="INA219"):
        INA219Write(sensorData,dateTime)
    if(sensorID=="PPD42NS"):
        PPD42NSWrite(sensorData,dateTime)




def BME280Write(sensorData,dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "BME280"
    dataLength = 4
    if(len(dataOut) == (dataLength +1)):
        sensorDictionary =  OrderedDict([
                ("dateTime"     , str(dateTime)),
        		("temperature"  ,dataOut[0]),
            	("pressure"     ,dataOut[1]),
                ("humidity"     ,dataOut[2]),
            	("altitude"     ,dataOut[3])
                ])
        sensorFinisher(dateTime,sensorName,sensorDictionary)


def MGS001Write(sensorData,dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "MGS001"
    dataLength = 8
    if(len(dataOut) == (dataLength +1)):
        sensorDictionary =  OrderedDict([
                ("dateTime"   , str(dateTime)),
        		("nh3"        ,dataOut[0]),
            	("co"         ,dataOut[1]),
                ("no2"        ,dataOut[2]),
            	("c3h8"       ,dataOut[3]),
        		("c4h10"      ,dataOut[4]),
            	("ch4"        ,dataOut[5]),
                ("h2"         ,dataOut[6]),
            	("c2h5oh"     ,dataOut[7]),
                ])
        sensorFinisher(dateTime,sensorName,sensorDictionary)


def SCD30Write(sensorData,dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "SCD30"
    dataLength = 3
    if(len(dataOut) == (dataLength +1)):
        sensorDictionary =  OrderedDict([
                ("dateTime"     , str(dateTime)),
        		("c02"          ,dataOut[0]),
            	("temperature"  ,dataOut[1]),
                ("humidity"     ,dataOut[2]),

                ])
        sensorFinisher(dateTime,sensorName,sensorDictionary)


def LIBRADWrite(sensorData,dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "LIBRAD"
    dataLength = 4
    if(len(dataOut) ==(dataLength +1)):
        sensorDictionary = OrderedDict([
                ("dateTime"           ,str(dateTime)),
        	    ("countPerMinute"     ,dataOut[0]),
            	("radiationValue"     ,dataOut[1]),
                ("timeSpent"          ,dataOut[2]),
                ("LIBRADCount"        ,dataOut[3])
        	     ])

        sensorFinisher(dateTime,sensorName,sensorDictionary)


def VEML6070Write(sensorData,dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "VEML6070"
    dataLength = 1
    if(len(dataOut) ==(dataLength +1)):
        sensorDictionary = OrderedDict([
                ("dateTime"    , str(dateTime)),
        	    ("UVLightLevel" ,dataOut[0]),
        	     ])

        sensorFinisher(dateTime,sensorName,sensorDictionary)


def TSL2591Write(sensorData,dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "TSL2591"
    dataLength = 5
    if(len(dataOut) ==(dataLength +1)):
        sensorDictionary = OrderedDict([
                ("dateTime"   ,str(dateTime)),
        	    ("luminosity" ,dataOut[0]),
            	("ir"         ,dataOut[1]),
                ("full"       ,dataOut[2]),
                ("visible"    ,dataOut[3]),
                ("lux"        ,dataOut[4])
        	     ])

        sensorFinisher(dateTime,sensorName,sensorDictionary)

def VEML6075Write(sensorData,dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "VEML6075"
    dataLength = 3
    if(len(dataOut) ==(dataLength +1)):
        sensorDictionary = OrderedDict([
                ("dateTime"    , str(dateTime)),
        	    ("UVALightLevel" ,dataOut[0]),
                ("UVBLightLevel" ,dataOut[1]),
        	    ("UVILightLevel" ,dataOut[2])
        	     ])

        sensorFinisher(dateTime,sensorName,sensorDictionary)


def AS7262Write(sensorData,dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "AS7262"
    dataLength = 13
    if(len(dataOut) ==(dataLength +1)):
        sensorDictionary = OrderedDict([
                ("dateTime"          ,str(dateTime)),
                ("temperature"        ,dataOut[0]),
                ("violetPre"          ,dataOut[1]),
            	("bluePre"            ,dataOut[2]),
                ("greenPre"           ,dataOut[3]),
                ("yellowPre"          ,dataOut[4]),
                ("orangePre"          ,dataOut[5]),
        	    ("redPre"             ,dataOut[6]),
                ("violetCalibrated"   ,dataOut[7]),
            	("blueCalibrated"     ,dataOut[8]),
                ("greenCalibrated"    ,dataOut[9]),
                ("yellowCalibrated"   ,dataOut[10]),
                ("orangeCalibrated"   ,dataOut[11]),
                ("redCalibrated"      ,dataOut[12])
        	    ])

        sensorFinisher(dateTime,sensorName,sensorDictionary)


def MI305Write(dataOut,dateTime):
    sensorName = "MI305"
    dataLength = 512
    dataOut = list(np.float_(dataOut))
    if(len(dataOut) == dataLength):
        sensorDictionary =  OrderedDict([
                 ("dateTime"     , str(dateTime)),
                 ("amplitudes" ,dataOut)
                 ])
        # print(sensorDictionary)

        sensorFinisherUnpublished(dateTime,sensorName,sensorDictionary)




# def MI305Write(dataOut,dateTime):
#     sensorName = "MI305"
#     dataLength = 512
#     if(len(dataOut) == (dataLength)):
#         sensorDictionary =  OrderedDict([
#                  ("dateTime"     , str(dateTime)),
#                  ("ampForFreq_0_00" , dataOut[0]),
#                  ("ampForFreq_15_66", dataOut[1]),
#                  ("ampForFreq_31_31", dataOut[2]),
#                  ("ampForFreq_46_97", dataOut[3]),
#                  ("ampForFreq_62_62", dataOut[4]),
#                  ("ampForFreq_78_28", dataOut[5]),
#                  ("ampForFreq_93_93", dataOut[6]),
#                  ("ampForFreq_109_59", dataOut[7]),
#                  ("ampForFreq_125_24", dataOut[8]),
#                  ("ampForFreq_140_90", dataOut[9]),
#                  ("ampForFreq_156_56", dataOut[10]),
#                  ("ampForFreq_172_21", dataOut[11]),
#                  ("ampForFreq_187_87", dataOut[12]),
#                  ("ampForFreq_203_52", dataOut[13]),
#                  ("ampForFreq_219_18", dataOut[14]),
#                  ("ampForFreq_234_83", dataOut[15]),
#                  ("ampForFreq_250_49", dataOut[16]),
#                  ("ampForFreq_266_14", dataOut[17]),
#                  ("ampForFreq_281_80", dataOut[18]),
#                  ("ampForFreq_297_46", dataOut[19]),
#                  ("ampForFreq_313_11", dataOut[20]),
#                  ("ampForFreq_328_77", dataOut[21]),
#                  ("ampForFreq_344_42", dataOut[22]),
#                  ("ampForFreq_360_08", dataOut[23]),
#                  ("ampForFreq_375_73", dataOut[24]),
#                  ("ampForFreq_391_39", dataOut[25]),
#                  ("ampForFreq_407_05", dataOut[26]),
#                  ("ampForFreq_422_70", dataOut[27]),
#                  ("ampForFreq_438_36", dataOut[28]),
#                  ("ampForFreq_454_01", dataOut[29]),
#                  ("ampForFreq_469_67", dataOut[30]),
#                  ("ampForFreq_485_32", dataOut[31]),
#                  ("ampForFreq_500_98", dataOut[32]),
#                  ("ampForFreq_516_63", dataOut[33]),
#                  ("ampForFreq_532_29", dataOut[34]),
#                  ("ampForFreq_547_95", dataOut[35]),
#                  ("ampForFreq_563_60", dataOut[36]),
#                  ("ampForFreq_579_26", dataOut[37]),
#                  ("ampForFreq_594_91", dataOut[38]),
#                  ("ampForFreq_610_57", dataOut[39]),
#                  ("ampForFreq_626_22", dataOut[40]),
#                  ("ampForFreq_641_88", dataOut[41]),
#                  ("ampForFreq_657_53", dataOut[42]),
#                  ("ampForFreq_673_19", dataOut[43]),
#                  ("ampForFreq_688_85", dataOut[44]),
#                  ("ampForFreq_704_50", dataOut[45]),
#                  ("ampForFreq_720_16", dataOut[46]),
#                  ("ampForFreq_735_81", dataOut[47]),
#                  ("ampForFreq_751_47", dataOut[48]),
#                  ("ampForFreq_767_12", dataOut[49]),
#                  ("ampForFreq_782_78", dataOut[50]),
#                  ("ampForFreq_798_43", dataOut[51]),
#                  ("ampForFreq_814_09", dataOut[52]),
#                  ("ampForFreq_829_75", dataOut[53]),
#                  ("ampForFreq_845_40", dataOut[54]),
#                  ("ampForFreq_861_06", dataOut[55]),
#                  ("ampForFreq_876_71", dataOut[56]),
#                  ("ampForFreq_892_37", dataOut[57]),
#                  ("ampForFreq_908_02", dataOut[58]),
#                  ("ampForFreq_923_68", dataOut[59]),
#                  ("ampForFreq_939_33", dataOut[60]),
#                  ("ampForFreq_954_99", dataOut[61]),
#                  ("ampForFreq_970_65", dataOut[62]),
#                  ("ampForFreq_986_30", dataOut[63]),
#                  ("ampForFreq_1001_96", dataOut[64]),
#                  ("ampForFreq_1017_61", dataOut[65]),
#                  ("ampForFreq_1033_27", dataOut[66]),
#                  ("ampForFreq_1048_92", dataOut[67]),
#                  ("ampForFreq_1064_58", dataOut[68]),
#                  ("ampForFreq_1080_23", dataOut[69]),
#                  ("ampForFreq_1095_89", dataOut[70]),
#                  ("ampForFreq_1111_55", dataOut[71]),
#                  ("ampForFreq_1127_20", dataOut[72]),
#                  ("ampForFreq_1142_86", dataOut[73]),
#                  ("ampForFreq_1158_51", dataOut[74]),
#                  ("ampForFreq_1174_17", dataOut[75]),
#                  ("ampForFreq_1189_82", dataOut[76]),
#                  ("ampForFreq_1205_48", dataOut[77]),
#                  ("ampForFreq_1221_14", dataOut[78]),
#                  ("ampForFreq_1236_79", dataOut[79]),
#                  ("ampForFreq_1252_45", dataOut[80]),
#                  ("ampForFreq_1268_10", dataOut[81]),
#                  ("ampForFreq_1283_76", dataOut[82]),
#                  ("ampForFreq_1299_41", dataOut[83]),
#                  ("ampForFreq_1315_07", dataOut[84]),
#                  ("ampForFreq_1330_72", dataOut[85]),
#                  ("ampForFreq_1346_38", dataOut[86]),
#                  ("ampForFreq_1362_04", dataOut[87]),
#                  ("ampForFreq_1377_69", dataOut[88]),
#                  ("ampForFreq_1393_35", dataOut[89]),
#                  ("ampForFreq_1409_00", dataOut[90]),
#                  ("ampForFreq_1424_66", dataOut[91]),
#                  ("ampForFreq_1440_31", dataOut[92]),
#                  ("ampForFreq_1455_97", dataOut[93]),
#                  ("ampForFreq_1471_62", dataOut[94]),
#                  ("ampForFreq_1487_28", dataOut[95]),
#                  ("ampForFreq_1502_94", dataOut[96]),
#                  ("ampForFreq_1518_59", dataOut[97]),
#                  ("ampForFreq_1534_25", dataOut[98]),
#                  ("ampForFreq_1549_90", dataOut[99]),
#                  ("ampForFreq_1565_56", dataOut[100]),
#                  ("ampForFreq_1581_21", dataOut[101]),
#                  ("ampForFreq_1596_87", dataOut[102]),
#                  ("ampForFreq_1612_52", dataOut[103]),
#                  ("ampForFreq_1628_18", dataOut[104]),
#                  ("ampForFreq_1643_84", dataOut[105]),
#                  ("ampForFreq_1659_49", dataOut[106]),
#                  ("ampForFreq_1675_15", dataOut[107]),
#                  ("ampForFreq_1690_80", dataOut[108]),
#                  ("ampForFreq_1706_46", dataOut[109]),
#                  ("ampForFreq_1722_11", dataOut[110]),
#                  ("ampForFreq_1737_77", dataOut[111]),
#                  ("ampForFreq_1753_42", dataOut[112]),
#                  ("ampForFreq_1769_08", dataOut[113]),
#                  ("ampForFreq_1784_74", dataOut[114]),
#                  ("ampForFreq_1800_39", dataOut[115]),
#                  ("ampForFreq_1816_05", dataOut[116]),
#                  ("ampForFreq_1831_70", dataOut[117]),
#                  ("ampForFreq_1847_36", dataOut[118]),
#                  ("ampForFreq_1863_01", dataOut[119]),
#                  ("ampForFreq_1878_67", dataOut[120]),
#                  ("ampForFreq_1894_32", dataOut[121]),
#                  ("ampForFreq_1909_98", dataOut[122]),
#                  ("ampForFreq_1925_64", dataOut[123]),
#                  ("ampForFreq_1941_29", dataOut[124]),
#                  ("ampForFreq_1956_95", dataOut[125]),
#                  ("ampForFreq_1972_60", dataOut[126]),
#                  ("ampForFreq_1988_26", dataOut[127]),
#                  ("ampForFreq_2003_91", dataOut[128]),
#                  ("ampForFreq_2019_57", dataOut[129]),
#                  ("ampForFreq_2035_23", dataOut[130]),
#                  ("ampForFreq_2050_88", dataOut[131]),
#                  ("ampForFreq_2066_54", dataOut[132]),
#                  ("ampForFreq_2082_19", dataOut[133]),
#                  ("ampForFreq_2097_85", dataOut[134]),
#                  ("ampForFreq_2113_50", dataOut[135]),
#                  ("ampForFreq_2129_16", dataOut[136]),
#                  ("ampForFreq_2144_81", dataOut[137]),
#                  ("ampForFreq_2160_47", dataOut[138]),
#                  ("ampForFreq_2176_13", dataOut[139]),
#                  ("ampForFreq_2191_78", dataOut[140]),
#                  ("ampForFreq_2207_44", dataOut[141]),
#                  ("ampForFreq_2223_09", dataOut[142]),
#                  ("ampForFreq_2238_75", dataOut[143]),
#                  ("ampForFreq_2254_40", dataOut[144]),
#                  ("ampForFreq_2270_06", dataOut[145]),
#                  ("ampForFreq_2285_71", dataOut[146]),
#                  ("ampForFreq_2301_37", dataOut[147]),
#                  ("ampForFreq_2317_03", dataOut[148]),
#                  ("ampForFreq_2332_68", dataOut[149]),
#                  ("ampForFreq_2348_34", dataOut[150]),
#                  ("ampForFreq_2363_99", dataOut[151]),
#                  ("ampForFreq_2379_65", dataOut[152]),
#                  ("ampForFreq_2395_30", dataOut[153]),
#                  ("ampForFreq_2410_96", dataOut[154]),
#                  ("ampForFreq_2426_61", dataOut[155]),
#                  ("ampForFreq_2442_27", dataOut[156]),
#                  ("ampForFreq_2457_93", dataOut[157]),
#                  ("ampForFreq_2473_58", dataOut[158]),
#                  ("ampForFreq_2489_24", dataOut[159]),
#                  ("ampForFreq_2504_89", dataOut[160]),
#                  ("ampForFreq_2520_55", dataOut[161]),
#                  ("ampForFreq_2536_20", dataOut[162]),
#                  ("ampForFreq_2551_86", dataOut[163]),
#                  ("ampForFreq_2567_51", dataOut[164]),
#                  ("ampForFreq_2583_17", dataOut[165]),
#                  ("ampForFreq_2598_83", dataOut[166]),
#                  ("ampForFreq_2614_48", dataOut[167]),
#                  ("ampForFreq_2630_14", dataOut[168]),
#                  ("ampForFreq_2645_79", dataOut[169]),
#                  ("ampForFreq_2661_45", dataOut[160]),
#                  ("ampForFreq_2677_10", dataOut[171]),
#                  ("ampForFreq_2692_76", dataOut[172]),
#                  ("ampForFreq_2708_41", dataOut[173]),
#                  ("ampForFreq_2724_07", dataOut[174]),
#                  ("ampForFreq_2739_73", dataOut[175]),
#                  ("ampForFreq_2755_38", dataOut[176]),
#                  ("ampForFreq_2771_04", dataOut[177]),
#                  ("ampForFreq_2786_69", dataOut[178]),
#                  ("ampForFreq_2802_35", dataOut[179]),
#                  ("ampForFreq_2818_00", dataOut[180]),
#                  ("ampForFreq_2833_66", dataOut[181]),
#                  ("ampForFreq_2849_32", dataOut[182]),
#                  ("ampForFreq_2864_97", dataOut[183]),
#                  ("ampForFreq_2880_63", dataOut[184]),
#                  ("ampForFreq_2896_28", dataOut[185]),
#                  ("ampForFreq_2911_94", dataOut[186]),
#                  ("ampForFreq_2927_59", dataOut[187]),
#                  ("ampForFreq_2943_25", dataOut[188]),
#                  ("ampForFreq_2958_90", dataOut[189]),
#                  ("ampForFreq_2974_56", dataOut[190]),
#                  ("ampForFreq_2990_22", dataOut[191]),
#                  ("ampForFreq_3005_87", dataOut[192]),
#                  ("ampForFreq_3021_53", dataOut[193]),
#                  ("ampForFreq_3037_18", dataOut[194]),
#                  ("ampForFreq_3052_84", dataOut[195]),
#                  ("ampForFreq_3068_49", dataOut[196]),
#                  ("ampForFreq_3084_15", dataOut[197]),
#                  ("ampForFreq_3099_80", dataOut[198]),
#                  ("ampForFreq_3115_46", dataOut[199]),
#                  ("ampForFreq_3131_12", dataOut[200]),
#                  ("ampForFreq_3146_77", dataOut[201]),
#                  ("ampForFreq_3162_43", dataOut[202]),
#                  ("ampForFreq_3178_08", dataOut[203]),
#                  ("ampForFreq_3193_74", dataOut[204]),
#                  ("ampForFreq_3209_39", dataOut[205]),
#                  ("ampForFreq_3225_05", dataOut[206]),
#                  ("ampForFreq_3240_70", dataOut[207]),
#                  ("ampForFreq_3256_36", dataOut[208]),
#                  ("ampForFreq_3272_02", dataOut[209]),
#                  ("ampForFreq_3287_67", dataOut[200]),
#                  ("ampForFreq_3303_33", dataOut[211]),
#                  ("ampForFreq_3318_98", dataOut[212]),
#                  ("ampForFreq_3334_64", dataOut[213]),
#                  ("ampForFreq_3350_29", dataOut[214]),
#                  ("ampForFreq_3365_95", dataOut[215]),
#                  ("ampForFreq_3381_60", dataOut[216]),
#                  ("ampForFreq_3397_26", dataOut[217]),
#                  ("ampForFreq_3412_92", dataOut[218]),
#                  ("ampForFreq_3428_57", dataOut[219]),
#                  ("ampForFreq_3444_23", dataOut[220]),
#                  ("ampForFreq_3459_88", dataOut[221]),
#                  ("ampForFreq_3475_54", dataOut[222]),
#                  ("ampForFreq_3491_19", dataOut[223]),
#                  ("ampForFreq_3506_85", dataOut[224]),
#                  ("ampForFreq_3522_50", dataOut[225]),
#                  ("ampForFreq_3538_16", dataOut[226]),
#                  ("ampForFreq_3553_82", dataOut[227]),
#                  ("ampForFreq_3569_47", dataOut[228]),
#                  ("ampForFreq_3585_13", dataOut[229]),
#                  ("ampForFreq_3600_78", dataOut[230]),
#                  ("ampForFreq_3616_44", dataOut[231]),
#                  ("ampForFreq_3632_09", dataOut[232]),
#                  ("ampForFreq_3647_75", dataOut[233]),
#                  ("ampForFreq_3663_41", dataOut[234]),
#                  ("ampForFreq_3679_06", dataOut[235]),
#                  ("ampForFreq_3694_72", dataOut[236]),
#                  ("ampForFreq_3710_37", dataOut[237]),
#                  ("ampForFreq_3726_03", dataOut[238]),
#                  ("ampForFreq_3741_68", dataOut[239]),
#                  ("ampForFreq_3757_34", dataOut[240]),
#                  ("ampForFreq_3772_99", dataOut[241]),
#                  ("ampForFreq_3788_65", dataOut[242]),
#                  ("ampForFreq_3804_31", dataOut[243]),
#                  ("ampForFreq_3819_96", dataOut[244]),
#                  ("ampForFreq_3835_62", dataOut[245]),
#                  ("ampForFreq_3851_27", dataOut[246]),
#                  ("ampForFreq_3866_93", dataOut[247]),
#                  ("ampForFreq_3882_58", dataOut[248]),
#                  ("ampForFreq_3898_24", dataOut[249]),
#                  ("ampForFreq_3913_89", dataOut[250]),
#                  ("ampForFreq_3929_55", dataOut[251]),
#                  ("ampForFreq_3945_21", dataOut[252]),
#                  ("ampForFreq_3960_86", dataOut[253]),
#                  ("ampForFreq_3976_52", dataOut[254]),
#                  ("ampForFreq_3992_17", dataOut[255]),
#                  ("ampForFreq_4007_83", dataOut[256]),
#                  ("ampForFreq_4023_48", dataOut[257]),
#                  ("ampForFreq_4039_14", dataOut[258]),
#                  ("ampForFreq_4054_79", dataOut[259]),
#                  ("ampForFreq_4070_45", dataOut[260]),
#                  ("ampForFreq_4086_11", dataOut[261]),
#                  ("ampForFreq_4101_76", dataOut[262]),
#                  ("ampForFreq_4117_42", dataOut[263]),
#                  ("ampForFreq_4133_07", dataOut[264]),
#                  ("ampForFreq_4148_73", dataOut[265]),
#                  ("ampForFreq_4164_38", dataOut[266]),
#                  ("ampForFreq_4180_04", dataOut[267]),
#                  ("ampForFreq_4195_69", dataOut[268]),
#                  ("ampForFreq_4211_35", dataOut[269]),
#                  ("ampForFreq_4227_01", dataOut[270]),
#                  ("ampForFreq_4242_66", dataOut[271]),
#                  ("ampForFreq_4258_32", dataOut[272]),
#                  ("ampForFreq_4273_97", dataOut[273]),
#                  ("ampForFreq_4289_63", dataOut[274]),
#                  ("ampForFreq_4305_28", dataOut[275]),
#                  ("ampForFreq_4320_94", dataOut[276]),
#                  ("ampForFreq_4336_59", dataOut[277]),
#                  ("ampForFreq_4352_25", dataOut[278]),
#                  ("ampForFreq_4367_91", dataOut[279]),
#                  ("ampForFreq_4383_56", dataOut[280]),
#                  ("ampForFreq_4399_22", dataOut[281]),
#                  ("ampForFreq_4414_87", dataOut[282]),
#                  ("ampForFreq_4430_53", dataOut[283]),
#                  ("ampForFreq_4446_18", dataOut[284]),
#                  ("ampForFreq_4461_84", dataOut[285]),
#                  ("ampForFreq_4477_50", dataOut[286]),
#                  ("ampForFreq_4493_15", dataOut[287]),
#                  ("ampForFreq_4508_81", dataOut[288]),
#                  ("ampForFreq_4524_46", dataOut[289]),
#                  ("ampForFreq_4540_12", dataOut[290]),
#                  ("ampForFreq_4555_77", dataOut[291]),
#                  ("ampForFreq_4571_43", dataOut[292]),
#                  ("ampForFreq_4587_08", dataOut[293]),
#                  ("ampForFreq_4602_74", dataOut[294]),
#                  ("ampForFreq_4618_40", dataOut[295]),
#                  ("ampForFreq_4634_05", dataOut[296]),
#                  ("ampForFreq_4649_71", dataOut[297]),
#                  ("ampForFreq_4665_36", dataOut[298]),
#                  ("ampForFreq_4681_02", dataOut[299]),
#                  ("ampForFreq_4696_67", dataOut[300]),
#                  ("ampForFreq_4712_33", dataOut[301]),
#                  ("ampForFreq_4727_98", dataOut[302]),
#                  ("ampForFreq_4743_64", dataOut[303]),
#                  ("ampForFreq_4759_30", dataOut[304]),
#                  ("ampForFreq_4774_95", dataOut[305]),
#                  ("ampForFreq_4790_61", dataOut[306]),
#                  ("ampForFreq_4806_26", dataOut[307]),
#                  ("ampForFreq_4821_92", dataOut[308]),
#                  ("ampForFreq_4837_57", dataOut[309]),
#                  ("ampForFreq_4853_23", dataOut[310]),
#                  ("ampForFreq_4868_88", dataOut[311]),
#                  ("ampForFreq_4884_54", dataOut[312]),
#                  ("ampForFreq_4900_20", dataOut[313]),
#                  ("ampForFreq_4915_85", dataOut[314]),
#                  ("ampForFreq_4931_51", dataOut[315]),
#                  ("ampForFreq_4947_16", dataOut[316]),
#                  ("ampForFreq_4962_82", dataOut[317]),
#                  ("ampForFreq_4978_47", dataOut[318]),
#                  ("ampForFreq_4994_13", dataOut[319]),
#                  ("ampForFreq_5009_78", dataOut[320]),
#                  ("ampForFreq_5025_44", dataOut[321]),
#                  ("ampForFreq_5041_10", dataOut[322]),
#                  ("ampForFreq_5056_75", dataOut[323]),
#                  ("ampForFreq_5072_41", dataOut[324]),
#                  ("ampForFreq_5088_06", dataOut[325]),
#                  ("ampForFreq_5103_72", dataOut[326]),
#                  ("ampForFreq_5119_37", dataOut[327]),
#                  ("ampForFreq_5135_03", dataOut[328]),
#                  ("ampForFreq_5150_68", dataOut[329]),
#                  ("ampForFreq_5166_34", dataOut[330]),
#                  ("ampForFreq_5182_00", dataOut[331]),
#                  ("ampForFreq_5197_65", dataOut[332]),
#                  ("ampForFreq_5213_31", dataOut[333]),
#                  ("ampForFreq_5228_96", dataOut[334]),
#                  ("ampForFreq_5244_62", dataOut[335]),
#                  ("ampForFreq_5260_27", dataOut[336]),
#                  ("ampForFreq_5275_93", dataOut[337]),
#                  ("ampForFreq_5291_59", dataOut[338]),
#                  ("ampForFreq_5307_24", dataOut[339]),
#                  ("ampForFreq_5322_90", dataOut[340]),
#                  ("ampForFreq_5338_55", dataOut[341]),
#                  ("ampForFreq_5354_21", dataOut[342]),
#                  ("ampForFreq_5369_86", dataOut[343]),
#                  ("ampForFreq_5385_52", dataOut[344]),
#                  ("ampForFreq_5401_17", dataOut[345]),
#                  ("ampForFreq_5416_83", dataOut[346]),
#                  ("ampForFreq_5432_49", dataOut[347]),
#                  ("ampForFreq_5448_14", dataOut[348]),
#                  ("ampForFreq_5463_80", dataOut[349]),
#                  ("ampForFreq_5479_45", dataOut[350]),
#                  ("ampForFreq_5495_11", dataOut[351]),
#                  ("ampForFreq_5510_76", dataOut[352]),
#                  ("ampForFreq_5526_42", dataOut[353]),
#                  ("ampForFreq_5542_07", dataOut[354]),
#                  ("ampForFreq_5557_73", dataOut[355]),
#                  ("ampForFreq_5573_39", dataOut[356]),
#                  ("ampForFreq_5589_04", dataOut[357]),
#                  ("ampForFreq_5604_70", dataOut[358]),
#                  ("ampForFreq_5620_35", dataOut[359]),
#                  ("ampForFreq_5636_01", dataOut[360]),
#                  ("ampForFreq_5651_66", dataOut[361]),
#                  ("ampForFreq_5667_32", dataOut[362]),
#                  ("ampForFreq_5682_97", dataOut[363]),
#                  ("ampForFreq_5698_63", dataOut[364]),
#                  ("ampForFreq_5714_29", dataOut[365]),
#                  ("ampForFreq_5729_94", dataOut[366]),
#                  ("ampForFreq_5745_60", dataOut[367]),
#                  ("ampForFreq_5761_25", dataOut[368]),
#                  ("ampForFreq_5776_91", dataOut[369]),
#                  ("ampForFreq_5792_56", dataOut[370]),
#                  ("ampForFreq_5808_22", dataOut[371]),
#                  ("ampForFreq_5823_87", dataOut[372]),
#                  ("ampForFreq_5839_53", dataOut[373]),
#                  ("ampForFreq_5855_19", dataOut[374]),
#                  ("ampForFreq_5870_84", dataOut[375]),
#                  ("ampForFreq_5886_50", dataOut[376]),
#                  ("ampForFreq_5902_15", dataOut[377]),
#                  ("ampForFreq_5917_81", dataOut[378]),
#                  ("ampForFreq_5933_46", dataOut[379]),
#                  ("ampForFreq_5949_12", dataOut[380]),
#                  ("ampForFreq_5964_77", dataOut[381]),
#                  ("ampForFreq_5980_43", dataOut[382]),
#                  ("ampForFreq_5996_09", dataOut[383]),
#                  ("ampForFreq_6011_74", dataOut[384]),
#                  ("ampForFreq_6027_40", dataOut[385]),
#                  ("ampForFreq_6043_05", dataOut[386]),
#                  ("ampForFreq_6058_71", dataOut[387]),
#                  ("ampForFreq_6074_36", dataOut[388]),
#                  ("ampForFreq_6090_02", dataOut[389]),
#                  ("ampForFreq_6105_68", dataOut[390]),
#                  ("ampForFreq_6121_33", dataOut[391]),
#                  ("ampForFreq_6136_99", dataOut[392]),
#                  ("ampForFreq_6152_64", dataOut[393]),
#                  ("ampForFreq_6168_30", dataOut[394]),
#                  ("ampForFreq_6183_95", dataOut[395]),
#                  ("ampForFreq_6199_61", dataOut[396]),
#                  ("ampForFreq_6215_26", dataOut[397]),
#                  ("ampForFreq_6230_92", dataOut[398]),
#                  ("ampForFreq_6246_58", dataOut[399]),
#                  ("ampForFreq_6262_23", dataOut[400]),
#                  ("ampForFreq_6277_89", dataOut[401]),
#                  ("ampForFreq_6293_54", dataOut[402]),
#                  ("ampForFreq_6309_20", dataOut[403]),
#                  ("ampForFreq_6324_85", dataOut[404]),
#                  ("ampForFreq_6340_51", dataOut[405]),
#                  ("ampForFreq_6356_16", dataOut[406]),
#                  ("ampForFreq_6371_82", dataOut[407]),
#                  ("ampForFreq_6387_48", dataOut[408]),
#                  ("ampForFreq_6403_13", dataOut[409]),
#                  ("ampForFreq_6418_79", dataOut[410]),
#                  ("ampForFreq_6434_44", dataOut[411]),
#                  ("ampForFreq_6450_10", dataOut[412]),
#                  ("ampForFreq_6465_75", dataOut[413]),
#                  ("ampForFreq_6481_41", dataOut[414]),
#                  ("ampForFreq_6497_06", dataOut[415]),
#                  ("ampForFreq_6512_72", dataOut[416]),
#                  ("ampForFreq_6528_38", dataOut[417]),
#                  ("ampForFreq_6544_03", dataOut[418]),
#                  ("ampForFreq_6559_69", dataOut[419]),
#                  ("ampForFreq_6575_34", dataOut[420]),
#                  ("ampForFreq_6591_00", dataOut[421]),
#                  ("ampForFreq_6606_65", dataOut[422]),
#                  ("ampForFreq_6622_31", dataOut[423]),
#                  ("ampForFreq_6637_96", dataOut[424]),
#                  ("ampForFreq_6653_62", dataOut[425]),
#                  ("ampForFreq_6669_28", dataOut[426]),
#                  ("ampForFreq_6684_93", dataOut[427]),
#                  ("ampForFreq_6700_59", dataOut[428]),
#                  ("ampForFreq_6716_24", dataOut[429]),
#                  ("ampForFreq_6731_90", dataOut[430]),
#                  ("ampForFreq_6747_55", dataOut[431]),
#                  ("ampForFreq_6763_21", dataOut[432]),
#                  ("ampForFreq_6778_86", dataOut[433]),
#                  ("ampForFreq_6794_52", dataOut[434]),
#                  ("ampForFreq_6810_18", dataOut[435]),
#                  ("ampForFreq_6825_83", dataOut[436]),
#                  ("ampForFreq_6841_49", dataOut[437]),
#                  ("ampForFreq_6857_14", dataOut[438]),
#                  ("ampForFreq_6872_80", dataOut[439]),
#                  ("ampForFreq_6888_45", dataOut[440]),
#                  ("ampForFreq_6904_11", dataOut[441]),
#                  ("ampForFreq_6919_77", dataOut[442]),
#                  ("ampForFreq_6935_42", dataOut[443]),
#                  ("ampForFreq_6951_08", dataOut[444]),
#                  ("ampForFreq_6966_73", dataOut[445]),
#                  ("ampForFreq_6982_39", dataOut[446]),
#                  ("ampForFreq_6998_04", dataOut[447]),
#                  ("ampForFreq_7013_70", dataOut[448]),
#                  ("ampForFreq_7029_35", dataOut[449]),
#                  ("ampForFreq_7045_01", dataOut[450]),
#                  ("ampForFreq_7060_67", dataOut[451]),
#                  ("ampForFreq_7076_32", dataOut[452]),
#                  ("ampForFreq_7091_98", dataOut[453]),
#                  ("ampForFreq_7107_63", dataOut[454]),
#                  ("ampForFreq_7123_29", dataOut[455]),
#                  ("ampForFreq_7138_94", dataOut[456]),
#                  ("ampForFreq_7154_60", dataOut[457]),
#                  ("ampForFreq_7170_25", dataOut[458]),
#                  ("ampForFreq_7185_91", dataOut[459]),
#                  ("ampForFreq_7201_57", dataOut[460]),
#                  ("ampForFreq_7217_22", dataOut[461]),
#                  ("ampForFreq_7232_88", dataOut[462]),
#                  ("ampForFreq_7248_53", dataOut[463]),
#                  ("ampForFreq_7264_19", dataOut[464]),
#                  ("ampForFreq_7279_84", dataOut[465]),
#                  ("ampForFreq_7295_50", dataOut[466]),
#                  ("ampForFreq_7311_15", dataOut[467]),
#                  ("ampForFreq_7326_81", dataOut[468]),
#                  ("ampForFreq_7342_47", dataOut[469]),
#                  ("ampForFreq_7358_12", dataOut[470]),
#                  ("ampForFreq_7373_78", dataOut[471]),
#                  ("ampForFreq_7389_43", dataOut[472]),
#                  ("ampForFreq_7405_09", dataOut[473]),
#                  ("ampForFreq_7420_74", dataOut[474]),
#                  ("ampForFreq_7436_40", dataOut[475]),
#                  ("ampForFreq_7452_05", dataOut[476]),
#                  ("ampForFreq_7467_71", dataOut[477]),
#                  ("ampForFreq_7483_37", dataOut[478]),
#                  ("ampForFreq_7499_02", dataOut[479]),
#                  ("ampForFreq_7514_68", dataOut[470]),
#                  ("ampForFreq_7530_33", dataOut[481]),
#                  ("ampForFreq_7545_99", dataOut[482]),
#                  ("ampForFreq_7561_64", dataOut[483]),
#                  ("ampForFreq_7577_30", dataOut[484]),
#                  ("ampForFreq_7592_95", dataOut[485]),
#                  ("ampForFreq_7608_61", dataOut[486]),
#                  ("ampForFreq_7624_27", dataOut[487]),
#                  ("ampForFreq_7639_92", dataOut[488]),
#                  ("ampForFreq_7655_58", dataOut[489]),
#                  ("ampForFreq_7671_23", dataOut[490]),
#                  ("ampForFreq_7686_89", dataOut[491]),
#                  ("ampForFreq_7702_54", dataOut[492]),
#                  ("ampForFreq_7718_20", dataOut[493]),
#                  ("ampForFreq_7733_86", dataOut[494]),
#                  ("ampForFreq_7749_51", dataOut[495]),
#                  ("ampForFreq_7765_17", dataOut[496]),
#                  ("ampForFreq_7780_82", dataOut[497]),
#                  ("ampForFreq_7796_48", dataOut[498]),
#                  ("ampForFreq_7812_13", dataOut[499]),
#                  ("ampForFreq_7827_79", dataOut[500]),
#                  ("ampForFreq_7843_44", dataOut[501]),
#                  ("ampForFreq_7859_10", dataOut[502]),
#                  ("ampForFreq_7874_76", dataOut[503]),
#                  ("ampForFreq_7890_41", dataOut[504]),
#                  ("ampForFreq_7906_07", dataOut[505]),
#                  ("ampForFreq_7921_72", dataOut[506]),
#                  ("ampForFreq_7937_38", dataOut[507]),
#                  ("ampForFreq_7953_03", dataOut[508]),
#                  ("ampForFreq_7968_69", dataOut[509]),
#                  ("ampForFreq_7984_34", dataOut[510]),
#                  ("ampForFreq_8000_00", dataOut[511])
#     	     ])
#
#         sensorFinisher(dateTime,sensorName,sensorDictionary)
#



def HTU21DWrite(sensorData,dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "HTU21D"
    dataLength = 2
    if(len(dataOut) ==(dataLength +1)):
        sensorDictionary = OrderedDict([
                ("dateTime"    , str(dateTime)),
        	    ("temperature" ,dataOut[0]),
            	("humidity"    ,dataOut[1])
        	     ])


        #Getting Write Path
        sensorFinisher(dateTime,sensorName,sensorDictionary)

def BMP280Write(sensorData,dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "BMP280"
    dataLength = 2
    if(len(dataOut) == (dataLength +1)):
        sensorDictionary =  OrderedDict([
                ("dateTime"     , str(dateTime)),
        		("temperature"  ,dataOut[0]),
            	("pressure"     ,dataOut[1])
                ])

        #Getting Write Path
        sensorFinisher(dateTime,sensorName,sensorDictionary)

def INA219Write(sensorData,dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "INA219"
    dataLength = 5

    if(len(dataOut) == (dataLength +1)):
        sensorDictionary = OrderedDict([
                ("dateTime"      ,str(dateTime)),
        	    ("shuntVoltage"  ,dataOut[0]),
            	("busVoltage"    ,dataOut[1]),
                ("currentMA"     ,dataOut[2]),
                ("powerMW"       ,dataOut[3]),
                ("loadVoltage"   ,dataOut[4])
        	     ])

        #Getting Write Path
        sensorFinisher(dateTime,sensorName,sensorDictionary)

def OPCN2Write(sensorData,dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "OPCN2"
    dataLength= 28
    if(len(dataOut) == (dataLength +1)):
        sensorDictionary = OrderedDict([
                ("dateTime"    ,str(dateTime)),
        		("valid"       ,dataOut[0]),
            	("binCount0"   ,dataOut[1]),
            	("binCount1"   ,dataOut[2]),
            	("binCount2"   ,dataOut[3]),
            	("binCount3"   ,dataOut[4]),
            	("binCount4"   ,dataOut[5]),
            	("binCount5"   ,dataOut[6]),
            	("binCount6"   ,dataOut[7]),
            	("binCount7"   ,dataOut[8]),
            	("binCount8"   ,dataOut[9]),
            	("binCount9"   ,dataOut[10]),
            	("binCount10"  ,dataOut[11]),
            	("binCount11"  ,dataOut[12]),
            	("binCount12"  ,dataOut[13]),
            	("binCount13"  ,dataOut[14]),
            	("binCount14"  ,dataOut[15]),
                ("binCount15"  ,dataOut[16]),
                ("bin1TimeToCross"      ,dataOut[17]),
                ("bin3TimeToCross"      ,dataOut[18]),
                ("bin5TimeToCross"      ,dataOut[19]),
                ("bin7TimeToCross"      ,dataOut[20]),
                ("sampleFlowRate"       ,dataOut[21]),
                ("temperatureOrPressure",dataOut[22]),
                ("samplingPeriod"       ,dataOut[23]),
                ("checkSum"             ,dataOut[24]),
                ("pm1"                  ,dataOut[25]),
                ("pm2_5"                ,dataOut[26]),
                ("pm10"                 ,dataOut[27])
                ])

        #Getting Write Path
        sensorFinisher(dateTime,sensorName,sensorDictionary)



def OPCN3Write(sensorData,dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "OPCN3"
    valid      = dataOut[0]
    dataLength=43
    if((len(dataOut) == (dataLength +1)) and valid =="1"):
        sensorDictionary = OrderedDict([
                ("dateTime"    ,str(dateTime)),
        		("valid"       ,dataOut[0]),
            	("binCount0"   ,dataOut[1]),
            	("binCount1"   ,dataOut[2]),
            	("binCount2"   ,dataOut[3]),
            	("binCount3"   ,dataOut[4]),
            	("binCount4"   ,dataOut[5]),
            	("binCount5"   ,dataOut[6]),
            	("binCount6"   ,dataOut[7]),
            	("binCount7"   ,dataOut[8]),
            	("binCount8"   ,dataOut[9]),
            	("binCount9"   ,dataOut[10]),
            	("binCount10"  ,dataOut[11]),
            	("binCount11"  ,dataOut[12]),
            	("binCount12"  ,dataOut[13]),
            	("binCount13"  ,dataOut[14]),
            	("binCount14"  ,dataOut[15]),
            	("binCount15"  ,dataOut[16]),
            	("binCount16"  ,dataOut[17]),
            	("binCount17"  ,dataOut[18]),
            	("binCount18"  ,dataOut[19]),
            	("binCount19"  ,dataOut[20]),
            	("binCount20"  ,dataOut[21]),
            	("binCount21"  ,dataOut[22]),
            	("binCount22"  ,dataOut[23]),
            	("binCount23"  ,dataOut[24]),
                ("bin1TimeToCross"      ,dataOut[25]),
                ("bin3TimeToCross"      ,dataOut[26]),
                ("bin5TimeToCross"      ,dataOut[27]),
                ("bin7TimeToCross"      ,dataOut[28]),
                ("samplingPeriod"       ,dataOut[29]),
                ("sampleFlowRate"       ,dataOut[30]),
                ("temperature"          ,str(float(dataOut[31])/1000)),
                ("humidity"             ,str(float(dataOut[32])/500)),
                ("pm1"                ,dataOut[33]),
                ("pm2_5"              ,dataOut[34]),
                ("pm10"               ,dataOut[35]),
                ("rejectCountGlitch"    ,dataOut[36]),
                ("rejectCountLongTOF"   ,dataOut[37]),
                ("rejectCountRatio"     ,dataOut[38]),
                ("rejectCountOutOfRange",dataOut[39]),
                ("fanRevCount"          ,dataOut[40]),
                ("laserStatus"          ,dataOut[41]),
                ("checkSum"             ,dataOut[42])
                ])

        #Getting Write Path
        sensorFinisher(dateTime,sensorName,sensorDictionary)

def PPD42NSDuoWrite(sensorData,dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "PPD42NSDuo"
    dataLength = 8
    if(len(dataOut) ==(dataLength +1)):
        sensorDictionary = OrderedDict([
                ("dateTime"           ,str(dateTime)),
                ("sampleTimeSeconds"  ,dataOut[0]),
        	    ("LPOPmMid"           ,dataOut[1]),
            	("LPOPm10"            ,dataOut[2]),
                ("ratioPmMid"         ,dataOut[3]),
                ("ratioPm10"          ,dataOut[4]),
        	    ("concentrationPmMid" ,dataOut[5]),
                ("concentrationPm2_5" ,dataOut[6]),
                ("concentrationPm10"  ,dataOut[7])
        	     ])

        sensorFinisher(dateTime,sensorName,sensorDictionary)


def PPD42NSWrite(sensorData,dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "PPD42NS"
    dataLength = 4
    if(len(dataOut) ==(dataLength +1)):
        sensorDictionary = OrderedDict([
                ("dateTime"           ,str(dateTime)),
        	    ("lowPulseOccupancy"  ,dataOut[0]),
            	("concentration"      ,dataOut[1]),
                ("ratio"              ,dataOut[2]),
                ("timeSpent"          ,dataOut[3])
        	     ])

        sensorFinisher(dateTime,sensorName,sensorDictionary)


def getDeltaTime(beginTime,deltaWanted):
    return (time.time() - beginTime)> deltaWanted

def GPSGPGGAWrite(dataString,dateTime):

    dataStringPost = dataString.replace('\n', '')
    sensorData = pynmea2.parse(dataStringPost)
    if(sensorData.gps_qual>0):
        sensorName = "GPSGPGGA"
        sensorDictionary = OrderedDict([
                ("dateTime"          ,str(dateTime)),
                ("timestamp"         ,sensorData.timestamp),
                ("latitude"          ,sensorData.lat),
                ("latitudeDirection" ,sensorData.lat_dir),
                ("longitude"         ,sensorData.lon),
                ("longitudeDirection",sensorData.lon_dir),
                ("gpsQuality"        ,sensorData.gps_qual),
                ("numberOfSatellites",sensorData.num_sats),
                ("HorizontalDilution",sensorData.horizontal_dil),
                ("altitude"          ,sensorData.altitude),
                ("altitudeUnits"     ,sensorData.altitude_units),
                ("undulation"        ,sensorData.geo_sep),
                ("undulationUnits"   ,sensorData.geo_sep_units),
                ("age"               ,sensorData.age_gps_data),
                ("stationID"         ,sensorData.ref_station_id)
        	     ])

        #Getting Write Path
        sensorFinisher(dateTime,sensorName,sensorDictionary)

def GPSGPRMCWrite(dataString,dateTime):

    dataStringPost = dataString.replace('\n', '')
    sensorData = pynmea2.parse(dataStringPost)
    if(sensorData.status=='A'):
        sensorName = "GPSGPRMC"
        sensorDictionary = OrderedDict([
                ("dateTime"             ,str(dateTime)),
                ("timestamp"            ,sensorData.timestamp),
                ("status"               ,sensorData.status),
                ("latitude"             ,sensorData.lat),
                ("latitudeDirection"    ,sensorData.lat_dir),
                ("longitude"            ,sensorData.lon),
                ("longitudeDirection"   ,sensorData.lon_dir),
                ("speedOverGround"      ,sensorData.spd_over_grnd),
                ("trueCourse"           ,sensorData.true_course),
                ("dateStamp"            ,sensorData.datestamp),
                ("magVariation"         ,sensorData.mag_variation),
                ("magVariationDirection",sensorData.mag_var_dir)
                 ])

        #Getting Write Path
        sensorFinisher(dateTime,sensorName,sensorDictionary)




def writeCSV2(writePath,sensorDictionary,exists):
    keys =  list(sensorDictionary.keys())
    with open(writePath, 'a') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        # print(exists)
        if(not(exists)):
            writer.writeheader()
        writer.writerow(sensorDictionary)


# def writeHDF5Latest(writePath,sensorDictionary,sensorName):
#     try:
#         dd.io.save(dataFolder+sensorName+".h5", sensorDictionary)
#     except:
#         print("Data Conflict!")


def getWritePathIP(labelIn,dateTime):
    #Example  : MINTS_0061.csv
    writePath = dataFolder+"/"+macAddress+"/"+"MINTS_"+ macAddress+ "_IP.csv"
    return writePath;


def getWritePathSnaps(labelIn,dateTime):
    #Example  : MINTS_0061_OOPCN3_2019_01_04.csv
    writePath = dataFolder+"/"+macAddress+"/"+str(dateTime.year).zfill(4)  + "/" + str(dateTime.month).zfill(2)+ "/"+str(dateTime.day).zfill(2)+"/snaps/MINTS_"+ macAddress+ "_" +labelIn + "_" + str(dateTime.year).zfill(4) + "_" +str(dateTime.month).zfill(2) + "_" +str(dateTime.day).zfill(2) + "_" +str(dateTime.hour).zfill(2) + "_" +str(dateTime.minute).zfill(2)+ "_" +str(dateTime.second).zfill(2) +".png"
    return writePath;



def getWritePath(labelIn,dateTime):
    #Example  : MINTS_0061_OOPCN3_2019_01_04.csv
    writePath = dataFolder+"/"+macAddress+"/"+str(dateTime.year).zfill(4)  + "/" + str(dateTime.month).zfill(2)+ "/"+str(dateTime.day).zfill(2)+"/"+ "MINTS_"+ macAddress+ "_" +labelIn + "_" + str(dateTime.year).zfill(4) + "_" +str(dateTime.month).zfill(2) + "_" +str(dateTime.day).zfill(2) +".csv"
    return writePath;

def getWritePathUnpublished(labelIn,dateTime):
    #Example  : MINTS_0061_OOPCN3_2019_01_04.csv
    writePath = dataFolderUnpublished+"/"+macAddress+"/"+str(dateTime.year).zfill(4)  + "/" + str(dateTime.month).zfill(2)+ "/"+str(dateTime.day).zfill(2)+"/"+ "MINTS_"+ macAddress+ "_" +labelIn + "_" + str(dateTime.year).zfill(4) + "_" +str(dateTime.month).zfill(2) + "_" +str(dateTime.day).zfill(2) +".csv"
    return writePath;



def getListDictionaryFromPath(dirPath):
    print("Reading : "+ dirPath)
    reader = csv.DictReader(open(dirPath))
    reader = list(reader)

def fixCSV(keyIn,valueIn,currentDictionary):
    editedList       = editDictionaryList(currentDictionary,keyIn,valueIn)
    return editedList

def editDictionaryList(dictionaryListIn,keyIn,valueIn):
    for dictionaryIn in dictionaryListIn:
        dictionaryIn[keyIn] = valueIn

    return dictionaryListIn

def getDateDataOrganized(currentCSV,nodeID):
    currentCSVName = os.path.basename(currentCSV)
    nameOnly = currentCSVName.split('-Organized.')
    dateOnly = nameOnly[0].split(nodeID+'-')
    print(dateOnly)
    dateInfo = dateOnly[1].split('-')
    print(dateInfo)
    return dateInfo


def getFilePathsforOrganizedNodes(nodeID,subFolder):
    nodeFolder = subFolder+ nodeID+'/';
    pattern = "*Organized.csv"
    fileList = [];
    for path, subdirs, files in os.walk(nodeFolder):
        for name in files:
            if fnmatch(name, pattern):
                fileList.append(os.path.join(path, name))
    return sorted(fileList)


def getLocationList(directory, suffix=".csv"):
    filenames = listdir(directory)
    dateList = [ filename for filename in filenames if filename.endswith( suffix ) ]
    return sorted(dateList)


def getListDictionaryCSV(inputPath):
    # the path will depend on the node ID
    reader = csv.DictReader(open(inputPath))
    reader = list(reader)
    return reader

def writeCSV(reader,keys,outputPath):
    directoryCheck(outputPath)
    csvWriter(outputPath,reader,keys)

def directoryCheck(outputPath):
    exists = os.path.isfile(outputPath)
    directoryIn = os.path.dirname(outputPath)
    if not os.path.exists(directoryIn):
        os.makedirs(directoryIn)
    return exists

def csvWriter(writePath,organizedData,keys):
    with open(writePath,'w') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(organizedData)


def gainDirectoryInfo(dailyDownloadLocation):
    directoryPaths = []
    directoryNames = []
    directoryFiles = []
    for (dirpath, dirnames, filenames) in walk(dailyDownloadLocation):
        directoryPaths.extend(dirpath)
        directoryNames.extend(dirnames)
        directoryFiles.extend(filenames)

    return directoryPaths,directoryNames,directoryFiles;
