// ===============================
// ESCLAVO TEMPERATURA
// ===============================

#include <SoftwareSerial.h>
#include "max6675.h"

// ===============================
// COMUNICACION CON MAESTRO
// ===============================
// RX = 2
// TX = 3

SoftwareSerial link(2, 3);

// ===============================
// MAX6675
// ===============================

int thermoDO = 12;
int thermoCS = 10;
int thermoCLK = 13;

MAX6675 thermocouple(thermoCLK, thermoCS, thermoDO);

// ===============================
// VARIABLES
// ===============================

float temperatura = 0;
float filtro = 0;

unsigned long lastRead = 0;

// ===============================
// SETUP
// ===============================

void setup()
{
  link.begin(9600);
  delay(500);
}

// ===============================
// LOOP
// ===============================

void loop()
{
  // ===============================
  // LECTURA CONTINUA
  // ===============================

  if (millis() - lastRead > 200)
  {
    lastRead = millis();

    temperatura = thermocouple.readCelsius();

    // Evitar NaN
    if (!isnan(temperatura))
    {
      // Filtro digital
      filtro = filtro * 0.85 + temperatura * 0.15;
    }
  }

  // ===============================
  // COMUNICACION CON MAESTRO
  // ===============================

  if (link.available())
  {
    String cmd = link.readStringUntil('\n');
    cmd.trim();

    if (cmd == "READ")
    {
      link.println(filtro, 2);
    }
  }
}