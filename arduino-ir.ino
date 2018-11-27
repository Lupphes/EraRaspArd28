#include <pRNG.h>
pRNG prng;
int serIn; //var that will hold the bytes in read from the serialBuffer

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
}

void loop() {
  // Format for python
  while (true) {
    Serial.println(String(prng.getRndByte()) + ":" + String(prng.getRndByte()));
    delay(1000);
  }

}
