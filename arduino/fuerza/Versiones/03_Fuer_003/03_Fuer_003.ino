#include <SoftwareSerial.h>

SoftwareSerial maestro(2, 3); // RX, TX hacia maestro

// ===== VARIABLES =====
float F = 0.0;      // Fuerza simulada
float D = 0.0;      // Desplazamiento recibido
float SP_F = 0.0;   // Setpoint fuerza
float SP_D = 0.0;   // Setpoint desplazamiento

// ===== PARAMETROS CONTROL =====
float Kp_F = 0.5;   // Ganancia proporcional (estable)
float Ki_F = 0.05;  // Integral suave

float errorF = 0.0;
float integralF = 0.0;

unsigned long lastTime = 0;

void setup() {
  Serial.begin(9600);
  maestro.begin(9600);

  Serial.println("Esclavo Fuerza iniciado");
}

void loop() {

  // ===== RECIBIR DATOS DEL MAESTRO =====
  if (maestro.available()) {
    String entrada = maestro.readStringUntil('\n');
    entrada.trim();

    // ---- SETPOINT FUERZA ----
    if (entrada.startsWith("SP_F=")) {
      SP_F = entrada.substring(5).toFloat();
    }

    // ---- DESPLAZAMIENTO ----
    if (entrada.startsWith("D=")) {
      float D_nuevo = entrada.substring(2).toFloat();

      // filtro simple anti-basura serial
      if (D_nuevo >= 0 && D_nuevo <= 100) {
        D = D_nuevo;
      }
    }
  }

  // ===== SIMULACION FUERZA =====
  // Relación mecánica simple
  F = 2.0 * D;

  // ===== CONTROL FUERZA -> SP_D =====
  unsigned long now = millis();
  float dt = (now - lastTime) / 1000.0;

  if (dt > 0.05) {

    errorF = SP_F - F;
    integralF += errorF * dt;

    SP_D = Kp_F * errorF + Ki_F * integralF;

    // límites físicos
    if (SP_D < 0) SP_D = 0;
    if (SP_D > 100) SP_D = 100;

    lastTime = now;
  }

  // ===== RESPUESTA AL MAESTRO =====
  maestro.println(F);

  delay(50);
}