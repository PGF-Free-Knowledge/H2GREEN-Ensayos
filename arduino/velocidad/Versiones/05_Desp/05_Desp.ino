#include <SoftwareSerial.h>

SoftwareSerial link(3, 2); // RX, TX hacia maestro

float D = 0.0;       // desplazamiento actual
float SP_D = 0.0;    // setpoint desplazamiento

float velocidad = 0.5;   // rapidez del actuador simulado

void setup() {
  link.begin(9600);
}

void loop() {

  // ---- COMUNICACION ----
  if (link.available()) {

    String comando = link.readStringUntil('\n');
    comando.trim();

    if (comando == "READ") {
      link.println(D, 2);
    }

    if (comando.startsWith("SP_D=")) {
      SP_D = comando.substring(5).toFloat();
    }
  }

  // ---- DINAMICA SIMULADA ----
  if (D < SP_D) {
    D += velocidad;
  }
  else if (D > SP_D) {
    D -= velocidad;
  }

  delay(20);
}