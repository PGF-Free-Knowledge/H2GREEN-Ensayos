// ===============================
// ESCLAVO PRESION
// ===============================

#define SENSOR A0

float presion = 0;
float filtro = 0;

float SP_P = 0;

void setup()
{

Serial.begin(9600);

Serial.println("Esclavo presion listo");

}

// ===============================

void loop()
{

if(Serial.available())
{

String cmd = Serial.readStringUntil('\n');
cmd.trim();

// ===============================
// SETPOINT PRESION
// ===============================

if(cmd.startsWith("SP_P="))
{
SP_P = cmd.substring(5).toFloat();
}

// ===============================
// LECTURA
// ===============================

if(cmd=="READ")
{

int raw = analogRead(SENSOR);

// ejemplo conversión (ajustar según sensor)
presion = raw * 0.00488;

// filtro digital
filtro = filtro*0.85 + presion*0.15;

Serial.println(filtro,3);

}

}

}