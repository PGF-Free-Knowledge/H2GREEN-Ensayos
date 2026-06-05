#include <SoftwareSerial.h>
#include "HX711.h"

SoftwareSerial link(3,2);   // RX, TX

#define HX_DT 5
#define HX_SCK 4

HX711 scale;

float calibration_factor = 1.0;

void setup()
{

Serial.begin(115200);
link.begin(9600);

scale.begin(HX_DT, HX_SCK);

scale.set_scale(calibration_factor);
scale.tare();

}

void loop()
{

float force = scale.get_units(10);

link.print("F=");
link.println(force,3);

delay(100);

}