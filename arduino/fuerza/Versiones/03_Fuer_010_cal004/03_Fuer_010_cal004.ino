#include <SoftwareSerial.h>
#include "HX711.h"

SoftwareSerial link(3,2);

#define DT 7
#define SCK 6

HX711 scale;

long offset = 11321;
float factor = 58.0;

void setup() {

  Serial.begin(9600);
  link.begin(9600);

  scale.begin(DT,SCK);
}

void loop() {

  long lectura = scale.read();

  float fuerza_N = (lectura - offset) / factor;

  float fuerza_kN = fuerza_N / 1000.0;

  link.print("F=");
  link.println(fuerza_kN);

  delay(50);

}