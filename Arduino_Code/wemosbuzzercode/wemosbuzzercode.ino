#include <NinjaIoT.h>
#include <entry.h>

NinjaIoT iot;

void setup() {
  Serial.begin(115200);
  iot.connect("wifi", "pwd", "uid");   //link: https://iot.roboninja.in/
}

void loop() {
  iot.ReadAll();
  iot.SyncOut("D1");
  delay(50);  // wait 50 milliseconds
}
