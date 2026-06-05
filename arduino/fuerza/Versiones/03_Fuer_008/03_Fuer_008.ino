#include <SoftwareSerial.h>

SoftwareSerial link(3, 2);  // RX, TX

float SP_F_objetivo = 0.0;
float SP_F = 0.0;

float F = 0.0;
float D = 0.0;
float SP_D = 0.0;

float Kp = 0.28;
float Ki = 0.08;

float integral = 0.0;

float k = 2.0;

unsigned long lastTime = 0;

void setup() {
  link.begin(9600);
  lastTime = millis();
}

void loop() {

  // ===== RECEPCIÓN =====
  if (link.available()) {

    String entrada = link.readStringUntil('\n');
    entrada.trim();

    if (entrada.startsWith("SP_F=")) {
      SP_F_objetivo = entrada.substring(5).toFloat();
    }

    if (entrada.startsWith("D=")) {
      float D_recibido = entrada.substring(2).toFloat();

      if (D_recibido >= 0.0 && D_recibido <= 100.0) {
        D = D_recibido;
      }
    }
  }

  // ===== RAMPA SUAVE =====
  float velocidad_rampa = 1.5;

  if (SP_F < SP_F_objetivo)
    SP_F += velocidad_rampa;
  else if (SP_F > SP_F_objetivo)
    SP_F -= velocidad_rampa;

  // ===== MODELO =====
  F = k * D;

  if (F > 1000) F = 1000;
  if (F < -1000) F = -1000;

  // ===== CONTROL PI =====
  unsigned long now = millis();
  float dt = (now - lastTime) / 1000.0;
  lastTime = now;

  float error = SP_F - F;

  integral += error * dt;

  // anti-windup más ajustado
  if (integral > 80) integral = 80;
  if (integral < -80) integral = -80;

  SP_D = Kp * error + Ki * integral;

  if (SP_D > 100) SP_D = 100;
  if (SP_D < 0) SP_D = 0;

  // ===== RESPUESTA =====
  link.print("F=");
  link.print(F, 2);
  link.print(";SP_D=");
  link.println(SP_D, 2);
}