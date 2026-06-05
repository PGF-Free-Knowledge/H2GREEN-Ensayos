void setup() {

  Serial.begin(9600);
  Serial3.begin(9600);   // STEPPER

  delay(2000);

  Serial.println("TEST MEGA → STEPPER");
}

void loop() {

  Serial.println("Enviando VEL=1");
  Serial3.println("VEL=1");

  delay(2000);

  Serial.println("Enviando VEL=0");
  Serial3.println("VEL=0");

  delay(2000);
}