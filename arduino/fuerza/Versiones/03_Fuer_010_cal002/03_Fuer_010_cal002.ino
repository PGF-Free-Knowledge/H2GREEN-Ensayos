#include "HX711.h"

#define DT 7
#define SCK 6

HX711 scale;

void setup() {

  Serial.begin(9600);

  scale.begin(DT,SCK);

}

void loop() {

  if(scale.is_ready()){

    Serial.println(scale.read());

  } else {

    Serial.println("HX711 no encontrado");

  }

  delay(500);

}