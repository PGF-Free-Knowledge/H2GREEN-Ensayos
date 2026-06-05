#include <SoftwareSerial.h>
#include <max6675.h>

// ============================
// COMUNICACION
// ============================

SoftwareSerial link(3, 2); // RX, TX

// ============================
// MAX6675
// ============================

int pinSO  = 4;
int pinCS  = 5;
int pinSCK = 6;

MAX6675 termocouple(pinSCK, pinCS, pinSO);

// ============================

void setup() {

  Serial.begin(9600);
  link.begin(9600);

  Serial.println("Esclavo temperatura OK");

  delay(500);
}

// ============================

void loop() {

  if (link.available()) {

    String cmd = link.readStringUntil('\n');
    cmd.trim();

    if (cmd == "READ") {

      float temp = termocouple.readCelsius();

      link.println(temp);

      // DEBUG
      Serial.print("Temp enviada: ");
      Serial.println(temp);
    }
  }
}