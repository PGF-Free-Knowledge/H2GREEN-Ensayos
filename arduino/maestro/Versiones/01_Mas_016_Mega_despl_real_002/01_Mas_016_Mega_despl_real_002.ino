#include <Arduino.h>

// ============================
// VARIABLES
// ============================

unsigned long t0;

float P = 0;
float F = 0;
float D = 0;
float T = 0;

// ============================

void setup()
{
  Serial.begin(9600);     // PC

  Serial1.begin(9600);    // PRESION
  Serial2.begin(9600);    // FUERZA
  Serial3.begin(9600);    // TEMPERATURA

  delay(2000);

  t0 = millis();

  Serial.println("MAESTRO MEGA COMPLETO OK");
}

// ============================

void loop()
{
  float t = (millis() - t0) / 1000.0;

  // =========================
  // PEDIR DATOS
  // =========================

  Serial1.println("READ");   // presión
  Serial2.println("READ");   // fuerza
  Serial3.println("READ");   // temperatura

  delay(50);

  // =========================
  // PRESION
  // =========================

  if (Serial1.available())
  {
    String data = Serial1.readStringUntil('\n');
    data.trim();
    P = data.toFloat();
  }

  // =========================
  // FUERZA
  // =========================

  if (Serial2.available())
  {
    String data = Serial2.readStringUntil('\n');
    data.trim();
    F = data.toFloat();
  }

  // =========================
  // TEMPERATURA
  // =========================

  if (Serial3.available())
  {
    String data = Serial3.readStringUntil('\n');
    data.trim();
    T = data.toFloat();
  }

  // =========================
  // COMANDOS DESDE PYTHON (Stepper)
  // =========================

  if (Serial.available())
  {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    // 👉 Enviar al Arduino del stepper (por Serial USB separado o ajustar luego)
    // TEMPORAL: solo debug
    Serial.print("CMD: ");
    Serial.println(cmd);
  }

  // =========================
  // ENVIO A PYTHON
  // =========================

  Serial.print("t=");
  Serial.print(t,3);

  Serial.print(";P=");
  Serial.print(P,3);

  Serial.print(";F=");
  Serial.print(F,5);

  Serial.print(";D=");
  Serial.print(D,3);

  Serial.print(";T=");
  Serial.println(T,2);

  delay(100);
}