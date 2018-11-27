int serIn; //var that will hold the bytes in read from the serialBuffer


void setup() {
  Serial.begin(9600);
}

void loop() {
  // Format for python
  Serial.println(String(random(0, 255)) + ":" + String(random(0, 255)));


  delay(1000);
}
