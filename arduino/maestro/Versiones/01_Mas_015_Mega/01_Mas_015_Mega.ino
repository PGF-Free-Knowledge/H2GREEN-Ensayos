#include <Arduino.h>

// =============================

float fuerza = 0;
float presion = 0;
float temperatura = 25;
float desplazamiento = 0;

float velocidad = 0;

unsigned long t0;

// =============================

void setup()
{

Serial.begin(9600);     // PC

Serial1.begin(9600);    // PRESION
Serial2.begin(9600);    // FUERZA
Serial3.begin(9600);    // STEPPER o TEMP

delay(2000);

t0 = millis();

Serial.println("MAESTRO MEGA LISTO");

}

// =============================

void loop()
{

leerComandoPC();

leerPresion();
leerFuerza();

enviarPC();

delay(20);

}

// =============================

void leerComandoPC()
{

if(Serial.available())
{

String cmd = Serial.readStringUntil('\n');
cmd.trim();

if(cmd.startsWith("VEL="))
{

velocidad = cmd.substring(4).toFloat();

Serial3.print("VEL=");
Serial3.println(velocidad);

}

}

}

// =============================
// PRESION (Serial1)
// =============================

void leerPresion()
{

Serial1.println("READ");

unsigned long t = millis();

while(!Serial1.available())
{
if(millis()-t > 50) return;
}

String val = Serial1.readStringUntil('\n');
presion = val.toFloat();

}

// =============================
// FUERZA (Serial2)
// =============================

void leerFuerza()
{

Serial2.println("READ");

unsigned long t = millis();

while(!Serial2.available())
{
if(millis()-t > 50) return;
}

String val = Serial2.readStringUntil('\n');
fuerza = val.toFloat();

}

// =============================

void enviarPC()
{

float tiempo = (millis()-t0)/1000.0;

Serial.print("t=");
Serial.print(tiempo,3);

Serial.print(";P=");
Serial.print(presion,3);

Serial.print(";F=");
Serial.print(fuerza,5);

Serial.print(";D=");
Serial.print(desplazamiento,3);

Serial.print(";T=");
Serial.println(temperatura,2);

}