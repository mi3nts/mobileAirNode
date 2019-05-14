sleep 5 
kill $(ps aux | grep '[p]ython3 thermalCamReader.py' | awk '{print $2}') &
sleep 5 
cd /home/teamlary/gitHubRepos/Lakitha/mobileAirNode/firmware/xu4 && python3 thermalCamReaderWithDisplay.py



