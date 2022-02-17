# mobileAirNode
## Wiring 

 OPC pins goinf rom left to right 

| Nano        | Nano Pin  | All Pins | OPC Pin | Twisted Pair Color |
|-------------|-----------|----------|---------|--------------------|
| Vcc         | 5v        | Vcc      | 1       | Orange Spots       |
| Sck         | D13       | Sck      | 2       | Blue Stripe        |
| MISO        | D12       | SDO      | 3       | Green Spot         |
| MOSI        | D11       | SDI      | 4       | Green Stripes      |
| Digital Pin | D10       | SS       | 5       | Blue Spots         |
| Gnd         | gnd       | GND      | 6       |   Orange Stripe     |
| SCL         | A5        |          |         |  Brown Spots     |
| SDA         | A4        |          |         | BrownStripe      |

- crontab 
```*/1 * * * * cd /home/teamlary/gitHubRepos/Lakitha/mobileAirNode/firmware/xu4 && python3 wavToMp3.py ```

- udev rule 
```SUBSYSTEMS=="usb", ATTRS{idVendor}=="08bb", ATTRS{idProduct}=="2902", GROUP="users", MODE="0666"```

- IP Addresses for the robotic Team

  - Otter On Board Combuter: 192.168.1.2
  - Otter Payload PC: 192.168.1.3
  - Otter Biosonics MX: 192.168.1.201
  - Otter Camera: 192.168.1.5
  
  - Show Side (Trailer) Radio: 192.168.1.10
  - Boat (Otter) Radio: 192.168.1.20
  - Arial Vehicle Radio: 192.168.1.30
  - Walking Robot Radio: 192.168.1.40
 
  - New Radio (UNKNOWN): 192.168.1.15 
  
  - Boat (Otter) laptop/ VCS: 192.168.1.58
  - Arial Vehicle NUC: 192.168.1.200
  - Robot Team Viz: 192.168.1.100
  - Camera NUC: 192.168.1.24
  
  - Otter C1+: 192.168.1.220 
  - Arial Vehicle C1+: 192.168.1.221
  - Walking Robot: 192.168.1.222
  - Drone Jetson: 192.168.1.223
  
  
