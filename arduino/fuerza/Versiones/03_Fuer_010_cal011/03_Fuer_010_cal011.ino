#include <SoftwareSerial.h>
#include "HX711.h"

SoftwareSerial link(3,2);   // RX,TX

#define DT 7
#define SCK 6

HX711 scale;

long offset = 11682;
float factor = 150.0;

float filtro = 0;

void setup()
{

Serial.begin(9600);
link.begin(9600);

scale.begin(DT,SCK);

Serial.println("Esclavo fuerza listo");

}

void loop()
{

if(link.available())
{

String cmd = link.readStringUntil('\n');
cmd.trim();

if(cmd=="READ")
{

long lectura = scale.read_average(10);

float fuerza_N = (lectura - offset)/factor;
float fuerza_kN = fuerza_N/1000.0;

// filtro digital
filtro = filtro*0.85 + fuerza_kN*0.15;

link.println(filtro);

// debug
Serial.print("Fuerza kN: ");
Serial.println(filtro,5);

}

}

}