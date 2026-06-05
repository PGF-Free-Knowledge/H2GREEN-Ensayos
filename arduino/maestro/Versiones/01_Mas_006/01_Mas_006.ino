#include <SoftwareSerial.h>

// ===============================
// ESCLAVOS
// ===============================

SoftwareSerial slaveP(2, 3);
SoftwareSerial slaveF(4, 5);
SoftwareSerial slaveT(6, 7);
SoftwareSerial slaveStepper(8, 9);

// ===============================

float P = 0;
float F = 0;
float T = 0;
float D = 0;

float SP_P = 0;
float VEL = 0;

unsigned long t0;

// ===============================

void setup() {

  Serial.begin(9600);

  slaveP.begin(9600);
  slaveF.begin(9600);
  slaveT.begin(9600);
  slaveStepper.begin(9600);

  Serial.println("Maestro listo");

  t0 = millis();
}

// ===============================

void loop() {

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
  // ENVIAR VEL AL STEPPER
  // ===============================

  slaveStepper.listen();
  slaveStepper.print("VEL=");
  slaveStepper.println(VEL);

  // ===============================
  // PRESION
  // ===============================

  slaveP.listen();

  slaveP.print("SP_P=");
  slaveP.println(SP_P);

  delay(5);

  slaveP.println("READ");

  delay(20);

  if (slaveP.available()) {
    P = slaveP.readStringUntil('\n').toFloat();
  }

  // ===============================
  // FUERZA
  // ===============================

  slaveF.listen();

  slaveF.println("READ");

  delay(20);

  if (slaveF.available()) {
    F = slaveF.readStringUntil('\n').toFloat();
  }

  // ===============================
  // TEMPERATURA
  // ===============================

  slaveT.listen();

  slaveT.println("READ");

  delay(20);

  if (slaveT.available()) {
    T = slaveT.readStringUntil('\n').toFloat();
  }

  // ===============================
  // ENVIO A PYTHON
  // ===============================

  float tiempo = (millis() - t0) / 1000.0;

  Serial.print("t=");
  Serial.print(tiempo);

  Serial.print(";P=");
  Serial.print(P);

  Serial.print(";F=");
  Serial.print(F);

  Serial.print(";D=");
  Serial.print(D);

  Serial.print(";T=");
  Serial.println(T);

  delay(100);
}