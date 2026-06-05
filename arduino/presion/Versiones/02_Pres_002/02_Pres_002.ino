#include <SoftwareSerial.h>

SoftwareSerial link(2,3); // RX, TX

void setup() {
  link.begin(9600);
}

void loop() {
  if(link.available()) {
    String cmd = link.readStringUntil('\n');
    cmd.trim();

    if(cmd=="READ") {
      float P = random(200,300)/10.0;
      link.println(P);
    }
  }
}