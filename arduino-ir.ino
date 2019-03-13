#include <Arduino.h>

//Defining pin assesment
#define heatingPWMM 11 //Heating system pin

int floortemps = 2;//Floor temp sensor
int roomtemps = 3;//Room temp sensor

//Declaring other variables
int floorval; //temporary variable to hold floor temperature value
int roomval; //temporary variable to hold room temperature value
float vout; //temporary variable to hold sensor reading 
float tempc; //variable to store temperature in degree Celsius 
int reqtemp = 30; //requested temperature

void setup() {
  //Humidity sensor setup
  Serial.begin(9600); //Initiating communicationg over serial, speed 9600 baud
  pinMode(floortemps, INPUT); //Floor temperature sensor set as input
  pinMode(heatingPWMM, OUTPUT); //Heating system pin set as output
}

void loop() {
  //All of the functions are declared below
  heating();
  delay(500);
}

void heating() { 
  roomval = analogRead(floortemps);
  float mv = ( roomval/1024.0)*5000;
  float cel = mv/10;
  Serial.print("\nrequested: ");
  Serial.print(reqtemp);
  Serial.print("\nactual: ");
  Serial.print(cel);
  if (reqtemp > cel) {
    analogWrite(heatingPWMM, 220);
  } else
  {
    analogWrite(heatingPWMM, 0);
  }
  vout=analogRead(roomtemps); //Reading the value from sensor
  vout=(vout*500)/1023;  
  Serial.print("\nfloor ");
  Serial.print(vout); 
  if (vout > 45) {
    analogWrite(10, 0);
  }
}