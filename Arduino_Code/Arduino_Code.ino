#include <NinjaIoT.h>

NinjaIoT iot;

void setup() {
  Serial.begin(115200);
  iot.connect("MSB_2G", "9900015169", "NB09");   //link: https://iot.roboninja.in/
}

void loop() {
  iot.ReadAll();
  iot.SyncOut("D1");
  delay(50);  // wait 50 milliseconds
}