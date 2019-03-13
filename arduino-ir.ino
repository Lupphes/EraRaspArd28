#include <Arduino.h>

// Defining pin assesment
#define heatingPWMM 11 // Heating system pin

int floortemps = 2;// Floor temp sensor
int roomtemps = 3;// Room temp sensor

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
  pinMode(floortemps, INPUT); // Floor temperature sensor set as input
  pinMode(heatingPWMM, OUTPUT); // Heating system pin set as output
}

void loop() {
  // All of the functions are declared below
  heating();
  delay(500);
}

void heating() { 
  // Room temperature check  
  float roomtemp = (analogRead(roomtemps)/1024.0)*500; // Reading and converting sensor value to Celsius
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
  floortemp = (analogRead(floortemps)*500)/1023; // Reading and converting sensor value to Celsius
  Serial.print("\nfloor ");
  Serial.print(floortemp); 
  if (floortemp > 45) { // If floor heating temperature exceeds defined temperature heating turns off
    analogWrite(heatingPWMM, 0);
  }
}