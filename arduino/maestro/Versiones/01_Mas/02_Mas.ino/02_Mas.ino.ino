#include <SoftwareSerial.h>

SoftwareSerial slaveP(2, 3); // RX, TX

void setup() {
  Serial.begin(9600);
  slaveP.begin(9600);

  Serial.println("TEST SETPOINT PRESION");
}

void loop() {

  // --- enviar setpoint ---
  slaveP.listen();
  slaveP.println("SET:50");

  delay(200);

  if (slaveP.available()) {
    Serial.print("RESPUESTA SET: ");
    Serial.println(slaveP.readStringUntil('\n'));
  }

  delay(2000);

  // --- pedir lectura normal ---
  slaveP.listen();
  slaveP.println("READ");

  delay(200);

  if (slaveP.available()) {
    Serial.print("RESPUESTA READ: ");
    Serial.println(slaveP.readStringUntil('\n'));
  }

  delay(3000);
}