import serial
import time
import csv
import matplotlib.pyplot as plt
from collections import deque

# -------------------------------
# CONFIGURACION
# -------------------------------
PUERTO = 'COM4'
BAUDIOS = 9600
VENTANA = 100

# -------------------------------
# CONEXION
# -------------------------------
arduino = serial.Serial(PUERTO, BAUDIOS, timeout=1)
time.sleep(2)

print("Conectado a Arduino")

# -------------------------------
# ARCHIVO CSV
# -------------------------------
archivo_csv = open("datos.csv", "w", newline="")
writer = csv.writer(archivo_csv)
writer.writerow(["t", "P", "F", "D", "T"])

# -------------------------------
# ESTRUCTURAS DATOS
# -------------------------------
tiempo = deque(maxlen=VENTANA)
P_data = deque(maxlen=VENTANA)
F_data = deque(maxlen=VENTANA)
D_data = deque(maxlen=VENTANA)

# -------------------------------
# GRAFICAS
# -------------------------------
plt.ion()

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

# ----- Grafica vs Tiempo -----
lineP, = ax1.plot([], [], label="Presion P")
lineF, = ax1.plot([], [], label="Fuerza F")
lineD, = ax1.plot([], [], label="Desplazamiento D")

ax1.set_xlabel("Tiempo (s)")
ax1.set_ylabel("Valor")
ax1.legend()
ax1.grid(True)

# ----- Grafica F vs D -----
lineFD, = ax2.plot([], [], label="F vs D")
ax2.set_xlabel("Desplazamiento D")
ax2.set_ylabel("Fuerza F")
ax2.legend()
ax2.grid(True)

# -------------------------------
# LOOP
# -------------------------------
try:
    while True:

        if arduino.in_waiting:

            linea = arduino.readline().decode().strip()
            print("Arduino:", linea)

            if linea.startswith("t="):

                partes = linea.split(";")

                t = float(partes[0].split("=")[1])
                P = float(partes[1].split("=")[1])
                F = float(partes[2].split("=")[1])
                T = float(partes[4].split("=")[1])

                # ----- MODELO -----
                D = P * 0.5 + F * 0.3

                arduino.write(f"D={D:.2f}\n".encode())

                writer.writerow([t, P, F, D, T])

                # guardar datos
                tiempo.append(t)
                P_data.append(P)
                F_data.append(F)
                D_data.append(D)

                # actualizar grafica tiempo
                lineP.set_data(tiempo, P_data)
                lineF.set_data(tiempo, F_data)
                lineD.set_data(tiempo, D_data)

                ax1.relim()
                ax1.autoscale_view()

                # actualizar grafica F vs D
                lineFD.set_data(D_data, F_data)

                ax2.relim()
                ax2.autoscale_view()

                plt.pause(0.01)

except KeyboardInterrupt:
    print("\nPrograma detenido")
    archivo_csv.close()
    arduino.close()
    plt.close()
