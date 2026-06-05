#include <SoftwareSerial.h>
#include <AccelStepper.h>

// ============================
// COMUNICACION CON MAESTRO
// ============================
// RX = 3 (desde Mega TX3)
// TX = 2 (hacia Mega RX3)

SoftwareSerial link(3, 2);

// ============================
// DRIVER STEPPER
// ============================

const int PIN_STEP = 8;
const int PIN_DIR  = 9;

AccelStepper stepper(1, PIN_STEP, PIN_DIR);

// ============================
// PARAMETROS MECANICOS
// ============================

const float PASOS_POR_VUELTA = 1600.0;
const float MM_POR_VUELTA = 5.0;

const float PASOS_POR_MM = PASOS_POR_VUELTA / MM_POR_VUELTA;

// ============================
// VARIABLES
// ============================

float velocidad_mm = 0.0;
float velocidad_steps = 0.0;

unsigned long lastSend = 0;

// ============================

void setup() {

  Serial.begin(9600);     // DEBUG
  link.begin(9600);       // MEGA

  stepper.setMaxSpeed(4000);
  stepper.setAcceleration(2000);

  stepper.setCurrentPosition(0);   // ORIGEN

  Serial.println("STEPPER CON POSICION LISTO");
}

// ============================

void loop() {

  // Movimiento continuo
  stepper.setSpeed(velocidad_steps);
  stepper.runSpeed();

  // =========================
  // RECIBIR COMANDOS
  // =========================

  if (link.available()) {

    String msg = link.readStringUntil('\n');
    msg.trim();

    if (msg.startsWith("VEL=")) {

      velocidad_mm = msg.substring(4).toFloat();
      velocidad_steps = velocidad_mm * PASOS_POR_MM;

      Serial.print("VEL mm/s: ");
      Serial.println(velocidad_mm);
    }

    // Reset de posición
    if (msg == "ZERO") {

      stepper.setCurrentPosition(0);
      Serial.println("POSICION RESETEADA");
    }
  }

  // =========================
  // ENVIAR POSICION AL MAESTRO
  // =========================

  if (millis() - lastSend > 200) {

    lastSend = millis();

    long pasos = stepper.currentPosition();
    float desplazamiento_mm = pasos / PASOS_POR_MM;

    // Enviar al Mega
    link.print("POS=");
    link.println(desplazamiento_mm, 3);

    // Debug
    Serial.print("D(mm): ");
    Serial.println(desplazamiento_mm);
  }
}