import serial
import time
import csv
import matplotlib.pyplot as plt
from collections import deque

# ===============================
# CONFIGURACION
# ===============================

PUERTO = 'COM4'
BAUDIOS = 9600

SP_P = 50.0      # Setpoint presión, probado con 20.0 y funciona ok también
Kp = 0.8         # Ganancia proporcional

# ===============================
# CONEXION SERIAL
# ===============================

arduino = serial.Serial(PUERTO, BAUDIOS, timeout=1)
time.sleep(2)

print("Conectado a Arduino")

# ===============================
# CSV
# ===============================

archivo = open("datos_control.csv", "w", newline="")
writer = csv.writer(archivo)
writer.writerow(["t", "P", "F", "D", "T"])

# ===============================
# GRAFICOS
# ===============================

plt.ion()

fig, ax = plt.subplots()

t_data = deque(maxlen=200)
P_data = deque(maxlen=200)
F_data = deque(maxlen=200)
D_data = deque(maxlen=200)

lineP, = ax.plot([], [], label="Presion")
lineF, = ax.plot([], [], label="Fuerza")
lineD, = ax.plot([], [], label="Desplazamiento")

ax.legend()
ax.set_xlabel("Tiempo (s)")
ax.set_ylabel("Valor")

# ===============================
# LOOP PRINCIPAL
# ===============================

while True:

    if arduino.in_waiting:

        linea = arduino.readline().decode(errors='ignore').strip()
        print("Arduino:", linea)

        try:
            if linea.startswith("t="):

                partes = linea.split(";")

                t = float(partes[0].split("=")[1])
                P = float(partes[1].split("=")[1])
                F = float(partes[2].split("=")[1])
                D = float(partes[3].split("=")[1])
                T = float(partes[4].split("=")[1])

                # ===============================
                # CONTROL PROPORCIONAL PRESION
                # ===============================

                error = SP_P - P
                D_control = Kp * error

                envio = f"SP_P={SP_P}\n"
                arduino.write(envio.encode())

                print("Enviado:", envio.strip())

                # ===============================
                # GUARDAR CSV
                # ===============================

                writer.writerow([t, P, F, D_control, T])

                # ===============================
                # ACTUALIZAR GRAFICOS
                # ===============================

                t_data.append(t)
                P_data.append(P)
                F_data.append(F)
                D_data.append(D_control)

                lineP.set_data(t_data, P_data)
                lineF.set_data(t_data, F_data)
                lineD.set_data(t_data, D_data)

                ax.relim()
                ax.autoscale_view()

                plt.pause(0.01)

        except Exception as e:
            print("Error:", e)

