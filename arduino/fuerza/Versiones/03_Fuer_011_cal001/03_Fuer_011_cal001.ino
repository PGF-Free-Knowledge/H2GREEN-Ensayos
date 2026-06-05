#include "HX711.h"

#define DT 7
#define SCK 6

HX711 scale;

long offset = 0;
float factor = 1;

void setup() {

  Serial.begin(9600);

  scale.begin(DT, SCK);

  delay(2000);

  Serial.println("CALIBRACION HX711");
  Serial.println("Retire toda la carga...");
  delay(5000);

  Serial.println("Midiendo OFFSET...");

  offset = scale.read_average(50);

  Serial.print("OFFSET = ");
  Serial.println(offset);

  Serial.println("Coloque peso conocido.");
  Serial.println("Luego escriba el valor en kg y presione ENTER.");

}

void loop() {

  if (Serial.available()) {

    String entrada = Serial.readStringUntil('\n');
    entrada.trim();

    if (entrada.length() == 0) return;

    float peso = entrada.toFloat();

    Serial.print("Peso ingresado = ");
    Serial.println(peso);

    Serial.println("Midiendo con peso...");

    long lectura = scale.read_average(50);

    long delta = lectura - offset;

    factor = delta / peso;

    Serial.println("==============");

    Serial.print("LECTURA = ");
    Serial.println(lectura);

    Serial.print("DELTA = ");
    Serial.println(delta);

    Serial.println("==============");

    Serial.print("OFFSET FINAL = ");
    Serial.println(offset);

    Serial.print("FACTOR FINAL = ");
    Serial.println(factor);

    Serial.println("==============");

    Serial.println("Copie estos valores en el codigo del esclavo");

  }

}