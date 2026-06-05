#include <SoftwareSerial.h>

// Stepper usa SoftwareSerial
SoftwareSerial stepper(10,11);

// Variables
float P=0;
float F=0;
float T=0;
float D=0;

float SP_P=0;
float VEL=0;

unsigned long t0;

void setup()
{

Serial.begin(9600);    // PC

Serial1.begin(9600);   // Presión
Serial2.begin(9600);   // Fuerza
Serial3.begin(9600);   // Temperatura

stepper.begin(9600);

Serial.println("MAESTRO MEGA LISTO");

t0=millis();

}

void loop()
{

// =======================
// COMANDOS DESDE PYTHON
// =======================

if(Serial.available())
{

String cmd=Serial.readStringUntil('\n');
cmd.trim();

if(cmd.startsWith("VEL="))
VEL=cmd.substring(4).toFloat();

if(cmd.startsWith("SP_P="))
SP_P=cmd.substring(5).toFloat();

}

// =======================
// STEPPER
// =======================

stepper.print("VEL=");
stepper.println(VEL);

// =======================
// PRESION
// =======================

Serial1.print("SP_P=");
Serial1.println(SP_P);

delay(5);

Serial1.println("READ");

delay(20);

if(Serial1.available())
{

String dato=Serial1.readStringUntil('\n');
dato.trim();

if(dato.length()>0)
P=dato.toFloat();

}

// =======================
// FUERZA
// =======================

Serial2.println("READ");

delay(20);

if(Serial2.available())
{

String dato=Serial2.readStringUntil('\n');
dato.trim();

if(dato.length()>0)
F=dato.toFloat();

}

// =======================
// TEMPERATURA
// =======================

Serial3.println("READ");

delay(20);

if(Serial3.available())
{

String dato=Serial3.readStringUntil('\n');
dato.trim();

if(dato.length()>0)
T=dato.toFloat();

}

// =======================
// ENVIO AL DASHBOARD
// =======================

float tiempo=(millis()-t0)/1000.0;

Serial.print("t=");
Serial.print(tiempo,2);

Serial.print(";P=");
Serial.print(P,3);

Serial.print(";F=");
Serial.print(F,5);

Serial.print(";D=");
Serial.print(D,3);

Serial.print(";T=");
Serial.println(T,2);

delay(60);

}
