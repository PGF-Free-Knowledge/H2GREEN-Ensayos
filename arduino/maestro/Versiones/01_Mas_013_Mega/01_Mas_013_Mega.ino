#include <Arduino.h>

// ================================
// VARIABLES
// ================================

float fuerza = 0;
float presion = 0;
float temperatura = 0;
float desplazamiento = 0;

float velocidad = 0;

unsigned long t0;

// parametros mecanicos
const float PASOS_POR_VUELTA = 1600.0;
const float MM_POR_VUELTA = 5.0;

const float PASOS_POR_MM = PASOS_POR_VUELTA / MM_POR_VUELTA;

// ================================
// SETUP
// ================================

void setup()
{

Serial.begin(9600);     // PC
Serial1.begin(9600);    // fuerza
Serial2.begin(9600);    // presion
Serial3.begin(9600);    // stepper

t0 = millis();

Serial.println("MAESTRO MEGA LISTO");

}

// ================================
// LOOP
// ================================

void loop()
{

leerComandoPC();

leerFuerza();

leerPresion();

leerTemperatura();

leerDesplazamiento();

enviarPC();

delay(20);

}

// ================================
// LEER COMANDOS DASHBOARD
// ================================

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

// ================================
// FUERZA
// ================================

void leerFuerza()
{

Serial1.println("READ");

unsigned long t = millis();

while(!Serial1.available())
{
if(millis()-t > 50) return;
}

fuerza = Serial1.parseFloat();

}

// ================================
// PRESION
// ================================

void leerPresion()
{

Serial2.println("READ");

unsigned long t = millis();

while(!Serial2.available())
{
if(millis()-t > 50) return;
}

presion = Serial2.parseFloat();

}

// ================================
// TEMPERATURA
// ================================

void leerTemperatura()
{

temperatura = 25;   // provisional hasta instalar sensor

}

// ================================
// DESPLAZAMIENTO
// ================================

void leerDesplazamiento()
{

// si luego agregamos encoder o conteo de pasos
// aqui se calcula

}

// ================================
// ENVIAR DATOS AL DASHBOARD
// ================================

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