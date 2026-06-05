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
float factor = 150;//152

// =============================
// VARIABLES
// =============================

float fuerza_N = 0;
float fuerza_kN = 0;

// =============================
// SETUP
// =============================

void setup() {

  Serial.begin(9600);      // solo para diagnóstico
  link.begin(9600);        // comunicación con maestro

  scale.begin(DT,SCK);

  Serial.println("Esclavo fuerza HX711 iniciado");
}

// =============================
// LOOP
// =============================

void loop() {

  // Promedio para estabilidad
  long lectura = scale.read_average(20);

  // Calculo de fuerza
  fuerza_N = (lectura - offset) / factor;

  // Convertir a kN
  fuerza_kN = fuerza_N / 1000.0;

  // =============================
  // ENVIO AL MAESTRO
  // =============================

  link.print("F=");
  link.println(fuerza_kN,5);

  // =============================
  // MONITOR SERIAL (opcional)
  // =============================

  Serial.print("Lectura: ");
  Serial.print(lectura);

  Serial.print(" | Fuerza N: ");
  Serial.print(fuerza_N,3);

  Serial.print(" | Fuerza kN: ");
  Serial.println(fuerza_kN,5);

  delay(100);
}