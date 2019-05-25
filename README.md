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
