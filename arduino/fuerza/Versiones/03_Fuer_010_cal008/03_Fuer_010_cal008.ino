#include <SoftwareSerial.h>
#include "HX711.h"

// =============================
// COMUNICACION CON MAESTRO
// =============================

SoftwareSerial link(3,2);   // RX, TX hacia maestro

// =============================
// HX711
// =============================

#define DT 7
#define SCK 6

HX711 scale;

// =============================
// CALIBRACION
// =============================

long offset = 11682;//10500
float factor = 150.0;//152

// =============================

float fuerza_N = 0;
float fuerza_kN = 0;

// =============================

void setup() {

  Serial.begin(9600);
  link.begin(9600);

  scale.begin(DT,SCK);

  Serial.println("Esclavo fuerza listo");
}

// =============================

void loop() {

  if (link.available()) {

    String cmd = link.readStringUntil('\n');
    cmd.trim();

    if (cmd == "READ") {

      long lectura = scale.read_average(20);

      fuerza_N = (lectura - offset) / factor;
      fuerza_kN = fuerza_N / 1000.0;

      // enviar SOLO numero
      link.println(fuerza_kN,5);

      // debug opcional
      Serial.print("Fuerza kN: ");
      Serial.println(fuerza_kN,5);
    }
  }
}