
#include "devicesMints.h"

// BME280  ---------------------------------------
//
bool initializeBME280Mints(){
      if (bme280.init()) {
        Serial.println("BME280 Initiated");
        delay(1);
        return true;
      }
      else
      {
      Serial.println("BME280 not found");
      delay(1);

      return false;
      }

}

void readBME280Mints(){

  float temperature    = bme280.getTemperature();
  float pressure       = bme280.getPressure();
  float humidity       = bme280.getHumidity();
  float altitude       = bme280.calcAltitude(pressure);

  String readings[4] = { String(temperature,2) , String(pressure,2), String(humidity,2) , String(altitude,2) };
  sensorPrintMints("BME280",readings,4);
}

//
//
// // // MGS001  ---------------------------------------

bool initializeMGS001Mints(){

  gas.begin(0x04);//the default I2C address of the slave is 0x04
  gas.powerOn();
  Serial.println("MGS001 Initiated");
  Serial.print("MGS001 Firmware Version = ");
  Serial.println(gas.getVersion());
  delay(1);

return true;
}

void readMGS001Mints(){

  float nh3     = gas.measure_NH3();
  float co      = gas.measure_CO();
  float no2     = gas.measure_NO2();
  float c3h8    = gas.measure_C3H8();
  float c4h10   = gas.measure_C4H10();
  float ch4     = gas.measure_CH4();
  float h2      = gas.measure_H2();
  float c2h5oh  = gas.measure_C2H5OH();


  String readings[8] = { String(nh3,2) , String(co,2), String(no2,2) , String(c3h8,2), String(c4h10,2) , String(ch4,2), String(h2,2) , String(c2h5oh,2) };
  sensorPrintMints("MGS001",readings,8);
}


//
//
// // SCD30 ---------------------------------------
// bool initializeSCD30Mints(){
//   if (scd.begin()) {
//     Serial.println("SCD30 Initiated");
//     delay(1);
//     return true;
//   }else{
//     Serial.println("SCD30 not found");
//     delay(1);
//     return false;
//   }
//
//   delay(2000);
// }
//
// void readSCD30Mints(){
//
//   uint16_t co2         = scd.getCO2();
//   uint16_t temperature = scd.getTemperature();
//   uint16_t humidity    = scd.getHumidity();
//
//   String readings[3] = { String(co2), String(temperature) , String(humidity) };
//   sensorPrintMints("SCD30",readings,3);
//
// }

//
// // INA219  ---------------------------------------
//
// bool initializeINA219Mints(){
//     ina.begin();
//     Serial.println("INA219 Initiated");
//     delay(1);
//     return true;
// }
//
// void readINA219Mints(){
//
//   float shuntVoltage  = ina.getShuntVoltage_mV();
//   float busVoltage    = ina.getBusVoltage_V();
//   float currentMA     = ina.getCurrent_mA();
//   float powerMW      = ina.getPower_mW();
//   float loadVoltage  = busVoltage + (shuntVoltage / 1000);
//
//
//   String readings[5] = { String(shuntVoltage,4) , String(busVoltage,4),  String(currentMA,4) , String(powerMW,4), String(loadVoltage,4)};
//   sensorPrintMints("INA219",readings,5);
//
//
// }

//
//
// // OPCN3  ---------------------------------------

bool initializeOPCN3Mints(){

  return opc.initialize();

}

void readOPCN3Mints(){

  struct histogramData  allData= opc.readHistogramData();

  String readings[43] =  { \
                          String(allData.valid), \
                          String(allData.binCount0), \
                          String(allData.binCount1), \
                          String(allData.binCount2), \
                          String(allData.binCount3), \
                          String(allData.binCount4), \
                          String(allData.binCount5), \
                          String(allData.binCount6), \
                          String(allData.binCount7), \
                          String(allData.binCount8), \
                          String(allData.binCount9), \
                          String(allData.binCount10), \
                          String(allData.binCount11), \
                          String(allData.binCount12), \
                          String(allData.binCount13), \
                          String(allData.binCount14), \
                          String(allData.binCount15), \
                          String(allData.binCount16), \
                          String(allData.binCount17), \
                          String(allData.binCount18), \
                          String(allData.binCount19), \
                          String(allData.binCount20), \
                          String(allData.binCount21), \
                          String(allData.binCount22), \
                          String(allData.binCount23), \
                          String(allData.bin1TimeToCross), \
                          String(allData.bin3TimeToCross), \
                          String(allData.bin5TimeToCross), \
                          String(allData.bin7TimeToCross), \
                          String(allData.samplingPeriod), \
                          String(allData.sampleFlowRate), \
                          String(allData.temperature), \
                          String(allData.humidity), \
                          String(allData.pm1,2), \
                          String(allData.pm2_5,2), \
                          String(allData.pm10,2),\
                          String(allData.rejectCountGlitch), \
                          String(allData.rejectCountLongTOF), \
                          String(allData.rejectCountRatio), \
                          String(allData.rejectCountOutOfRange), \
                          String(allData.fanRevCount), \
                          String(allData.laserStatus), \
                          String(allData.checkSum) \
                        };
  sensorPrintMints("OPCN3",readings,43);
}
