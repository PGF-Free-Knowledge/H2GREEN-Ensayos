#include <SoftwareSerial.h>

SoftwareSerial link(3, 2); // RX, TX

float presion = 20.0;
float SP_P = 20.0;

float Kp = 0.8;
float Ki = 0.1;

float integral = 0.0;

unsigned long lastTime = 0;
const unsigned long sampleTime = 50; // ms (50 ms)

void setup() {
  link.begin(9600);
  lastTime = millis();
}

void loop() {

  // ==========================
  // CONTROL CADA 50 ms
  // ==========================
  unsigned long now = millis();

  if (now - lastTime >= sampleTime) {

    float dt = (now - lastTime) / 1000.0;
    lastTime = now;

    float error = SP_P - presion;

    // Integrador
    integral += error * dt;

    float salida = Kp * error + Ki * integral;

    // Simulación planta (limitamos velocidad)
    salida = constrain(salida, -5, 5);

    presion = presion + salida;
  }

  // ==========================
  // COMUNICACION
  // ==========================
  if (link.available()) {

    String msg = link.readStringUntil('\n');
    msg.trim();

    if (msg.startsWith("SET")) {
      SP_P = msg.substring(4).toFloat();
    }

    else if (msg == "READ") {
      link.println(presion);
    }
  }
}