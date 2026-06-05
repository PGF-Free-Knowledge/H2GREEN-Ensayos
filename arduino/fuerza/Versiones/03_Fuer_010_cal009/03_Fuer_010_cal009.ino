#include <SoftwareSerial.h>

SoftwareSerial link(3,2);

void setup() {

  Serial.begin(9600);
  link.begin(9600);

  Serial.println("Test esclavo fuerza");
}

void loop() {

  if (link.available()) {

    String cmd = link.readStringUntil('\n');
    cmd.trim();

    if (cmd == "READ") {

      link.println(12.34);   // valor fijo de prueba

      Serial.println("Enviado 12.34");
    }
  }
}