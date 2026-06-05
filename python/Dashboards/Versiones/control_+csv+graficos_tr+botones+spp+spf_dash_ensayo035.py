import sys
import time
import serial
import numpy as np
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
import csv

# ===============================
# DISPLAY DIGITAL
# ===============================

class DigitalDisplay(QtWidgets.QFrame):

    def __init__(self,titulo,unidad):

        super().__init__()

        self.setStyleSheet("""
        QFrame{
        background:black;
        border:2px solid #333;
        border-radius:8px;
        }
        """)

        layout=QtWidgets.QVBoxLayout()

        self.label_titulo=QtWidgets.QLabel(titulo)
        self.label_titulo.setAlignment(QtCore.Qt.AlignCenter)
        self.label_titulo.setStyleSheet("color:white;font-size:12px")

        self.label_valor=QtWidgets.QLabel("0.00")
        self.label_valor.setAlignment(QtCore.Qt.AlignCenter)
        self.label_valor.setStyleSheet("color:#00ff00;font-size:20px")

        self.label_unidad=QtWidgets.QLabel(unidad)
        self.label_unidad.setAlignment(QtCore.Qt.AlignCenter)
        self.label_unidad.setStyleSheet("color:white;font-size:11px")

        layout.addWidget(self.label_titulo)
        layout.addWidget(self.label_valor)
        layout.addWidget(self.label_unidad)

        self.setLayout(layout)

    def setValue(self,val):

        self.label_valor.setText(f"{val:.2f}")

# ===============================
# SERIAL THREAD
# ===============================

class SerialWorker(QtCore.QThread):

    data_received = QtCore.pyqtSignal(float,float,float,float,float)

    def __init__(self,port="COM4",baudrate=9600):

        super().__init__()

        self.port=port
        self.baudrate=baudrate
        self.running=True

    def run(self):

        try:

            ser=serial.Serial(self.port,self.baudrate,timeout=1)

            time.sleep(2)

            while self.running:

                line=ser.readline().decode(errors='ignore').strip()

                if line.startswith("t="):

                    try:

                        parts=line.split(";")

                        t=float(parts[0].split("=")[1])
                        P=float(parts[1].split("=")[1])
                        F=float(parts[2].split("=")[1])
                        D=float(parts[3].split("=")[1])
                        T=float(parts[4].split("=")[1])

                        self.data_received.emit(t,F,D,P,T)

                    except:
                        pass

        except Exception as e:

            print("Error serial:",e)

    def send_command(self,cmd):

        try:

            ser=serial.Serial(self.port,self.baudrate)
            ser.write((cmd+"\n").encode())
            ser.close()

        except:
            pass

# ===============================
# DASHBOARD
# ===============================

class Dashboard(QtWidgets.QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Sistema Ensayo Tracción")
        self.setGeometry(100,100,1500,900)

        self.running=False
        self.velocidad_guardada=0

        self.t_data=[]
        self.f_data=[]
        self.d_data=[]
        self.p_data=[]
        self.temp_data=[]

        tabs=QtWidgets.QTabWidget()
        self.setCentralWidget(tabs)

        tab_operacion=QtWidgets.QWidget()
        tab_graficos=QtWidgets.QWidget()

        tabs.addTab(tab_operacion,"Operación")
        tabs.addTab(tab_graficos,"Gráficos")

        layout=QtWidgets.QVBoxLayout()
        tab_operacion.setLayout(layout)

        titulo=QtWidgets.QLabel("Sistema de Ensayo Mecánico Servo-Controlado")
        titulo.setAlignment(QtCore.Qt.AlignCenter)
        titulo.setStyleSheet("font-size:20px;font-weight:bold")

        layout.addWidget(titulo)

        descripcion=QtWidgets.QLabel(
        "Sistema de caracterización mecánica que mide en tiempo real:\n"
        "Fuerza, Desplazamiento, Presión y Temperatura.\n"
        "Control de velocidad mediante motor stepper."
        )

        descripcion.setAlignment(QtCore.Qt.AlignCenter)

        layout.addWidget(descripcion)

        self.estado=QtWidgets.QLabel("● DETENIDO")
        self.estado.setAlignment(QtCore.Qt.AlignCenter)
        self.estado.setStyleSheet("font-size:18px;color:red")

        layout.addWidget(self.estado)

        grid=QtWidgets.QGridLayout()

        self.dispF=DigitalDisplay("Fuerza","kN")
        self.dispD=DigitalDisplay("Desplazamiento","mm")
        self.dispP=DigitalDisplay("Presión","MPa")
        self.dispT=DigitalDisplay("Temperatura","°C")
        self.dispV=DigitalDisplay("Velocidad","mm/s")

        grid.addWidget(self.dispF,0,0)
        grid.addWidget(self.dispD,0,1)
        grid.addWidget(self.dispP,0,2)
        grid.addWidget(self.dispT,1,0)
        grid.addWidget(self.dispV,1,1)

        layout.addLayout(grid)

        botones=QtWidgets.QHBoxLayout()

        self.btn_start=QtWidgets.QPushButton("INICIAR")
        self.btn_stop=QtWidgets.QPushButton("STOP")
        self.btn_return=QtWidgets.QPushButton("RETORNAR")

        botones.addWidget(self.btn_start)
        botones.addWidget(self.btn_stop)
        botones.addWidget(self.btn_return)

        layout.addLayout(botones)

        self.btn_start.clicked.connect(self.start_test)
        self.btn_stop.clicked.connect(self.stop_test)
        self.btn_return.clicked.connect(self.return_home)

        # SERIAL

        self.serial=SerialWorker()
        self.serial.data_received.connect(self.update_data)
        self.serial.start()

    def start_test(self):

        self.estado.setText("● ENSAYO EN CURSO")
        self.estado.setStyleSheet("color:green;font-size:18px")

        self.running=True

    def stop_test(self):

        self.estado.setText("● DETENIDO")
        self.estado.setStyleSheet("color:red;font-size:18px")

        self.running=False

        self.serial.send_command("VEL=0")

    def return_home(self):

        self.serial.send_command("RET")

    def update_data(self,t,F,D,P,T):

        self.dispF.setValue(F)
        self.dispD.setValue(D)
        self.dispP.setValue(P)
        self.dispT.setValue(T)
        self.dispV.setValue(self.velocidad_guardada)

# ===============================

if __name__ == "__main__":

    app=QtWidgets.QApplication(sys.argv)

    window=Dashboard()
    window.show()

    sys.exit(app.exec_())
