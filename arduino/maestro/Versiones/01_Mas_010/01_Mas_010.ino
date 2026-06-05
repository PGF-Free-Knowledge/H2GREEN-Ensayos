#include <SoftwareSerial.h>

SoftwareSerial slaveP(2,3);
SoftwareSerial slaveF(4,5);
SoftwareSerial slaveT(6,7);
SoftwareSerial slaveStepper(8,9);

float P=0;
float F=0;
float T=0;
float D=0;

float SP_P=0;
float VEL=0;

unsigned long t0;

void setup()
{

Serial.begin(9600);

slaveP.begin(9600);
slaveF.begin(9600);
slaveT.begin(9600);
slaveStepper.begin(9600);

Serial.println("Maestro listo");

t0 = millis();

}

void loop()
{

// =================
// COMANDOS PYTHON
// =================

if(Serial.available())
{

String cmd = Serial.readStringUntil('\n');
cmd.trim();

if(cmd.startsWith("VEL="))
VEL = cmd.substring(4).toFloat();

if(cmd.startsWith("SP_P="))
SP_P = cmd.substring(5).toFloat();

}

// =================
// STEPPER
// =================

slaveStepper.listen();
slaveStepper.print("VEL=");
slaveStepper.println(VEL);

// =================
// PRESION
// =================

slaveP.listen();

slaveP.print("SP_P=");
slaveP.println(SP_P);

delay(10);

slaveP.println("READ");

delay(40);

if(slaveP.available())
P = slaveP.readStringUntil('\n').toFloat();

// =================
// FUERZA
// =================

slaveF.listen();

slaveF.println("READ");

delay(40);

if(slaveF.available())
F = slaveF.readStringUntil('\n').toFloat();

// =================
// TEMPERATURA
// =================

slaveT.listen();

slaveT.println("READ");

delay(40);

if(slaveT.available())
T = slaveT.readStringUntil('\n').toFloat();

// =================
// ENVIO PC
// =================

float tiempo = (millis()-t0)/1000.0;

Serial.print("t=");
Serial.print(tiempo);

Serial.print(";P=");
Serial.print(P,4);

Serial.print(";F=");
Serial.print(F,5);

Serial.print(";D=");
Serial.print(D,3);

Serial.print(";T=");
Serial.println(T,2);

delay(80);

}