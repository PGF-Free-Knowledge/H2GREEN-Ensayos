#include <Arduino.h>
#include <SoftwareSerial.h>

// ============================
// SERIAL TEMPERATURA
// ============================

SoftwareSerial SerialTemp(10,11);

// ============================
// VARIABLES
// ============================

unsigned long t0;

float P = 0;
float F = 0;
float D = 0;
float T = 25;

// Fuerza máxima
float Fmax = 0;

// Detección rotura
bool roturaDetectada = false;

// ============================

void setup()
{
  Serial.begin(9600);

  Serial1.begin(9600);
  Serial2.begin(9600);
  Serial3.begin(9600);

  SerialTemp.begin(9600);

  delay(2000);

  t0 = millis();

  Serial.println("MAESTRO MEGA LISTO");
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
  SerialTemp.println("READ");

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
  // GUARDAR FUERZA MAXIMA
  // =========================

  if(F > Fmax)
  {
    Fmax = F;
  }

  // =========================
  // DETECCION ROTURA
  // =========================

  float UMBRAL_ROTURA = 0.6;

  if(Fmax > 0.1 && !roturaDetectada)
  {
    if(F < Fmax * UMBRAL_ROTURA)
    {
      roturaDetectada = true;

      Serial3.println("VEL=0");

      Serial.println("ROTURA DETECTADA");
    }
  }

  // =========================
  // TEMPERATURA
  // =========================

  if (SerialTemp.available())
  {
    String data = SerialTemp.readStringUntil('\n');
    data.trim();

    if(data.length()>0)
    {
      T = data.toFloat();
    }
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