import serial
import time

arduino = serial.Serial('COM4', 9600, timeout=1)
time.sleep(2)

print("Conectado a Arduino")

while True:

    if arduino.in_waiting:
        linea = arduino.readline().decode().strip()
        print("Arduino:", linea)

        try:
            if linea.startswith("t="):

                partes = linea.split(";")

                P = float(partes[1].split("=")[1])

                # Cálculo de D
                # D = P * 0.5
                # D = 99
                D = P * 0.5 + F * 0.3

                envio = f"D={D:.2f}\n"
                arduino.write(envio.encode())

                print("Enviado:", envio.strip())

        except Exception as e:
            print("Error:", e)
