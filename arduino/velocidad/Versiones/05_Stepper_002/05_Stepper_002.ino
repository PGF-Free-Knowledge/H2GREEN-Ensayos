#include <AccelStepper.h>

// =========================
// PINES
// =========================
const int PIN_STEP = 8;
const int PIN_DIR  = 9;

// =========================
// CONFIG MOTOR
// =========================
AccelStepper stepper(1, PIN_STEP, PIN_DIR);

// =========================
// PARAMETROS MECANICOS
// =========================
const float PASOS_POR_VUELTA = 1600.0;   // Por tu microstep
const float MM_POR_VUELTA = 5.0;         // PROVISIONAL (luego ajustamos)
const float PASOS_POR_MM = PASOS_POR_VUELTA / MM_POR_VUELTA;

// =========================
// VARIABLES
// =========================
float SP_D_mm = 0.0;
long  target_steps = 0;

void setup() {

  Serial.begin(9600);

  stepper.setMaxSpeed(2000);
  stepper.setAcceleration(1000);
  stepper.setCurrentPosition(0);

  Serial.println("Stepper listo - modo automatico");
}

void loop() {

  stepper.run();

  if (Serial.available()) {

    String mensaje = Serial.readStringUntil('\n');
    mensaje.trim();

    if (mensaje.startsWith("SP_D=")) {

      SP_D_mm = mensaje.substring(5).toFloat();

      target_steps = SP_D_mm * PASOS_POR_MM;

      stepper.moveTo(target_steps);

      Serial.print("Nuevo SP_D: ");
      Serial.print(SP_D_mm);
      Serial.print(" mm  | pasos: ");
      Serial.println(target_steps);
    }
  }
}
