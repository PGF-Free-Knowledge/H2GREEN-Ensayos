import serial
import time

arduino = serial.Serial('COM4', 9600, timeout=1)
time.sleep(2)

while True:

    if arduino.in_waiting:
        linea = arduino.readline().decode().strip()

        print("Arduino:", linea)

        # ejemplo simple:
        # D = presión * 0.5
        try:
            partes = linea.split(';')
            P = float(partes[1].split('=')[1])

            D = P * 0.5

            envio = f"D={D:.2f}\n"
            arduino.write(envio.encode())

        except:
            pass
