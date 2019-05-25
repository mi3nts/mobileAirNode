#!/bin/bash
#
sleep 30
python3 nanoReader0.py &
sleep 5
python3 nanoReader1.py &
# sleep 5
# python3 nanoReader2.py &
sleep 5
python3 audioReader.py &
sleep 5
python3 thermalCamReader.py &
sleep 5
python3 ipReader.py &
sleep 10
cd odroidShow2 && python3 mintsShow2.py


#@reboot cd /home/teamlary/gitHubRepos/Lakitha/UTDNodes/firmware/xu4 && ./runAll.sh
