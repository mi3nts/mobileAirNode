

import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import time
import sys
from matplotlib import style
from scipy.fftpack import fft
import serial
import datetime
from mintsXU4 import mintsSensorReader as mSR
from mintsXU4 import mintsDefinitions as mD
import wave

dataFolder   = mD.dataFolder
nanoPorts    = mD.nanoPorts


powerSpectrumWritePeriod = 1
wavWritePeriod           = 60


FORMAT = pyaudio.paInt16 # We use 16bit format per sample
CHANNELS = 1
RATE = 16000
CHUNK = 1024 # 1024bytes of data red from a buffer
INTERVAL = 1/RATE

audio = pyaudio.PyAudio()

# start Recording
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True)#,


def main():

    global keep_going
    keep_going = True

    # plt.show()


    startTimeWav = time.time()
    startTimePS  = time.time()
    audioDataWav  = []
    dateTimeWav = datetime.datetime.now()
    xf = np.linspace(0.0, 1.0/(2.0*INTERVAL), CHUNK//2)
    stream.start_stream()
    while keep_going:
        try:

            audioDataNow  = stream.read(CHUNK)
            audioDataWav.append(audioDataNow)

            if(time.time()-startTimePS>powerSpectrumWritePeriod ):
                yf  = fft(np.fromstring(audioDataNow, np.int16))
                powerSpectrum = 2.0/CHUNK * np.abs(yf[0:CHUNK//2])
                mSR.MI305Write(powerSpectrum,datetime.datetime.now())
                startTimePS = time.time()
                maxInd = np.argmax(powerSpectrum)
                print(xf[maxInd])

#            if(time.time()-startTimeWav> wavWritePeriod):
#                mSR.sensorFinisherAudio(dateTimeWav,"MI305",audioDataWav,CHANNELS,FORMAT,RATE,audio)
#                audioDataWav  = []
#                startTimeWav  = time.time()
#                dateTimeWav   =  datetime.datetime.now()


        except KeyboardInterrupt:
            keep_going=False
        except:
            pass
    #
    # # Close up shop (currently not used because KeyboardInterrupt
    # is the only way to close)
    stream.stop_stream()
    stream.close()
    audio.terminate()


# def returnPowerSpectrum():
#     yf            = fft(np.fromstring(stream.read(CHUNK), np.int16))
#     powerSpectrum = 2.0/CHUNK * np.abs(yf[0:CHUNK//2])
#     return powerSpectrum




if __name__ == "__main__":
   main()
