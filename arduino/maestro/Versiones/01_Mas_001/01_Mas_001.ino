#include <SoftwareSerial.h>

SoftwareSerial link(2, 3);  // RX, TX

float SP_F = 20.0;
float F = 0.0;

float D = 0.0;

float Kp = 0.6;
float Ki = 0.25;

float integral = 0.0;

unsigned long lastTime = 0;

void setup() {
  Serial.begin(115200);
  link.begin(9600);
  lastTime = millis();
}

void loop() {

  // ===== RECIBIR F =====
  if (link.available()) {

    String entrada = link.readStringUntil('\n');
    entrada.trim();

    if (entrada.startsWith("F=")) {
      F = entrada.substring(2).toFloat();
    }
  }

  // ===== CONTROL PI =====
  unsigned long now = millis();
  float dt = (now - lastTime) / 1000.0;
  lastTime = now;

  float error = SP_F - F;

  integral += error * dt;

  if (integral > 100) integral = 100;
  if (integral < -100) integral = -100;

  D = Kp * error + Ki * integral;

  if (D > 100) D = 100;
  if (D < 0) D = 0;

  // ===== ENVIAR D =====
  link.println(D);

  // ===== MONITOR =====
  Serial.print("SP_F=");
  Serial.print(SP_F);
  Serial.print("  F=");
  Serial.print(F);
  Serial.print("  D=");
  Serial.println(D);

  delay(20);
}