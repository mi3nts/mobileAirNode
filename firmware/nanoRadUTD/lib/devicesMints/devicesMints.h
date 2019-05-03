#ifndef DEVICES_MINTS_H
#define DEVICES_MINTS_H
//
#include <Arduino.h>
#include "jobsMints.h"



// For HTU21D
extern uint8_t PPD42NSPinMid;
extern uint8_t PPD42NSPinPM10;
bool initializePPD42NSDuoMints();
void readPPD42NSDuoMints(uint8_t sampleTimeSeconds);

#endif
