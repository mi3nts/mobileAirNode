#!/bin/bash
#
sleep 60
python3 nanoReader0.py &
sleep 5
python3 nanoReader1.py &
sleep 5
python3 nanoReader2.py &
sleep 5
python3 GPSReader.py &
sleep 5
python3 ipReader.py

# python3 centralNodeReaderNano.py &
# sleep 10
# cd odroidShow2 && python3 mintsShow2.py
