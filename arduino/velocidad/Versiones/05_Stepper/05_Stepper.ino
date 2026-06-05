#include <AccelStepper.h>

// PINES
const int PIN_STEP = 8;
const int PIN_DIR = 9;

// CONFIGURACIÓN DEL MOTOR
// 1 significa que usamos un driver (A4988, TB6600, SH1108, etc.)
AccelStepper stepper1(1, PIN_STEP, PIN_DIR); 

// CONSTANTES DE PRUEBA
const float VEL_LENTA = 400;   
const float VEL_RAPIDA = 1000; 
const long PASOS_PRUEBA = -3200; // Ajusta esto según el microstepping de tu driver

// VARIABLES DE ESTADO
bool enMovimiento = false;
bool avisoEspera = false;

void setup() {
  Serial.begin(9600);
  delay(1000); 
  
  // Configuración inicial de movimiento
  stepper1.setMaxSpeed(VEL_LENTA); 
  stepper1.setAcceleration(800); // Aceleración suave para Nema 34
  stepper1.setCurrentPosition(0); 
  
  Serial.println("--- PRUEBA DE MOTOR NEMA 34 LISTA ---");
  Serial.println("Comandos: 'iniciar', 'volver', 'detener'");
}

void loop() {
  // Ejecución obligatoria para que el motor se mueva
  stepper1.run();

  // Control de avisos al terminar movimiento
  if (!stepper1.isRunning() && enMovimiento) {
    enMovimiento = false;
    avisoEspera = false;
    Serial.print(">> Motor detenido en posicion: ");
    Serial.println(stepper1.currentPosition());
  }

  // Aviso de espera (solo una vez)
  if (!stepper1.isRunning() && !avisoEspera) {
    Serial.println("\nEsperando comando...");
    avisoEspera = true;
  }

  // LECTURA DE COMANDOS
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();

    if (comando == "iniciar") {
      Serial.println(">> Girando hacia OBJETIVO...");
      stepper1.setMaxSpeed(VEL_LENTA);
      stepper1.moveTo(PASOS_PRUEBA);
      enMovimiento = true;
    } 
    else if (comando == "volver") {
      Serial.println(">> Retornando a ORIGEN (0)...");
      stepper1.setMaxSpeed(VEL_RAPIDA);
      stepper1.moveTo(0);
      enMovimiento = true;
    } 
    else if (comando == "detener") {
      Serial.println("!!! PARADA DE EMERGENCIA !!!");
      stepper1.stop();
    }
  }
}
