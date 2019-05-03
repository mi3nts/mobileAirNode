#include <Arduino.h>
#include "jobsMints.h"
#include "devicesMints.h"


bool PPD42NSOnline;

uint8_t PPD42NSPinMid = 2;
uint8_t PPD42NSPinPM10 = 3;

uint16_t sensingPeriod = 2070;
uint16_t initPeriod = 1500;


void setup() {

  initializeSerialMints();
  delay(1000);
  PPD42NSOnline = initializePPD42NSDuoMints();
  delay(1000);

}

  // the loop routine runs over and over again forever:
void loop() {

    if(PPD42NSOnline)
        {
          readPPD42NSDuoMints(30);
        }

  }
