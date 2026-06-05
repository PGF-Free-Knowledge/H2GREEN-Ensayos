#include <SoftwareSerial.h>
#include <AccelStepper.h>

SoftwareSerial link(3, 2);  // RX, TX hacia maestro

const int PIN_STEP = 8;
const int PIN_DIR  = 9;

AccelStepper stepper(1, PIN_STEP, PIN_DIR);

const float PASOS_POR_VUELTA = 1600.0;
const float MM_POR_VUELTA = 5.0;
const float PASOS_POR_MM = PASOS_POR_VUELTA / MM_POR_VUELTA;

float SP_D_mm = 0.0;
long target_steps = 0;

char MODO = 'F';  // 'F' o 'D'
float velocidad_mm_s = 0.0;

void setup() {

  link.begin(9600);

  stepper.setMaxSpeed(3000);
  stepper.setAcceleration(1000);
  stepper.setCurrentPosition(0);
}

void loop() {

  // =============================
  // RECEPCIÓN DE COMANDOS
  // =============================
  if (link.available()) {

    String mensaje = link.readStringUntil('\n');
    mensaje.trim();

    if (mensaje.startsWith("MODE=")) {
      MODO = mensaje.substring(5)[0];
    }

    if (mensaje.startsWith("SP_D=") && MODO == 'F') {
      SP_D_mm = mensaje.substring(5).toFloat();
      target_steps = SP_D_mm * PASOS_POR_MM;
      stepper.moveTo(target_steps);
    }

    if (mensaje.startsWith("VEL=") && MODO == 'D') {
      velocidad_mm_s = mensaje.substring(4).toFloat();
      stepper.setSpeed(velocidad_mm_s * PASOS_POR_MM);
    }
  }

  // =============================
  // EJECUCIÓN SEGÚN MODO
  // =============================

  if (MODO == 'F') {
    stepper.run();        // movimiento por posición
  }

  if (MODO == 'D') {
    stepper.runSpeed();   // movimiento continuo
  }
}