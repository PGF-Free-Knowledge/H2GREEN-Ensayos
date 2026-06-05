#include "HX711.h"

#define DT 7
#define SCK 6

HX711 scale;

/* CALIBRACION */
long offset = 10500;
float factor = 152.0;

void setup() {

  Serial.begin(9600);

  scale.begin(DT,SCK);

  Serial.println("Sistema medicion fuerza");
  Serial.println("----------------------");

}

void loop() {

  long lectura = scale.read_average(20);

  float fuerza_N = (lectura - offset) / factor;

  float fuerza_kN = fuerza_N / 1000.0;

  Serial.print("Lectura HX711: ");
  Serial.print(lectura);

  Serial.print(" | Fuerza (N): ");
  Serial.print(fuerza_N,3);

  Serial.print(" | Fuerza (kN): ");
  Serial.println(fuerza_kN,5);

  delay(500);

}