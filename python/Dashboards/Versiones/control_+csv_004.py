import serial
import time
import csv

# ----- CONFIGURACION -----
PUERTO = 'COM4'
BAUDIOS = 9600
ARCHIVO = "datos.csv"

# ----- CONEXION -----
arduino = serial.Serial(PUERTO, BAUDIOS, timeout=1)
time.sleep(2)

print("Conectado a Arduino")

# ----- CREAR ARCHIVO CSV -----
archivo_csv = open(ARCHIVO, mode="w", newline="")
writer = csv.writer(archivo_csv)

# encabezado
writer.writerow(["t", "P", "F", "D", "T"])

P = 0.0
F = 0.0
T = 0.0
tiempo = 0.0

# ----- LOOP PRINCIPAL -----
while True:

    if arduino.in_waiting:

        linea = arduino.readline().decode(errors='ignore').strip()

        if not linea:
            continue

        print("Arduino:", linea)

        if linea.startswith("t="):

            try:
                partes = linea.split(";")

                for parte in partes:

                    if parte.startswith("t="):
                        tiempo = float(parte.split("=")[1])

                    elif parte.startswith("P="):
                        P = float(parte.split("=")[1])

                    elif parte.startswith("F="):
                        F = float(parte.split("=")[1])

                    elif parte.startswith("T="):
                        T = float(parte.split("=")[1])

                # ----- CALCULO D -----
                D = P * 0.5 + F * 0.3

                # enviar a Arduino
                envio = f"D={D:.2f}\n"
                arduino.write(envio.encode())
                print("Enviado:", envio.strip())

                # guardar en CSV
                writer.writerow([tiempo, P, F, D, T])
                archivo_csv.flush()

            except Exception as e:
                print("Error:", e)
