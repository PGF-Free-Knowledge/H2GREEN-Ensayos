#include <AccelStepper.h>

const int STEP_PIN = 8;
const int DIR_PIN  = 9;

AccelStepper stepper(1, STEP_PIN, DIR_PIN);

const float PASOS_POR_MM = 320.0;

float velocidad = 0;
long posicion = 0;

void setup() {
  Serial.begin(9600);

  stepper.setMaxSpeed(4000);
  stepper.setAcceleration(2000);
}

void loop() {

  stepper.runSpeed();

  posicion = stepper.currentPosition();

  float D = posicion / PASOS_POR_MM;

  // enviar posición
  Serial.print("POS=");
  Serial.println(D,3);

  // recibir comandos
  if(Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if(cmd.startsWith("VEL=")) {
      velocidad = cmd.substring(4).toFloat();
      stepper.setSpeed(velocidad * PASOS_POR_MM);
    }

    if(cmd=="ZERO") {
      stepper.setCurrentPosition(0);
    }
  }
}