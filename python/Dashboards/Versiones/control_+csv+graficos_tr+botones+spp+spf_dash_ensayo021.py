import sys
import time
import serial
import numpy as np
import csv
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg

# =========================
# SERIAL THREAD
# =========================

class SerialWorker(QtCore.QThread):

    data_received = QtCore.pyqtSignal(float, float, float, float, float)

    def __init__(self, port="COM4", baudrate=9600):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.running = True
        self.ser = None

def run(self):

    try:
        self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
        time.sleep(2)

        while self.running:

            line = self.ser.readline().decode(errors='ignore').strip()

            if line.startswith("t="):

                parts = line.split(";")

                try:
                    t = float(parts[0].split("=")[1])
                    P = float(parts[1].split("=")[1])
                    F = float(parts[2].split("=")[1])
                    D = float(parts[3].split("=")[1])
                    T = float(parts[4].split("=")[1])

                    self.data_received.emit(t, F, D, P, T)

                except:
                    pass

    except Exception as e:
        print("Error serial:", e)

def send(self, msg):

    if self.ser and self.ser.is_open:
        self.ser.write((msg + "\n").encode())

def stop(self):

    self.running = False

    if self.ser:
        self.ser.close()

    self.quit()
    self.wait()
# =========================
# DASHBOARD
# =========================

class Dashboard(QtWidgets.QMainWindow):

    def __init__(self):

        super().__init__()

    self.setWindowTitle("Maquina de Ensayo - Control de Velocidad")
    self.setGeometry(100,100,1600,950)

    self.running = False

    self.offset_F = None
    self.offset_D = None
    self.offset_t = None

    self.t_data=[]
    self.f_data=[]
    self.d_data=[]
    self.p_data=[]
    self.temp_data=[]

    # CSV
    self.csv_file=None
    self.csv_writer=None

    central=QtWidgets.QWidget()
    self.setCentralWidget(central)

    layout=QtWidgets.QVBoxLayout()
    central.setLayout(layout)

    # =========================
    # PANEL CONTROL
    # =========================

    control=QtWidgets.QHBoxLayout()
    layout.addLayout(control)

    self.input_vel=QtWidgets.QLineEdit()
    self.input_vel.setPlaceholderText("Velocidad mm/s")

    self.input_sp_p=QtWidgets.QLineEdit()
    self.input_sp_p.setPlaceholderText("SP Presion")

    self.btn_send=QtWidgets.QPushButton("Enviar SP")

    control.addWidget(self.input_vel)
    control.addWidget(self.input_sp_p)
    control.addWidget(self.btn_send)

    self.btn_send.clicked.connect(self.send_setpoints)

    # =========================
    # INDICADORES
    # =========================

    indicators=QtWidgets.QHBoxLayout()
    layout.addLayout(indicators)

    self.labelF=QtWidgets.QLabel("Fuerza: 0 N")
    self.labelD=QtWidgets.QLabel("Desplazamiento: 0 mm")
    self.labelP=QtWidgets.QLabel("Presion: 0")
    self.labelT=QtWidgets.QLabel("Temp: 0")

    indicators.addWidget(self.labelF)
    indicators.addWidget(self.labelD)
    indicators.addWidget(self.labelP)
    indicators.addWidget(self.labelT)

    # =========================
    # GRAFICOS
    # =========================

    grid=QtWidgets.QGridLayout()
    layout.addLayout(grid)

    self.plotF=pg.PlotWidget(title="Fuerza vs Tiempo")
    self.plotD=pg.PlotWidget(title="Desplazamiento vs Tiempo")
    self.plotP=pg.PlotWidget(title="Presion vs Tiempo")
    self.plotT=pg.PlotWidget(title="Temperatura vs Tiempo")

    grid.addWidget(self.plotF,0,0)
    grid.addWidget(self.plotD,0,1)
    grid.addWidget(self.plotP,1,0)
    grid.addWidget(self.plotT,1,1)

    self.curveF=self.plotF.plot(pen='r')
    self.curveD=self.plotD.plot(pen='g')
    self.curveP=self.plotP.plot(pen='b')
    self.curveT=self.plotT.plot(pen='y')

    # F vs D

    self.plotFD=pg.PlotWidget(title="Fuerza vs Desplazamiento")
    layout.addWidget(self.plotFD)

    self.curveFD=self.plotFD.plot(pen='w')

    # =========================
    # BOTONES
    # =========================

    buttons=QtWidgets.QHBoxLayout()
    layout.addLayout(buttons)

    self.btn_start=QtWidgets.QPushButton("INICIAR")
    self.btn_stop=QtWidgets.QPushButton("STOP")
    self.btn_reset=QtWidgets.QPushButton("RESET")

    buttons.addWidget(self.btn_start)
    buttons.addWidget(self.btn_stop)
    buttons.addWidget(self.btn_reset)

    self.btn_start.clicked.connect(self.start_test)
    self.btn_stop.clicked.connect(self.stop_test)
    self.btn_reset.clicked.connect(self.reset_graphs)

    # =========================
    # SERIAL
    # =========================

    self.serial=SerialWorker(port="COM4")
    self.serial.data_received.connect(self.update_data)
    self.serial.start()


# =========================
# SETPOINTS
# =========================

def send_setpoints(self):

    try:
        vel=float(self.input_vel.text())
        self.serial.send(f"VEL={vel}")
    except:
        pass

    try:
        sp=float(self.input_sp_p.text())
        self.serial.send(f"SP_P={sp}")
    except:
        pass


# =========================
# START
# =========================

def start_test(self):

    self.reset_graphs()

    self.running=True

    filename=time.strftime("Ensayo_%Y%m%d_%H%M%S.csv")

    self.csv_file=open(filename,"w",newline='')
    self.csv_writer=csv.writer(self.csv_file)

    self.csv_writer.writerow(["t","F","D","P","T"])

    print("Guardando:",filename)


# =========================
# STOP
# =========================

def stop_test(self):

    self.running=False

    self.serial.send("VEL=0")

    if self.csv_file:
        self.csv_file.close()


# =========================
# RESET
# =========================

def reset_graphs(self):

    self.t_data.clear()
    self.f_data.clear()
    self.d_data.clear()
    self.p_data.clear()
    self.temp_data.clear()

    self.offset_F=None
    self.offset_D=None
    self.offset_t=None


# =========================
# UPDATE DATA
# =========================

def update_data(self,t,F,D,P,T):

    # actualizar indicadores

    self.labelF.setText(f"Fuerza: {F:.2f} N")
    self.labelD.setText(f"Desplazamiento: {D:.2f} mm")
    self.labelP.setText(f"Presion: {P:.2f}")
    self.labelT.setText(f"Temp: {T:.2f}")

    if not self.running:
        return

    if self.offset_F is None:

        self.offset_F=F
        self.offset_D=D
        self.offset_t=t

    F_corr=F-self.offset_F
    D_corr=D-self.offset_D
    t_corr=t-self.offset_t

    self.t_data.append(t_corr)
    self.f_data.append(F_corr)
    self.d_data.append(D_corr)
    self.p_data.append(P)
    self.temp_data.append(T)

    self.curveF.setData(self.t_data,self.f_data)
    self.curveD.setData(self.t_data,self.d_data)
    self.curveP.setData(self.t_data,self.p_data)
    self.curveT.setData(self.t_data,self.temp_data)

    if len(self.d_data)>5:

        d=np.array(self.d_data)
        f=np.array(self.f_data)

        idx=np.argsort(d)

        self.curveFD.setData(d[idx],f[idx])

    # guardar CSV

    if self.csv_writer:
        self.csv_writer.writerow([t_corr,F_corr,D_corr,P,T])


def closeEvent(self,event):

    self.serial.stop()

    if self.csv_file:
        self.csv_file.close()

    event.accept()
# =========================
# MAIN
# =========================

  if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec_())
