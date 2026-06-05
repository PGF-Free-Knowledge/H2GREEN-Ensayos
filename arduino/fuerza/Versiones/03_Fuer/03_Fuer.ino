#include <SoftwareSerial.h>

SoftwareSerial link(3, 2);  // RX, TX hacia maestro

float SP_F = 0.0;
float F = 0.0;
float D = 0.0;
float SP_D = 0.0;

float Kp = 0.15;//Kp=0.6, probaré con Kp=0.15
float Ki = 0.10;//Ki=0.8, probaré con Kp=0.10
float integral = 0.0;

float k = 2.0;   // rigidez simulada

void setup() {
  link.begin(9600);
}

void loop() {

  // =========================
  // RECIBIR DATOS DEL MAESTRO
  // =========================
  if (link.available()) {

    String entrada = link.readStringUntil('\n');
    entrada.trim();

    if (entrada.startsWith("SP_F=")) {
      SP_F = entrada.substring(5).toFloat();
    }

    if (entrada.startsWith("D=")) {
      D = entrada.substring(2).toFloat();
    }
  }

  // =========================
  // MODELO FUERZA
  // =========================
  F = k * D;

  // =========================
  // CONTROL PI
  // =========================
  float error = SP_F - F;
  integral += error * 0.1;

  SP_D = Kp * error + Ki * integral;

  if (SP_D < 0) SP_D = 0;
  if (SP_D > 100) SP_D = 100;

  // =========================
  // RESPUESTA AL MAESTRO
  // =========================
  link.print("F=");
  link.print(F, 2);
  link.print(";SP_D=");
  link.println(SP_D, 2);

  delay(100);
}