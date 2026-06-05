#include <SoftwareSerial.h>
#include <AccelStepper.h>

SoftwareSerial link(3, 2);

const int PIN_STEP = 8;
const int PIN_DIR  = 9;

AccelStepper stepper(1, PIN_STEP, PIN_DIR);

const float PASOS_POR_VUELTA = 1600.0;
const float MM_POR_VUELTA = 5.0;
const float PASOS_POR_MM = PASOS_POR_VUELTA / MM_POR_VUELTA;

char MODO = 'F';
char modoAnterior = 'F';

float velocidad_mm_s = 0.0;

void setup() {

  link.begin(9600);

  stepper.setMaxSpeed(3000);
  stepper.setAcceleration(1000);
  stepper.setCurrentPosition(0);
}

void loop() {

  if (link.available()) {

    String mensaje = link.readStringUntil('\n');
    mensaje.trim();

    // -------- MODO --------
    if (mensaje.startsWith("MODE=")) {

      MODO = mensaje.substring(5)[0];

      // Solo actuar si realmente cambió el modo
      if (MODO != modoAnterior) {

        if (MODO == 'F') {
          velocidad_mm_s = 0;
          stepper.setSpeed(0);
          stepper.setCurrentPosition(0);  // reset SOLO al cambiar
        }

        modoAnterior = MODO;
      }
    }

    // -------- POSICIÓN --------
    if (mensaje.startsWith("SP_D=") && MODO == 'F') {

      float SP_D_mm = mensaje.substring(5).toFloat();
      long target_steps = SP_D_mm * PASOS_POR_MM;

      stepper.moveTo(target_steps);
    }

    // -------- VELOCIDAD --------
    if (mensaje.startsWith("VEL=") && MODO == 'D') {

      velocidad_mm_s = mensaje.substring(4).toFloat();
      stepper.setSpeed(velocidad_mm_s * PASOS_POR_MM);
    }
  }

  // EJECUCIÓN CONTINUA
  if (MODO == 'F') {
    stepper.run();
  }

  if (MODO == 'D') {
    stepper.runSpeed();
  }
}