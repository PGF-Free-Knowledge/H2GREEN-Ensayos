#include <SoftwareSerial.h>
#include "HX711.h"

SoftwareSerial link(3,2);   // RX,TX hacia maestro

#define DT 7
#define SCK 6

HX711 scale;

long offset = 11682;//10500
float factor = 150.0;//152

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

long lectura = scale.read();

float fuerza_N = (lectura - offset)/factor;
float fuerza_kN = fuerza_N/1000.0;

// envio SOLO el numero al maestro
link.println(fuerza_kN);

// debug monitor
Serial.print("Fuerza kN: ");
Serial.println(fuerza_kN,5);

}

}

}