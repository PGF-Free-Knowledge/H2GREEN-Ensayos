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

float SP_P = 100.0;

bool modo_auto = false;

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

if(modo_auto)
{
controlPresion();
}

comunicacion();

}

// ===============================
// LECTURA SENSORES
// ===============================

//void leerSensores()   *******SOLO PARA PRUEBA CON POTENCIOMETRO
//{

//int raw1 = analogRead(SENSOR_CAMARA);
//int raw2 = analogRead(SENSOR_BOTELLA);

//P1 = raw1 * 0.1;
//P2 = raw2 * 0.1;

//} **************


// **** PRUEBA CON POTENCIOMETRO SIMULANDO ENTRADA DE PRESION
void leerSensores()
{

int raw1 = analogRead(SENSOR_CAMARA);
int raw2 = analogRead(SENSOR_BOTELLA);

// Simulación con potenciómetro

P1 = 0;//map(raw1, 0, 1023, 0, 120);
P2 = map(raw2, 0, 1023, 0, 120);

}

//***** HASTA ACA ES LA PRUEB DE POTENCIOMETRO

// ===============================
// CONTROL PRESION
// ===============================

void controlPresion()
{

if(P1 < (SP_P - 2))
{
digitalWrite(VALVULA_HVL1,HIGH);
}

if(P1 > SP_P)
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
modo_auto = false;
digitalWrite(VALVULA_HVL2,HIGH);
}

if(cmd=="PURGE_OFF")
{
digitalWrite(VALVULA_HVL2,LOW);
}

// ===============================
// PRESION MANUAL
// ===============================

if(cmd=="PRESS_ON")
{
modo_auto = false;
digitalWrite(VALVULA_HVL1,HIGH);
}

if(cmd=="PRESS_OFF")
{
digitalWrite(VALVULA_HVL1,LOW);
}

// ===============================
// PRESION AUTOMATICA
// ===============================

if(cmd=="AUTO_ON")
{
modo_auto = true;
}

if(cmd=="AUTO_OFF")
{
modo_auto = false;
}

}

}