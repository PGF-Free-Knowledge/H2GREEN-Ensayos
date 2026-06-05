#include <SoftwareSerial.h>
#include "max6675.h"

// Comunicacion
SoftwareSerial link(2,3);

// MAX6675
int thermoDO = 12;
int thermoCS = 10;
int thermoCLK = 13;

MAX6675 thermocouple(thermoCLK, thermoCS, thermoDO);

float filtro = 0;
float temperatura = 0;

unsigned long lastRead = 0;

void setup()
{
  link.begin(9600);
  delay(500);
}

void loop()
{
  // MAX6675 necesita al menos 250 ms
  if (millis() - lastRead > 300)
  {
    lastRead = millis();

    temperatura = thermocouple.readCelsius();

    if (!isnan(temperatura))
    {
      filtro = filtro * 0.85 + temperatura * 0.15;
    }
  }

  if (link.available())
  {
    String cmd = link.readStringUntil('\n');
    cmd.trim();

    if (cmd == "READ")
    {
      link.println(filtro,2);
    }
  }
}