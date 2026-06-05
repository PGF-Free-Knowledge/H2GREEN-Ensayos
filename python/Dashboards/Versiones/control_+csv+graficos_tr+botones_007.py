import serial
import time
import csv
import matplotlib.pyplot as plt
from collections import deque
import keyboard

# -------------------------------
# CONFIG
# -------------------------------
PUERTO = 'COM4'
BAUDIOS = 9600
VENTANA = 200

arduino = serial.Serial(PUERTO, BAUDIOS, timeout=1)
time.sleep(2)

print("Conectado a Arduino")
print("S = iniciar | E = detener")

ensayo_activo = False

# -------------------------------
# CSV
# -------------------------------
archivo_csv = open("datos.csv", "w", newline="")
writer = csv.writer(archivo_csv)
writer.writerow(["t","P","F","D","T"])

# -------------------------------
# DATOS
# -------------------------------
tiempo = deque(maxlen=VENTANA)
P_data = deque(maxlen=VENTANA)
F_data = deque(maxlen=VENTANA)
D_data = deque(maxlen=VENTANA)

# -------------------------------
# GRAFICA
# -------------------------------
plt.ion()
fig, (ax1, ax2) = plt.subplots(2,1)
fig.canvas.draw()
plt.show(block=False)

lineP, = ax1.plot([],[],label="P")
lineF, = ax1.plot([],[],label="F")
lineD, = ax1.plot([],[],label="D")

ax1.legend()
ax1.grid(True)

lineFD, = ax2.plot([],[],label="F vs D")
ax2.legend()
ax2.grid(True)

ultimo_dibujo = time.time()

# -------------------------------
# LOOP
# -------------------------------
try:
    while True:

        if keyboard.is_pressed('s'):
            ensayo_activo = True
            print("ENSAYO INICIADO")
            time.sleep(0.4)

        if keyboard.is_pressed('e'):
            ensayo_activo = False
            print("ENSAYO DETENIDO")
            time.sleep(0.4)

        if arduino.in_waiting:

            linea = arduino.readline().decode(errors='ignore').strip()
            print("Arduino:", linea)

            if linea.startswith("t="):

                partes = linea.split(";")

                t = float(partes[0].split("=")[1])
                P = float(partes[1].split("=")[1])
                F = float(partes[2].split("=")[1])
                T = float(partes[4].split("=")[1])

                if ensayo_activo:

                    D = P*0.5 + F*0.3
                    arduino.write(f"D={D:.2f}\n".encode())

                    writer.writerow([t,P,F,D,T])

                    tiempo.append(t)
                    P_data.append(P)
                    F_data.append(F)
                    D_data.append(D)

        # -------- ACTUALIZACION GRAFICA --------
        if time.time() - ultimo_dibujo > 0.2:

            if len(tiempo) > 5:

                lineP.set_data(tiempo,P_data)
                lineF.set_data(tiempo,F_data)
                lineD.set_data(tiempo,D_data)

                lineFD.set_data(D_data,F_data)

                ax1.relim()
                ax1.autoscale_view()

                ax2.relim()
                ax2.autoscale_view()

                fig.canvas.draw_idle()
                fig.canvas.flush_events()

            ultimo_dibujo = time.time()

except KeyboardInterrupt:
    archivo_csv.close()
    arduino.close()
    plt.close()
    print("Programa cerrado")
