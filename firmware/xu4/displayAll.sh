sleep 5 
cd /home/teamlary/gitHubRepos/Lakitha/visualMints/firmware && python3 MGS001Visual.py &
sleep 5 
cd /home/teamlary/gitHubRepos/Lakitha/visualMints/firmware && python3 MI305Visual.py &
sleep 5
cd /home/teamlary/gitHubRepos/Lakitha/visualMints/firmware && python3 OPCN3Visual.py &
sleep 5
kill $(ps aux | grep '[p]ython3 thermalCamReader.py' | awk '{print $2}') &
sleep 5 
cd /home/teamlary/gitHubRepos/Lakitha/mobileAirNode/firmware/xu4 && python3 thermalCamReaderWithDisplay.py
sleep 5 


