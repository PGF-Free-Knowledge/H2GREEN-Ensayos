
import serial
import time
import csv

# -------------------------------
# CONFIGURACION
# -------------------------------
PUERTO = 'COM4'     # Arduino maestro
BAUDIOS = 9600

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
# LOOP PRINCIPAL
# -------------------------------
try:
    while True:

        if arduino.in_waiting:

            linea = arduino.readline().decode().strip()
            print("Arduino:", linea)

            # Solo procesamos líneas de datos
            if linea.startswith("t="):

                try:
                    partes = linea.split(";")

                    t = float(partes[0].split("=")[1])
                    P = float(partes[1].split("=")[1])
                    F = float(partes[2].split("=")[1])
                    D_actual = float(partes[3].split("=")[1])
                    T = float(partes[4].split("=")[1])

                    # -------------------------------
                    # CALCULO DE DESPLAZAMIENTO
                    # (modelo de prueba)
                    # -------------------------------
                    D = P * 0.5 + F * 0.3

                    # Enviar al Arduino
                    envio = f"D={D:.2f}\n"
                    arduino.write(envio.encode())

                    print("Enviado:", envio.strip())

                    # Guardar en CSV
                    writer.writerow([t, P, F, D, T])

                except Exception as e:
                    print("Error procesando datos:", e)

# -------------------------------
# CIERRE LIMPIO
# -------------------------------
except KeyboardInterrupt:
    print("\nPrograma detenido por el usuario")

    archivo_csv.close()
    arduino.close()

    print("Puerto serial cerrado correctamente")
