#include <SoftwareSerial.h>
#include "max6675.h"

// ============================
// COMUNICACION
// ============================

SoftwareSerial link(3, 2); // RX, TX

// ============================
// MAX6675 PINES (CORREGIDOS)
// ============================

int pinSO = 4;   // Cambiado de SO a pinSO
int pinCS = 5;   // Cambiado de CS a pinCS
int pinSCK = 6;  // Cambiado de SCK a pinSCK

// Se pasan los nuevos nombres al objeto del sensor
MAX6675 termocouple(pinSCK, pinCS, pinSO);

// ============================

void setup() {

  Serial.begin(9600);
  link.begin(9600);

  Serial.println("Esclavo temperatura MAX6675 listo");

  delay(500); // estabilización
}

// ============================

void loop() {

  if (link.available()) {

    String cmd = link.readStringUntil('\n');
    cmd.trim();

    if (cmd == "READ") {

      float temp = termocouple.readCelsius();

      link.println(temp);

      // debug
      Serial.print("Temp: ");
      Serial.println(temp);
    }
  }
}