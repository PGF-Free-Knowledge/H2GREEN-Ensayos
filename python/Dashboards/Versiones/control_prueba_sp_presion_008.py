import serial
import time

# ===============================
# CONFIGURACION
# ===============================
PUERTO = "COM4"
BAUDIOS = 9600

arduino = serial.Serial(PUERTO, BAUDIOS, timeout=1)
time.sleep(2)

print("Conectado a Arduino")

# Setpoints de prueba
setpoints = [20, 50, 80]
indice_sp = 0
ultimo_cambio = time.time()

while True:

    # ------------------------------
    # RECIBIR DATOS DEL ARDUINO
    # ------------------------------
    if arduino.in_waiting:
        linea = arduino.readline().decode(errors="ignore").strip()
        print("Arduino:", linea)

    # ------------------------------
    # CAMBIO AUTOMATICO DE SETPOINT
    # ------------------------------
    if time.time() - ultimo_cambio > 10:

        sp = setpoints[indice_sp]

        envio = f"SP_P={sp}\n"
        arduino.write(envio.encode())

        print("Enviado:", envio.strip())

        indice_sp += 1
        if indice_sp >= len(setpoints):
            indice_sp = 0

        ultimo_cambio = time.time()
