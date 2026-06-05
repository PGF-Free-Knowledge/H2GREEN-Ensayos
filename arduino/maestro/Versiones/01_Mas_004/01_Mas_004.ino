#include <SoftwareSerial.h>

// ===============================
// DEFINICIÓN DE ESCLAVOS
// ===============================

SoftwareSerial slaveP(2, 3);        // Presión
SoftwareSerial slaveF(4, 5);        // Fuerza
SoftwareSerial slaveT(6, 7);        // Temperatura
SoftwareSerial slaveStepper(8, 9);  // Stepper (antes desplazamiento)(8,9) x (10,11)

// ===============================
// VARIABLES
// ===============================

float P = 0.0;
float F = 0.0;
float T = 0.0;
float D = 0.0;        // Ahora será estimado = SP_D
float SP_D = 0.0;

float SP_P = 20.0;
float SP_F = 0.0;

unsigned long t0;

// ===============================
// SETUP
// ===============================

void setup() {

  Serial.begin(9600);

  slaveP.begin(9600);
  slaveF.begin(9600);
  slaveT.begin(9600);
  slaveStepper.begin(9600);

  Serial.println("Sistema Maestro iniciado - Version Stepper");

  t0 = millis();
}

// ===============================
// LOOP
// ===============================

void loop() {

  // ====================================
  // RECIBIR SETPOINTS DESDE PYTHON
  // ====================================
  if (Serial.available()) {

    String entrada = Serial.readStringUntil('\n');
    entrada.trim();

    if (entrada.startsWith("SP_P="))
      SP_P = entrada.substring(5).toFloat();

    if (entrada.startsWith("SP_F="))
      SP_F = entrada.substring(5).toFloat();
  }

  // ====================================
  // ENVIAR D (estimado) Y SP_F A FUERZA
  // ====================================
  slaveF.listen();

  slaveF.print("D=");
  slaveF.println(D, 2);

  delay(5);

  slaveF.print("SP_F=");
  slaveF.println(SP_F, 2);

  delay(20);

  // ====================================
  // RECIBIR F Y SP_D DESDE FUERZA
  // ====================================
  if (slaveF.available()) {

    String r = slaveF.readStringUntil('\n');
    r.trim();

    if (r.startsWith("F=") && r.indexOf(";SP_D=") > 0) {

      int sep = r.indexOf(";");

      String partF = r.substring(0, sep);
      String partSP = r.substring(sep + 1);

      float F_recibida = partF.substring(2).toFloat();
      float SP_D_recibido = partSP.substring(5).toFloat();

      if (F_recibida >= 0 && F_recibida <= 5000)
        F = F_recibida;

      if (SP_D_recibido >= 0 && SP_D_recibido <= 200)
        SP_D = SP_D_recibido;
    }
  }

  // ====================================
  // ENVIAR SP_D AL STEPPER
  // ====================================
  slaveStepper.listen();
  slaveStepper.print("SP_D=");
  slaveStepper.println(SP_D, 2);

  // ====================================
  // ACTUALIZAR D ESTIMADO
  // ====================================
  D = SP_D;   // Hasta integrar Basler

  // ====================================
  // PRESIÓN
  // ====================================
  slaveP.listen();
  slaveP.print("SP_P=");
  slaveP.println(SP_P, 2);

  delay(5);

  slaveP.println("READ");
  delay(20);

  if (slaveP.available()) {
    String r = slaveP.readStringUntil('\n');
    r.trim();
    P = r.toFloat();
  }

  // ====================================
  // TEMPERATURA
  // ====================================
  slaveT.listen();
  slaveT.println("READ");
  delay(20);

  if (slaveT.available()) {
    String r = slaveT.readStringUntil('\n');
    r.trim();
    T = r.toFloat();
  }

  // ====================================
  // ENVÍO GENERAL A PYTHON
  // ====================================
  float tiempo = (millis() - t0) / 1000.0;

  Serial.print("t=");
  Serial.print(tiempo, 3);

  Serial.print(";P=");
  Serial.print(P, 2);

  Serial.print(";F=");
  Serial.print(F, 2);

  Serial.print(";D=");
  Serial.print(D, 2);

  Serial.print(";SPD=");
  Serial.print(SP_D, 2);

  Serial.print(";T=");
  Serial.println(T, 2);

  delay(100);
}