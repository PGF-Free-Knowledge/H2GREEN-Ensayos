#include <SoftwareSerial.h>
#include <max6675.h>

SoftwareSerial link(3,2); // RX, TX

int pinSO  = 4;
int pinCS  = 5;
int pinSCK = 6;

MAX6675 termocouple(pinSCK, pinCS, pinSO);

void setup() {
  link.begin(9600);
}

void loop() {

  if(link.available()) {

    String cmd = link.readStringUntil('\n');
    cmd.trim();

    if(cmd=="READ") {

      float T = termocouple.readCelsius();

      link.println(T);
    }
  }
}