#include <SoftwareSerial.h>
#include "HX711.h"

SoftwareSerial link(4,5); // RX, TX

#define DT 7
#define SCK 6

HX711 scale;

long offset = 1338549;
float factor = -480027.0;

float filtro = 0;

void setup() {
  link.begin(9600);
  scale.begin(DT,SCK);
}

void loop() {

  if(link.available()) {

    String cmd = link.readStringUntil('\n');
    cmd.trim();

    if(cmd=="READ") {

      long lectura = scale.read_average(10);

      float fuerza = (lectura - offset)/factor;

      filtro = filtro*0.85 + fuerza*0.15;

      link.println(filtro);
    }
  }
}