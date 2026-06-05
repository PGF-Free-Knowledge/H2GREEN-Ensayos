#include <SoftwareSerial.h>

// ===============================
// ESCLAVOS
// ===============================
SoftwareSerial slaveP(2, 3);
SoftwareSerial slaveF(4, 5);
SoftwareSerial slaveT(6, 7);
SoftwareSerial slaveStepper(8, 9);

// ===============================
// VARIABLES
// ===============================
float P = 0.0;
float F = 0.0;
float T = 0.0;
float D = 0.0;
float SP_D = 0.0;

float SP_P = 20.0;
float SP_F = 0.0;

char MODO = 'F';      // 'F' = Fuerza | 'D' = Desplazamiento
float VEL = 1.0;      // mm/s

unsigned long t0;

// ===============================
void setup() {

  Serial.begin(9600);

  slaveP.begin(9600);
  slaveF.begin(9600);
  slaveT.begin(9600);
  slaveStepper.begin(9600);

  t0 = millis();
}

// ===============================
void loop() {

  // ===============================
  // RECIBIR DESDE PYTHON
  // ===============================
  if (Serial.available()) {

    String entrada = Serial.readStringUntil('\n');
    entrada.trim();

    if (entrada.startsWith("SP_P="))
      SP_P = entrada.substring(5).toFloat();

    if (entrada.startsWith("SP_F="))
      SP_F = entrada.substring(5).toFloat();

    if (entrada.startsWith("MODE="))
      MODO = entrada.substring(5)[0];

    if (entrada.startsWith("VEL="))
      VEL = entrada.substring(4).toFloat();
  }

  // ===============================
  // FUERZA
  // ===============================
  slaveF.listen();

  slaveF.print("D=");
  slaveF.println(D, 2);

  slaveF.print("SP_F=");
  slaveF.println(SP_F, 2);

  delay(10);

  if (slaveF.available()) {

    String r = slaveF.readStringUntil('\n');
    r.trim();

    if (r.startsWith("F=") && r.indexOf(";SP_D=") > 0) {

      int sep = r.indexOf(";");

      F = r.substring(2, sep).toFloat();
      SP_D = r.substring(sep + 6).toFloat();
    }
  }

  // ===============================
  // STEPPER
  // ===============================
  slaveStepper.listen();

  slaveStepper.print("MODE=");
  slaveStepper.println(MODO);

  if (MODO == 'F') {
    slaveStepper.print("SP_D=");
    slaveStepper.println(SP_D, 2);
  }

  if (MODO == 'D') {
    slaveStepper.print("VEL=");
    slaveStepper.println(VEL, 2);
  }

  D = SP_D;

  // ===============================
  // PRESIÓN
  // ===============================
  slaveP.listen();
  slaveP.print("SP_P=");
  slaveP.println(SP_P);

  slaveP.println("READ");
  delay(10);

  if (slaveP.available()) {
    P = slaveP.readStringUntil('\n').toFloat();
  }

  // ===============================
  // TEMPERATURA
  // ===============================
  slaveT.listen();
  slaveT.println("READ");
  delay(10);

  if (slaveT.available()) {
    T = slaveT.readStringUntil('\n').toFloat();
  }

  // ===============================
  // ENVÍO A PYTHON
  // ===============================
  float tiempo = (millis() - t0) / 1000.0;

  Serial.print("t=");
  Serial.print(tiempo, 3);

  Serial.print(";P=");
  Serial.print(P, 2);

  Serial.print(";F=");
  Serial.print(F, 2);

  Serial.print(";D=");
  Serial.print(D, 2);

  Serial.print(";T=");
  Serial.println(T, 2);

  delay(100);
}