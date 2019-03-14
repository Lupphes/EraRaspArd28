// Defining pin assesment
#define heatingPWMM 11 // Heating system pin
#define wateringPWMM 12 // Watering system pin
#define lightsensorpin A0 // Light sensor pin

int floorsensorpin = 2;// Floor temp sensor
int roomsensorpin = 3;// Room temp sensor
int humiditysensorpin = 4; // Humidity sensor
int waterpumppin = 5; // Water pump

// Declaring other variables
float floortemp; // Variable to store floor temperature in degree Celsius 
float roomtemp; // Variable to store room temperature in degree Celsius 
int reqtemp = 30; // Requested temperature

// Communication variables
char operation; // Holds operation (R, W, ...)
char mode; // Holds the mode (D, A)
int pin_number; // Holds the pin number
int digital_value; // Holds the digital value
int analog_value; // Holds the analog value
int value_to_write; // Holds the value that we want to write
int wait_for_transmission = 5; // Delay in ms in order to receive the serial data

void setup() {
  Serial.begin(9600); // Initiating communicationg over serial, speed 9600 baud
  Serial.setTimeout(100); // Instead of the default 1000ms, in order
                            // to speed up the Serial.parseInt()
  randomSeed(444);
  pinMode(16, OUTPUT);
  pinMode(floorsensorpin, INPUT); // Floor temperature sensor set as input
  pinMode(heatingPWMM, OUTPUT); // Heating system pin set as output
}

void loop() {
  // All of the functions are declared below
  heating();
  watering();
  lights();
  delay(500);

  // Check if characters available in the buffer
  if (Serial.available() > 0) {
      operation = Serial.read();
      delay(wait_for_transmission); // If not delayed, second character is not correctly read
      mode = Serial.read();
      pin_number = Serial.parseInt(); // Waits for an int to be transmitted
      if (Serial.read()==':'){
          value_to_write = Serial.parseInt(); // Collects the value to be written
      }
      switch (operation){
          case 'R': // Read operation, e.g. RD12, RA4
              if (mode == 'D'){ // Digital read
                  digital_read(pin_number);
              } else if (mode == 'A'){ // Analog read
                  analog_read(pin_number);
              } else {
                break; // Unexpected mode
              }
              break;

          case 'W': // Write operation, e.g. WD3:1, WA8:255
              if (mode == 'D'){ // Digital write
                  digital_write(pin_number, value_to_write);
              } else if (mode == 'A'){ // Analog write
                  analog_write(pin_number, value_to_write);
              } else {
                  break; // Unexpected mode
              }
              break;

          case 'M': // Pin mode, e.g. MI3, MO3, MP3
              set_pin_mode(pin_number, mode); // Mode contains I, O or P (INPUT, OUTPUT or PULLUP_INPUT)
              break;

          default: // Unexpected char
              break;
      }
  }   

}

void heating() { 
  // Room temperature check  
  float roomtemp = (analogRead(roomsensorpin)/1024.0)*500; // Reading and converting sensor value to Celsius
  Serial.print("\nrequested: ");
  Serial.print(reqtemp);
  Serial.print("\nactual: ");
  Serial.print(roomtemp);
  if (reqtemp > roomtemp) { 
    analogWrite(heatingPWMM, 120); // If the requested temperature is not achieved the heating turns on
  } else
  {
    analogWrite(heatingPWMM, 0); // If the requested temperature is higher the heating turns off
  }

  // Floor heating temperature check
  floortemp = (analogRead(floorsensorpin)*500)/1023; // Reading and converting sensor value to Celsius
  Serial.print("\nfloor ");
  Serial.print(floortemp); 
  if (floortemp > 45) { // If floor heating temperature exceeds defined temperature heating turns off
    analogWrite(heatingPWMM, 0);
  }
}

void watering(){ // Program that controls watering system
  //float humidity = random(0, 1000); // Reading raw values from sensor
  float humidity = analogRead(humiditysensorpin); // Reading raw values from sensor
  if (humidity < 30) {
      digital_write(waterpumppin, HIGH);// Watering on
  } else
  {
      digital_write(waterpumppin, LOW);// Watering off
  }    
}

void lights(){ // Program that controls lights inside of the house based on the outside light
  //float outside_light = random(o, 1000); // Reading and converting raw values to percentage
  float outside_light = map(analogRead(lightsensorpin), 0, 1023, 0, 100); // Reading and converting raw values to percentage
  if (outside_light <= 30) { // If the percentage of light falls below 30 percent the lights will turn on
          digitalWrite(13, HIGH); // Lights on
  } else
  {
          digitalWrite(13, LOW); // Lights off
  }
}