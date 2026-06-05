import serial
import time

arduino = serial.Serial('COM4', 9600, timeout=1)
time.sleep(2)

print("Conectado a Arduino")

P = 0.0
F = 0.0
T = 0.0

while True:

    if arduino.in_waiting:

        linea = arduino.readline().decode(errors='ignore').strip()

        if not linea:
            continue

        print("Arduino:", linea)

        # solo procesar datos válidos
        if linea.startswith("t="):

            try:
                partes = linea.split(";")

                for parte in partes:

                    if parte.startswith("P="):
                        P = float(parte.split("=")[1])

                    elif parte.startswith("F="):
                        F = float(parte.split("=")[1])

                    elif parte.startswith("T="):
                        T = float(parte.split("=")[1])

                # -------- CALCULO D --------
                D = P * 0.5 + F * 0.3

                envio = f"D={D:.2f}\n"
                arduino.write(envio.encode())

                print("Enviado:", envio.strip())

            except Exception as e:
                print("Error:", e)
