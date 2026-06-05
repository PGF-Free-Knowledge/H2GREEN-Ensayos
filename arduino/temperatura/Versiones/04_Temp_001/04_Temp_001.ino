// ===============================
// ESCLAVO TEMPERATURA
// ===============================
//Código funciona con MAX6675

#include "max6675.h"

int thermoDO = 12;
int thermoCS = 10;
int thermoCLK = 13;

MAX6675 thermocouple(thermoCLK, thermoCS, thermoDO);

float filtro = 0;

void setup()
{

Serial.begin(9600);

delay(500);

Serial.println("Esclavo temperatura listo");

}

void loop()
{

if(Serial.available())
{

String cmd = Serial.readStringUntil('\n');
cmd.trim();

if(cmd=="READ")
{

float temperatura = thermocouple.readCelsius();

// filtro digital
filtro = filtro*0.85 + temperatura*0.15;

Serial.println(filtro,2);

}

}

}