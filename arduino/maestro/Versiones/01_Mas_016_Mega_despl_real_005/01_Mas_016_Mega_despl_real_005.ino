#include <Arduino.h>
#include <SoftwareSerial.h>

// ============================
// TEMPERATURA (NUEVO)
// ============================
SoftwareSerial tempSerial(10, 11); // RX, TX

// ============================
// VARIABLES
// ============================

unsigned long t0;

float P = 0;
float F = 0;
float D = 0;
float T = 25;

// ============================

void setup()
{
  Serial.begin(9600);     // PC

  Serial1.begin(9600);    // PRESION
  Serial2.begin(9600);    // FUERZA
  Serial3.begin(9600);    // STEPPER

  tempSerial.begin(9600); // 🔥 SOLO AÑADIDO

  delay(2000);

  t0 = millis();

  Serial.println("MAESTRO MEGA FINAL ESTABLE + TEMP");
}

// ============================

void loop()
{
  float t = (millis() - t0) / 1000.0;

  // =========================
  // PEDIR DATOS
  // =========================

  Serial1.println("READ");
  Serial2.println("READ");
  tempSerial.println("READ");   // 🔥 NUEVO

  delay(20);

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
  // TEMPERATURA (NUEVO)
  // =========================

  if (tempSerial.available())
  {
    String data = tempSerial.readStringUntil('\n');
    data.trim();
    T = data.toFloat();
  }

  // =========================
  // STEPPER
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
  // COMANDOS PC
  // =========================

  if (Serial.available())
  {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd.startsWith("VEL=") || cmd == "ZERO")
    {
      Serial3.println(cmd);
    }
  }

  // =========================
  // ENVIO FINAL
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

