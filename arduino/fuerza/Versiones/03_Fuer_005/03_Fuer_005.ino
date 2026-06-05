#include <SoftwareSerial.h>

SoftwareSerial link(3, 2);  // RX, TX

float D = 0.0;
float F = 0.0;

float k = 2.0;
float alphaF = 0.15;   // suavizado dinámico

void setup() {
  link.begin(9600);
}

void loop() {

  // ===== RECIBIR D =====
  if (link.available()) {
    String entrada = link.readStringUntil('\n');
    D = entrada.toFloat();
  }

  // ===== MODELO FÍSICO =====
  float F_obj = k * D;

  // dinámica suave
  F += (F_obj - F) * alphaF;

  // ===== ENVIAR F =====
  link.print("F=");
  link.println(F, 2);

  delay(20);
}