#include <AccelStepper.h>

// Pines del driver
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

void setup() {

  Serial.begin(9600);

  stepper.setMaxSpeed(4000);
  stepper.setAcceleration(2000);

  Serial.println("Stepper listo - control velocidad");
}

void loop() {

  stepper.runSpeed();

  // =====================
  // RECEPCION MAESTRO
  // =====================

  if (Serial.available()) {

    String msg = Serial.readStringUntil('\n');
    msg.trim();

    if (msg.startsWith("VEL=")) {

      velocidad_mm = msg.substring(4).toFloat();

      velocidad_steps = velocidad_mm * PASOS_POR_MM;

      stepper.setSpeed(velocidad_steps);

      // debug
      Serial.print("VEL mm/s: ");
      Serial.println(velocidad_mm);
    }
  }
}