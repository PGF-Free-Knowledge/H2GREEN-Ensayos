#include <Arduino.h>

// ============================
// VARIABLES
// ============================

unsigned long t0;

float P = 0;
float F = 0;
float D = 0;
float T = 25;   // sin sensor aún

// ============================

void setup()
{
  Serial.begin(9600);     // PC

  Serial1.begin(9600);    // PRESION
  Serial2.begin(9600);    // FUERZA
  Serial3.begin(9600);    // STEPPER

  delay(2000);

  t0 = millis();

  Serial.println("MAESTRO MEGA CON DESPLAZAMIENTO LISTO");
}

// ============================

void loop()
{
  float t = (millis() - t0) / 1000.0;

  // =========================
  // PEDIR DATOS A ESCLAVOS
  // =========================

  Serial1.println("READ");   // presión
  Serial2.println("READ");   // fuerza

  delay(20);

  // =========================
  // LEER PRESION
  // =========================

  if (Serial1.available())
  {
    String data = Serial1.readStringUntil('\n');
    data.trim();
    P = data.toFloat();
  }

  // =========================
  // LEER FUERZA
  // =========================

  if (Serial2.available())
  {
    String data = Serial2.readStringUntil('\n');
    data.trim();
    F = data.toFloat();
  }

  // =========================
  // LEER STEPPER (POSICION)
  // =========================

  while (Serial3.available())
  {
    String msg = Serial3.readStringUntil('\n');
    msg.trim();

    if (msg.startsWith("POS="))
    {
      D = msg.substring(4).toFloat();
    }
  }

  // =========================
  // COMANDOS DESDE PC
  // =========================

  if (Serial.available())
  {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    // reenviar comandos al stepper
    if (cmd.startsWith("VEL=") || cmd == "ZERO")
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

  delay(100);
}