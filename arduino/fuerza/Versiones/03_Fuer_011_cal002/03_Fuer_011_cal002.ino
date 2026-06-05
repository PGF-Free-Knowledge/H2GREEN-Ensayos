#include "HX711.h"

#define DT 7
#define SCK 6

HX711 scale;

long offset = 15225;//15479-12939
float factor = 1276.00;//1370-1498.00

void setup() {

Serial.begin(9600);

scale.begin(DT,SCK);

delay(2000);

}

void loop() {

if(Serial.available())
{

String cmd = Serial.readStringUntil('\n');
cmd.trim();

if(cmd=="READ")
{

long lectura = scale.read_average(10);

float peso_kg = (lectura - offset) / factor;

float fuerza_N = peso_kg * 9.81;

float fuerza_kN = fuerza_N / 1000.0;

Serial.println(fuerza_kN,5);

}

}

}