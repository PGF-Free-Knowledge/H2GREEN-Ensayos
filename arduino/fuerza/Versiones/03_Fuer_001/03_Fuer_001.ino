#include <SoftwareSerial.h>

SoftwareSerial link(3, 2);  // RX, TX hacia maestro

// =====================
// VARIABLES
// =====================

float SP_F_objetivo = 0.0;   // lo que envía el maestro
float SP_F = 0.0;            // setpoint interno (filtrado)
float F = 0.0;
float D = 0.0;
float SP_D = 0.0;

float Kp = 0.15;
float Ki = 0.10;

float integral = 0.0;

float k = 2.0;   // rigidez simulada

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

  // =====================
  // RECIBIR DATOS DEL MAESTRO
  // =====================

  if (link.available()) {

    String entrada = link.readStringUntil('\n');
    entrada.trim();

    if (entrada.startsWith("SP_F=")) {
      SP_F_objetivo = entrada.substring(5).toFloat();
    }

    if (entrada.startsWith("D=")) {
      D = entrada.substring(2).toFloat();
    }
  }

  // =====================
  // FILTRO SUAVE DEL SETPOINT
  // (evita saltos bruscos)
  // =====================

  float velocidad_rampa = 1.0;   // N por ciclo

  if (SP_F < SP_F_objetivo)
    SP_F += velocidad_rampa;
  else if (SP_F > SP_F_objetivo)
    SP_F -= velocidad_rampa;

  // =====================
  // MODELO FUERZA
  // =====================

  F = k * D;

  // Protección física básica
  if (F > 1000) F = 1000;
  if (F < -1000) F = -1000;

  // =====================
  // CONTROL PI
  // =====================

  unsigned long now = millis();
  float dt = (now - lastTime) / 1000.0;
  lastTime = now;

  float error = SP_F - F;

  integral += error * dt;

  // ---- Anti-windup ----
  if (integral > 50) integral = 50;
  if (integral < -50) integral = -50;

  SP_D = Kp * error + Ki * integral;

  // ---- Saturación segura ----
  if (SP_D > 100) SP_D = 100;
  if (SP_D < 0) SP_D = 0;

  // =====================
  // RESPUESTA LIMPIA AL MAESTRO
  // =====================

  link.print("F=");
  link.print(F, 2);
  link.print(";SP_D=");
  link.println(SP_D, 2);

  delay(50);
}
