#include <pRNG.h>
pRNG prng;
int serIn; //var that will hold the bytes in read from the serialBuffer

void setup() {
  Serial.begin(9600);
}

void loop() {
  // Format for python
  Serial.println(String(prng.getRndByte()) + ":" + String(prng.getRndByte()));
  delay(1000);
}
