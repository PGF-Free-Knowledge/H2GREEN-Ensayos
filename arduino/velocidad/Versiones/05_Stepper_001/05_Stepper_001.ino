#include <AccelStepper.h>

// =========================
// CONFIGURACIÓN DE PINES
// =========================
const int PIN_STEP = 8;
const int PIN_DIR  = 9;

// =========================
// CONFIGURACIÓN MOTOR
// =========================
AccelStepper stepper(1, PIN_STEP, PIN_DIR);

// =========================
// PARÁMETROS MECÁNICOS
// =========================
float pasos_por_mm = 200.0;   // PROVISIONAL (se ajusta después)

// =========================
// VARIABLES
// =========================
float SP_D_mm = 0.0;
long SP_D_pasos = 0;

// =========================
// SETUP
// =========================
void setup() {

  Serial.begin(9600);

  stepper.setMaxSpeed(1500);      // velocidad máxima
  stepper.setAcceleration(800);   // aceleración suave
  stepper.setCurrentPosition(0);

  Serial.println("Stepper Esclavo listo");
}

// =========================
// LOOP
// =========================
void loop() {

  // Movimiento continuo no bloqueante
  stepper.run();

  // =====================
  // RECEPCIÓN SERIAL
  // =====================
  if (Serial.available()) {

    String msg = Serial.readStringUntil('\n');
    msg.trim();

    if (msg.startsWith("SP_D=")) {

      SP_D_mm = msg.substring(5).toFloat();

      SP_D_pasos = SP_D_mm * pasos_por_mm;

      stepper.moveTo(SP_D_pasos);

      Serial.print("Moviendo a mm: ");
      Serial.println(SP_D_mm);
    }
  }
}