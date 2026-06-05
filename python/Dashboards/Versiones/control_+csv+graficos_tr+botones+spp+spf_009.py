import serial
import time
import matplotlib.pyplot as plt
from collections import deque
import csv

# =========================
# CONFIGURACION
# =========================

PUERTO = 'COM4'
BAUDIOS = 9600

SP_P = 20.0      # Setpoint presión
SP_F = 30.0      # Setpoint fuerza 30.0, Prueba1, probaré con SP_F=50.0, para ver F=50 y D=25, sí se cumple
                                        #Prueba 2, probaré con SP_F=10, para ver F=10 y D=5, sí cumple
                                        #lo regresé a 30.0, F=30 y D=15
MAX_PUNTOS = 200

# =========================
# CONEXION SERIAL
# =========================

arduino = serial.Serial(PUERTO, BAUDIOS, timeout=1)
time.sleep(2)

print("Conectado a Arduino")

# =========================
# GRAFICOS
# =========================

plt.ion()

fig, ax = plt.subplots()

t_data = deque(maxlen=MAX_PUNTOS)
P_data = deque(maxlen=MAX_PUNTOS)
F_data = deque(maxlen=MAX_PUNTOS)
D_data = deque(maxlen=MAX_PUNTOS)

lineP, = ax.plot([], [], label="Presion")
lineF, = ax.plot([], [], label="Fuerza")
lineD, = ax.plot([], [], label="Desplazamiento")

ax.legend()
ax.set_xlabel("Tiempo (s)")
ax.set_ylabel("Valor")

# =========================
# CSV
# =========================

archivo = open("datos.csv", "w", newline="")
writer = csv.writer(archivo)
writer.writerow(["t", "P", "F", "D", "T"])

# =========================
# LOOP PRINCIPAL
# =========================

ultimo_envio = 0

while True:

    if arduino.in_waiting:
        linea = arduino.readline().decode(errors='ignore').strip()
        print("Arduino:", linea)

        if linea.startswith("t="):

            try:
                partes = linea.split(";")

                t = float(partes[0].split("=")[1])
                P = float(partes[1].split("=")[1])
                F = float(partes[2].split("=")[1])
                D = float(partes[3].split("=")[1])
                T = float(partes[4].split("=")[1])

                # ---- guardar CSV ----
                writer.writerow([t, P, F, D, T])

                # ---- actualizar buffers ----
                t_data.append(t)
                P_data.append(P)
                F_data.append(F)
                D_data.append(D)

                # ---- actualizar grafica ----
                lineP.set_data(t_data, P_data)
                lineF.set_data(t_data, F_data)
                lineD.set_data(t_data, D_data)

                ax.relim()
                ax.autoscale_view()
                plt.pause(0.001)

            except:
                pass

    # =========================
    # ENVIO SETPOINTS (cada 1 s)
    # =========================
    if time.time() - ultimo_envio > 1.0:

        envioP = f"SP_P={SP_P}\n"
        envioF = f"SP_F={SP_F}\n"

        arduino.write(envioP.encode())
        arduino.write(envioF.encode())

        print("Enviado:", envioP.strip())
        print("Enviado:", envioF.strip())

        ultimo_envio = time.time()
