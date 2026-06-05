#include <SoftwareSerial.h>

// ===============================
// ESCLAVOS
// ===============================

SoftwareSerial slaveP(2,3);        // Presión
SoftwareSerial slaveF(4,5);        // Fuerza
SoftwareSerial slaveT(6,7);        // Temperatura
SoftwareSerial slaveStepper(8,9);  // Motor

// ===============================
// VARIABLES
// ===============================

float P = 0;
float F = 0;
float T = 0;
float D = 0;

float SP_P = 0;
float VEL = 0;

unsigned long t0;

// ===============================

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

// ===============================

void loop()
{

// ===============================
// RECIBIR COMANDOS DE PYTHON
// ===============================

if (Serial.available())
{

String cmd = Serial.readStringUntil('\n');
cmd.trim();

if (cmd.startsWith("VEL="))
VEL = cmd.substring(4).toFloat();

if (cmd.startsWith("SP_P="))
SP_P = cmd.substring(5).toFloat();

}

// ===============================
// ENVIAR VELOCIDAD AL STEPPER
// ===============================

slaveStepper.listen();

slaveStepper.print("VEL=");
slaveStepper.println(VEL);

// ===============================
// PRESION
// ===============================

slaveP.listen();

slaveP.print("SP_P=");
slaveP.println(SP_P);

delay(5);

slaveP.println("READ");

delay(60);

if (slaveP.available())
{
String dato = slaveP.readStringUntil('\n');
dato.trim();

if (dato.length() > 0)
P = dato.toFloat();
}

// ===============================
// FUERZA
// ===============================

slaveF.listen();

slaveF.println("READ");

delay(60);

if (slaveF.available())
{
String dato = slaveF.readStringUntil('\n');
dato.trim();

if (dato.length() > 0)
F = dato.toFloat();
}

// ===============================
// TEMPERATURA
// ===============================

slaveT.listen();

slaveT.println("READ");

delay(60);

if (slaveT.available())
{
String dato = slaveT.readStringUntil('\n');
dato.trim();

if (dato.length() > 0)
T = dato.toFloat();
}

// ===============================
// ENVIO A PYTHON
// ===============================

float tiempo = (millis() - t0) / 1000.0;

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

// ===============================
// TIEMPO DE CICLO
// ===============================

delay(80);

}