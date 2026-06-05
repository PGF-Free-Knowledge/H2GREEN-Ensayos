#include "HX711.h"

#define DT 7
#define SCK 6

HX711 scale;

void setup() {

  Serial.begin(9600);
  scale.begin(DT, SCK);

  Serial.println("Tare...");
  scale.tare();   // elimina offset

}

void loop() {

  float lectura = scale.get_units(20);  // promedio de 20 muestras

  Serial.println(lectura);

  delay(200);

}