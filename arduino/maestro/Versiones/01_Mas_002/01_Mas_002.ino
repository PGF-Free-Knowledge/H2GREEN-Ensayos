#include <SoftwareSerial.h>

SoftwareSerial slaveP(2, 3);
SoftwareSerial slaveF(4, 5);
SoftwareSerial slaveT(6, 7);
SoftwareSerial slaveD(8, 9);

float P = 0.0;
float F = 0.0;
float T = 0.0;
float D = 0.0;

float SP_P = 20.0;
float SP_F = 0.0;
float SP_D = 0.0;

unsigned long t0;

void setup() {

  Serial.begin(9600);

  slaveP.begin(9600);
  slaveF.begin(9600);
  slaveT.begin(9600);
  slaveD.begin(9600);

  Serial.println("Sistema Maestro iniciado");

  t0 = millis();
}

void loop() {

  // ===============================
  // RECIBIR SETPOINTS DESDE PYTHON
  // ===============================
  if (Serial.available()) {

    String entrada = Serial.readStringUntil('\n');
    entrada.trim();

    if (entrada.startsWith("SP_P="))
      SP_P = entrada.substring(5).toFloat();

    if (entrada.startsWith("SP_F="))
      SP_F = entrada.substring(5).toFloat();
  }

  // ===============================
  // LEER DESPLAZAMIENTO
  // ===============================
  slaveD.listen();
  slaveD.println("READ");
  delay(20);

  if (slaveD.available()) {
    String r = slaveD.readStringUntil('\n');
    r.trim();
    D = r.toFloat();
  }

  // ===============================
  // ENVIAR D Y SP_F AL ESCLAVO FUERZA
  // ===============================
  slaveF.listen();

  slaveF.print("D=");
  slaveF.println(D, 2);

  delay(5);

  slaveF.print("SP_F=");
  slaveF.println(SP_F, 2);

  delay(20);

  // ===============================
  // RECIBIR F Y SP_D (CORREGIDO)
  // ===============================
  if (slaveF.available()) {

    String r = slaveF.readStringUntil('\n');
    r.trim();

    // SOLO aceptar paquetes completos
    if (r.startsWith("F=") && r.indexOf(";SP_D=") > 0) {

      int sep = r.indexOf(";");

      String partF = r.substring(0, sep);
      String partSP = r.substring(sep + 1);

      float F_recibida = partF.substring(2).toFloat();
      float SP_D_recibido = partSP.substring(5).toFloat();

      // Validación de rango
      if (F_recibida >= 0 && F_recibida <= 1000)
        F = F_recibida;

      if (SP_D_recibido >= 0 && SP_D_recibido <= 100)
        SP_D = SP_D_recibido;
    }
  }

  // ===============================
  // ENVIAR SP_D AL ESCLAVO D
  // ===============================
  slaveD.listen();
  slaveD.print("SP_D=");
  slaveD.println(SP_D, 2);

  // ===============================
  // PRESION
  // ===============================
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

  // ===============================
  // TEMPERATURA
  // ===============================
  slaveT.listen();
  slaveT.println("READ");
  delay(20);

  if (slaveT.available()) {
    String r = slaveT.readStringUntil('\n');
    r.trim();
    T = r.toFloat();
  }

  // ===============================
  // IMPRESION GENERAL
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

  Serial.print(";SPD=");
  Serial.print(SP_D, 2);

  Serial.print(";T=");
  Serial.println(T, 2);

  delay(100);
}