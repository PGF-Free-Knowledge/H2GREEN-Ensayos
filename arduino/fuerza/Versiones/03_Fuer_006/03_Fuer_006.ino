#include <SoftwareSerial.h>

SoftwareSerial link(3, 2);  // RX, TX

// =====================
// VARIABLES
// =====================

float SP_F_objetivo = 0.0;
float SP_F = 0.0;

float F = 0.0;
float D = 0.0;
float SP_D = 0.0;

float Kp = 0.15;     // más suave
float Ki = 0.05;     // integral lenta

float integral = 0.0;

float k = 2.0;       // F = k*D

unsigned long lastTime = 0;

// =====================
// SETUP
// =====================

void setup() {
  link.begin(9600);
  lastTime = millis();
}

// =====================
// LOOP
// =====================

void loop() {

  // ===== RECIBIR =====
  if (link.available()) {

    String entrada = link.readStringUntil('\n');
    entrada.trim();

    if (entrada.startsWith("SP_F="))
      SP_F_objetivo = entrada.substring(5).toFloat();

    if (entrada.startsWith("D="))
      D = entrada.substring(2).toFloat();
  }

  // ===== RAMPA SUAVE =====
  float velocidad_rampa = 1.0;

  if (SP_F < SP_F_objetivo)
    SP_F += velocidad_rampa;
  else if (SP_F > SP_F_objetivo)
    SP_F -= velocidad_rampa;

  // ===== MODELO =====
  F = k * D;

  // ===== TIEMPO =====
  unsigned long now = millis();
  float dt = (now - lastTime) / 1000.0;
  lastTime = now;

  // ===== CONTROL =====
  float error = SP_F - F;

  integral += error * dt;

  if (integral > 50) integral = 50;
  if (integral < -50) integral = -50;

  // ---- FEEDFORWARD ----
  float D_ff = SP_F / k;

  // ---- PI CORRECTOR ----
  float D_corr = Kp * error + Ki * integral;

  SP_D = D_ff + D_corr;

  // límites físicos
  if (SP_D > 100) SP_D = 100;
  if (SP_D < 0) SP_D = 0;

  // ===== RESPUESTA =====
  link.print("F=");
  link.print(F, 2);
  link.print(";SP_D=");
  link.println(SP_D, 2);

  delay(50);
}