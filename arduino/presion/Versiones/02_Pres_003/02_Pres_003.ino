#include <SoftwareSerial.h>

SoftwareSerial link(2,3); // RX, TX

#define SENSOR_CAMARA A0
#define SENSOR_BOTELLA A1

float P1 = 0;
float P2 = 0;

void setup() {

link.begin(9600);

}

void loop() {

if(link.available()) {

String cmd = link.readStringUntil('\n');
cmd.trim();

if(cmd=="READ") {

// simulación temporal (hasta tener sensores reales)

P1 = random(900,1000)/10.0;
P2 = random(1000,1200)/10.0;

link.print("P1=");
link.print(P1,2);

link.print(";P2=");
link.println(P2,2);

}

}

}