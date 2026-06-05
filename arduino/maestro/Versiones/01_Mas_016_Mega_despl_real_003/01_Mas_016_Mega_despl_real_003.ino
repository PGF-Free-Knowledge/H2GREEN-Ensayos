#include <Arduino.h>
#include <SoftwareSerial.h>

// temperatura
SoftwareSerial tempSerial(11,10); // RX, TX

float P=0, F=0, T=0, D=

unsigned long t0;

void setup() {

  Serial.begin(9600);

  Serial1.begin(9600); // presión
  Serial2.begin(9600); // fuerza
  Serial3.begin(9600); // stepper
  tempSerial.begin(9600);

  delay(2000);

  t0 = millis();

  Serial.println("MAESTRO FINAL OK");
}

void loop() {

  float t = (millis()-t0)/1000.0;

  // pedir datos
  Serial1.println("READ");
  Serial2.println("READ");
  tempSerial.println("READ");

  delay(120);

  if(Serial1.available()) P = Serial1.readStringUntil('\n').toFloat();
  if(Serial2.available()) F = Serial2.readStringUntil('\n').toFloat();
  if(tempSerial.available()) T = tempSerial.readStringUntil('\n').toFloat();

  while(Serial3.available()) {
    String msg = Serial3.readStringUntil('\n');
    if(msg.startsWith("POS=")) {
      D = msg.substring(4).toFloat();
    }
  }

  // comandos PC
  if(Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    Serial3.println(cmd);
  }

  // salida final
  Serial.print("t=");
  Serial.print(t,3);

  Serial.print(";P=");
  Serial.print(P,2);

  Serial.print(";F=");
  Serial.print(F,4);

  Serial.print(";D=");
  Serial.print(D,3);

  Serial.print(";T=");
  Serial.println(T,2);

  delay(100);
}