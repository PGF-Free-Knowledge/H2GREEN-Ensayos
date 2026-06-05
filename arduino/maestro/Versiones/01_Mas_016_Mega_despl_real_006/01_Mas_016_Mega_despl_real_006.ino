#include <Arduino.h>
#include <SoftwareSerial.h>

// ============================
// SERIAL TEMPERATURA
// ============================

SoftwareSerial SerialTemp(10,11); // RX, TX

// ============================
// VARIABLES
// ============================

unsigned long t0;

float P = 0;
float F = 0;
float D = 0;
float T = 25;

unsigned long lastTemp = 0;

// ============================

void setup()
{
  Serial.begin(9600);     // PC

  Serial1.begin(9600);    // PRESION
  Serial2.begin(9600);    // FUERZA
  Serial3.begin(9600);    // STEPPER

  SerialTemp.begin(9600); // TEMPERATURA

  delay(2000);

  t0 = millis();

  Serial.println("MAESTRO MEGA CON TEMPERATURA LISTO");
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

  // temperatura cada 500 ms
  if(millis() - lastTemp > 500)
  {
    SerialTemp.println("READ");
    lastTemp = millis();
  }

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
  // LEER TEMPERATURA
  // =========================

  if (SerialTemp.available())
  {
    String data = SerialTemp.readStringUntil('\n');
    data.trim();
    T = data.toFloat();
  }

  // =========================
  // LEER STEPPER
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