#include <Arduino.h>

unsigned long t0;

// ============================

void setup()
{
  Serial.begin(9600);     // PC

  Serial1.begin(9600);    // PRESION
  Serial2.begin(9600);    // FUERZA
  Serial3.begin(9600);    // STEPPER

  delay(2000);

  t0 = millis();

  Serial.println("MAESTRO MEGA LISTO");
}

// ============================

float P = 0;
float F = 0;
float T = 25;   // sin sensor aún
float D = 0;

// ============================

void loop()
{
  float t = (millis() - t0) / 1000.0;

  // =========================
  // PEDIR DATOS
  // =========================

  Serial1.println("READ");   // presión
  Serial2.println("READ");   // fuerza

  delay(50);

  // =========================
  // LEER PRESION
  // =========================

  if (Serial1.available())
  {
    P = Serial1.readStringUntil('\n').toFloat();
  }

  // =========================
  // LEER FUERZA
  // =========================

  if (Serial2.available())
  {
    F = Serial2.readStringUntil('\n').toFloat();
  }

  // =========================
  // COMANDOS DESDE PC
  // =========================

  if (Serial.available())
  {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    // reenviar al stepper
    if (cmd.startsWith("VEL="))
    {
      Serial3.println(cmd);
    }
  }

  // =========================
  // ENVIO A PC
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

  delay(200);
}
