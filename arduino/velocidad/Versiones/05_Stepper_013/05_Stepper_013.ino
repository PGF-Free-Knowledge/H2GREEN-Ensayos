#include <SoftwareSerial.h>
#include <AccelStepper.h>

// ============================
// COMUNICACION CON MAESTRO
// ============================
// RX = 3  (recibe del Mega TX3)
// TX = 2  (envía al Mega RX3)

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

// ============================

void setup() {

  Serial.begin(9600);     // DEBUG USB
  link.begin(9600);       // COMUNICACION MEGA

  stepper.setMaxSpeed(4000);
  stepper.setAcceleration(2000);

  Serial.println("STEPPER ESCLAVO LISTO");
}

// ============================

void loop() {

  // Ejecuta movimiento continuo
  stepper.setSpeed(velocidad_steps);
  stepper.runSpeed();

  // =========================
  // RECEPCION DESDE MAESTRO
  // =========================

  if (link.available()) {

    String msg = link.readStringUntil('\n');
    msg.trim();

    if (msg.startsWith("VEL=")) {

      velocidad_mm = msg.substring(4).toFloat();
      velocidad_steps = velocidad_mm * PASOS_POR_MM;

      Serial.print("RECIBIDO: ");
      Serial.println(msg);

      Serial.print("Velocidad mm/s: ");
      Serial.println(velocidad_mm);

      Serial.print("Velocidad steps/s: ");
      Serial.println(velocidad_steps);
    }
  }
}