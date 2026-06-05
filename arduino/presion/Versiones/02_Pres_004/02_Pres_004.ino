#include <SoftwareSerial.h>

SoftwareSerial link(2,3); // RX, TX

// ===============================
// PINES
// ===============================

#define SENSOR_CAMARA A0
#define SENSOR_BOTELLA A1

#define VALVULA_HVL1 8
#define VALVULA_HVL2 9

// ===============================
// VARIABLES
// ===============================

float P1 = 0;
float P2 = 0;

float SP = 100.0;   // setpoint presión

// ===============================

void setup() {

link.begin(9600);

pinMode(VALVULA_HVL1,OUTPUT);
pinMode(VALVULA_HVL2,OUTPUT);

digitalWrite(VALVULA_HVL1,LOW);
digitalWrite(VALVULA_HVL2,LOW);

}

// ===============================

void loop() {

leerSensores();
controlPresion();
comunicacion();

}

// ===============================
// LECTURA SENSORES
// ===============================

void leerSensores()
{

int raw1 = analogRead(SENSOR_CAMARA);
int raw2 = analogRead(SENSOR_BOTELLA);

// Simulación temporal (reemplazar luego por 4-20mA real)

P1 = raw1 * 0.1;
P2 = raw2 * 0.1;

}

// ===============================
// CONTROL PRESION
// ===============================

void controlPresion()
{

if(P1 < (SP - 2))
{
digitalWrite(VALVULA_HVL1,HIGH);
}

if(P1 > SP)
{
digitalWrite(VALVULA_HVL1,LOW);
}

}

// ===============================
// COMUNICACION
// ===============================

void comunicacion()
{

if(link.available())
{

String cmd = link.readStringUntil('\n');
cmd.trim();

// ===============================
// LECTURA
// ===============================

if(cmd=="READ")
{

link.print("P1=");
link.print(P1,2);

link.print(";P2=");
link.println(P2,2);

}

// ===============================
// PURGA
// ===============================

if(cmd=="PURGE_ON")
{
digitalWrite(VALVULA_HVL2,HIGH);
}

if(cmd=="PURGE_OFF")
{
digitalWrite(VALVULA_HVL2,LOW);
}

// ===============================
// PRESION ON/OFF
// ===============================

if(cmd=="PRESS_ON")
{
digitalWrite(VALVULA_HVL1,HIGH);
}

if(cmd=="PRESS_OFF")
{
digitalWrite(VALVULA_HVL1,LOW);
}

}

}