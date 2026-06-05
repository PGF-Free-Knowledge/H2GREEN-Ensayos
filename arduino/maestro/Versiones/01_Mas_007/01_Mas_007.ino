#include <SoftwareSerial.h>

// ===============================
// ESCLAVOS
// ===============================

SoftwareSerial slaveP(2,3);
SoftwareSerial slaveF(4,5);
SoftwareSerial slaveT(6,7);
SoftwareSerial slaveStepper(8,9);

// ===============================

float P = 0;
float F = 0;
float T = 0;
float D = 0;

float SP_P = 0;
float VEL = 0;

// ===============================

unsigned long t0;

unsigned long lastSend = 0;
unsigned long lastPressure = 0;
unsigned long lastForce = 0;
unsigned long lastTemp = 0;
unsigned long lastStepper = 0;

// intervalos (ms)

const int sendInterval = 50;     // 20 Hz envío a Python
const int pressureInterval = 40;
const int forceInterval = 40;
const int tempInterval = 200;
const int stepperInterval = 50;

// ===============================

void setup() {

  Serial.begin(9600);

  slaveP.begin(9600);
  slaveF.begin(9600);
  slaveT.begin(9600);
  slaveStepper.begin(9600);

  Serial.println("Maestro optimizado listo");

  t0 = millis();
}

// ===============================

void loop() {

  unsigned long now = millis();

  // ===============================
  // RECIBIR PYTHON
  // ===============================

  if (Serial.available()) {

    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd.startsWith("SP_P="))
      SP_P = cmd.substring(5).toFloat();

    if (cmd.startsWith("VEL="))
      VEL = cmd.substring(4).toFloat();
  }

  // ===============================
  // ENVIAR VELOCIDAD AL STEPPER
  // ===============================

  if (now - lastStepper >= stepperInterval) {

    slaveStepper.listen();

    slaveStepper.print("VEL=");
    slaveStepper.println(VEL);

    lastStepper = now;
  }

  // ===============================
  // PRESION
  // ===============================

  if (now - lastPressure >= pressureInterval) {

    slaveP.listen();

    slaveP.print("SP_P=");
    slaveP.println(SP_P);

    delay(2);

    slaveP.println("READ");

    delay(3);

    if (slaveP.available()) {

      String val = slaveP.readStringUntil('\n');
      val.trim();

      P = val.toFloat();
    }

    lastPressure = now;
  }

  // ===============================
  // FUERZA
  // ===============================

  if (now - lastForce >= forceInterval) {

    slaveF.listen();

    slaveF.println("READ");

    delay(3);

    if (slaveF.available()) {

      String val = slaveF.readStringUntil('\n');
      val.trim();

      F = val.toFloat();
    }

    lastForce = now;
  }

  // ===============================
  // TEMPERATURA
  // ===============================

  if (now - lastTemp >= tempInterval) {

    slaveT.listen();

    slaveT.println("READ");

    delay(3);

    if (slaveT.available()) {

      String val = slaveT.readStringUntil('\n');
      val.trim();

      T = val.toFloat();
    }

    lastTemp = now;
  }

  // ===============================
  // ENVIO A PYTHON
  // ===============================

  if (now - lastSend >= sendInterval) {

    float tiempo = (now - t0) / 1000.0;

    Serial.print("t=");
    Serial.print(tiempo);

    Serial.print(";P=");
    Serial.print(P,3);

    Serial.print(";F=");
    Serial.print(F,5);

    Serial.print(";D=");
    Serial.print(D,3);

    Serial.print(";T=");
    Serial.println(T,2);

    lastSend = now;
  }
}