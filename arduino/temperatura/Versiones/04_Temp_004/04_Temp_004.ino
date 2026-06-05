#include <max6675.h>

// Pines del MAX6675
int pinSO  = 4;   // DO
int pinCS  = 5;
int pinSCK = 6;

MAX6675 termocouple(pinSCK, pinCS, pinSO);

void setup() {

  Serial.begin(9600);

  Serial.println("TEST MAX6675 INICIADO");

  delay(1000);
}

void loop() {

  float temp = termocouple.readCelsius();

  Serial.print("Temperatura: ");
  Serial.print(temp);
  Serial.println(" C");

  delay(1000);
}