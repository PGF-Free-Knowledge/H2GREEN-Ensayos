#include "HX711.h"

#define DT 6// 6
#define SCK 7//7

HX711 scale;

void setup() {

  Serial.begin(9600);

  scale.begin(DT, SCK);

  Serial.println("HX711 listo");

}

void loop() {

  long lectura = scale.read();

  Serial.println(lectura);

  delay(500);

}