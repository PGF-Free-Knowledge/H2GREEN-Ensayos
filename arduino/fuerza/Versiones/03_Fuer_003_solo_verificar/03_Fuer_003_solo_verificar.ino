float sp_f = 10.0;     // fuerza deseada
float f_meas = 0;
float error_f = 0;

float Kp = 2.0;

int pwm_out = 0;

void setup() {
  Serial.begin(115200);
  pinMode(9, OUTPUT);
}

void loop() {

  // ---- LECTURA SENSOR ----
  f_meas = analogRead(A0);   // cambiar por tu lectura real

  // ---- ERROR ----
  error_f = sp_f - f_meas;

  // ---- CONTROL SIMPLE ----
  pwm_out = Kp * error_f;

  pwm_out = constrain(pwm_out, 0, 255);

  analogWrite(9, pwm_out);

  // ---- DEBUG ----
  Serial.print("SP:");
  Serial.print(sp_f);
  Serial.print(" F:");
  Serial.print(f_meas);
  Serial.print(" PWM:");
  Serial.println(pwm_out);

  delay(20);
}