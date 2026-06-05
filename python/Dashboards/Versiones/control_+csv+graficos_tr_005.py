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

# cantidad de puntos visibles en pantalla
VENTANA = 50

# -------------------------------
# CONEXION SERIAL
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
# DATOS PARA GRAFICA
# -------------------------------
tiempo = deque(maxlen=VENTANA)
P_data = deque(maxlen=VENTANA)
F_data = deque(maxlen=VENTANA)
D_data = deque(maxlen=VENTANA)

plt.ion()
fig, ax = plt.subplots()

lineP, = ax.plot([], [], label="Presion P")
lineF, = ax.plot([], [], label="Fuerza F")
lineD, = ax.plot([], [], label="Desplazamiento D")

ax.set_xlabel("Tiempo (s)")
ax.set_ylabel("Valor")
ax.legend()
ax.grid(True)

# -------------------------------
# LOOP PRINCIPAL
# -------------------------------
try:
    while True:

        if arduino.in_waiting:

            linea = arduino.readline().decode().strip()
            print("Arduino:", linea)

            if linea.startswith("t="):

                try:
                    partes = linea.split(";")

                    t = float(partes[0].split("=")[1])
                    P = float(partes[1].split("=")[1])
                    F = float(partes[2].split("=")[1])
                    D_actual = float(partes[3].split("=")[1])
                    T = float(partes[4].split("=")[1])

                    # ----- CALCULO DE D -----
                    D = P * 0.5 + F * 0.3

                    envio = f"D={D:.2f}\n"
                    arduino.write(envio.encode())

                    # guardar csv
                    writer.writerow([t, P, F, D, T])

                    # guardar datos grafica
                    tiempo.append(t)
                    P_data.append(P)
                    F_data.append(F)
                    D_data.append(D)

                    # actualizar grafica
                    lineP.set_data(tiempo, P_data)
                    lineF.set_data(tiempo, F_data)
                    lineD.set_data(tiempo, D_data)

                    ax.relim()
                    ax.autoscale_view()

                    plt.pause(0.01)

                except Exception as e:
                    print("Error:", e)

except KeyboardInterrupt:
    print("\nPrograma detenido")

    archivo_csv.close()
    arduino.close()
    plt.close()
