from datetime import timezone
import time
import os
import datetime
import numpy as np
import pickle
from skimage import io, color
import cv2
import h5py
# import hdf5storage
import json
from collections import OrderedDict
try:
  from queue import Queue
except ImportError:
  from Queue import Queue
import platform


from mintsXU4 import mintsSkyCamReader as mSCR
from mintsXU4 import mintsSensorReader as mSR
from mintsXU4 import mintsDefinitions as mD
from mintsXU4.mintsThermal import *
from scipy.io import savemat


def main():
  ctx  = POINTER(uvc_context)()
  dev  = POINTER(uvc_device)()
  devh = POINTER(uvc_device_handle)()
  ctrl = uvc_stream_ctrl()

  res = libuvc.uvc_init(byref(ctx), 0)

  if res < 0:
    print("uvc_init error")
    exit(1)

  try:
    res = libuvc.uvc_find_device(ctx, byref(dev), PT_USB_VID, PT_USB_PID, 0)
    if res < 0:
      print("uvc_find_device error")
      exit(1)

    try:
      res = libuvc.uvc_open(dev, byref(devh))
      if res < 0:
        print("uvc_open error")
        exit(1)

      print("device opened!")
      #
      # print_device_info(devh)
      # print_device_formats(devh)

      frame_formats = uvc_get_frame_formats_by_guid(devh, VS_FMT_GUID_Y16)

      if len(frame_formats) == 0:
        print("device does not support Y16")
        exit(1)

      libuvc.uvc_get_stream_ctrl_format_size(devh, byref(ctrl), UVC_FRAME_FORMAT_Y16,
        frame_formats[0].wWidth, frame_formats[0].wHeight, int(1e7 / frame_formats[0].dwDefaultFrameInterval)
      )

      res = libuvc.uvc_start_streaming(devh, byref(ctrl), PTR_PY_FRAME_CALLBACK, None, 0)

      if res < 0:
        print("uvc_start_streaming failed: {0}".format(res))
        exit(1)

      try:
        data = q.get(True, 500)
        dateTime = datetime.datetime.now()

        if data is not None:

            dataKelvin  = cv2.resize(data[:,:], (640, 480))
            dataCelcius = ktoc(dataKelvin)
            minCelcius, maxCelcius, minLocation, maxLocation = cv2.minMaxLoc(dataCelcius)
            sensorDictionary =  OrderedDict([
                ("dateTime"     , str(dateTime)),
        		("maxTemperature"  ,maxCelcius),
                ("minTemperature"  ,minCelcius),
            	("maxTempLocX"     ,maxLocation[0]),
                ("maxTempLocY"     ,maxLocation[1]),
            	("minTempLocX"     ,minLocation[0]),
                ("minTempLocY"     ,minLocation[1])
                ])

            mSR.sensorFinisher(dateTime,"FLIR001",sensorDictionary)
            mSR.sensorFinisherThermal(dateTime,"FLIR001",sensorDictionary,dataCelcius)
            print(" ")
            print("============== MINTS Thermal ==============")
            print(" ")
            print("Maximum Temperature Read:"+ str(maxCelcius))
            print("Maximum Temperature Location X:"+ str(maxLocation[0]))
            print("Maximum Temperature Location Y:"+ str(maxLocation[1]))
            print("Minimum Temperature Read:" + str(minCelcius))
            print("Minimum Temperature Location X:"+ str(minLocation[0]))
            print("Minimum Temperature Location Y:"+ str(minLocation[1]))
            print(" ")
            print("============== MINTS Thermal ==============")
            print(type(dataCelcius))
            print(dataCelcius.shape)
            print(" ")
            print("============== MINTS Thermal ==============")
            print(" ")
            time.sleep(1)
            print(" ")
            print("============== MINTS Thermal ==============")
            print(" ")

      finally:
        libuvc.uvc_stop_streaming(devh)
      #
      # print("done")
    finally:
      libuvc.uvc_unref_device(dev)
  finally:
    libuvc.uvc_exit(ctx)




if __name__ == '__main__':
  main()