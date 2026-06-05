import sys
import time
import serial
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
        background-color:black;
        border:2px solid #444;
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
# SERIAL THREAD (OPTIMIZADO)
# ===============================

class SerialWorker(QtCore.QThread):

    data_received = QtCore.pyqtSignal(float,float,float,float,float)

    def __init__(self,port="COM3",baudrate=9600):
        super().__init__()

        self.port=port
        self.baudrate=baudrate
        self.running=True
        self.ser=None
        self.buffer=""

    def run(self):

        try:
            self.ser=serial.Serial(self.port,self.baudrate,timeout=0)
            time.sleep(2)

            while self.running:

                if self.ser.in_waiting:

                    data=self.ser.read(self.ser.in_waiting).decode(errors='ignore')
                    self.buffer += data

                    while '\n' in self.buffer:

                        line, self.buffer = self.buffer.split('\n',1)
                        line=line.strip()

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
        if self.ser and self.ser.is_open:
            self.ser.write((cmd+"\n").encode())

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

        self.F_max_registrada = 0

        self.t_data=[]
        self.f_data=[]
        self.d_data=[]
        self.p_data=[]
        self.temp_data=[]

        self.csv_file=None
        self.csv_writer=None

        tabs=QtWidgets.QTabWidget()
        self.setCentralWidget(tabs)

        tab_operacion=QtWidgets.QWidget()
        tab_graficos=QtWidgets.QWidget()

        tabs.addTab(tab_operacion,"Operación")
        tabs.addTab(tab_graficos,"Gráficos")

        layout=QtWidgets.QVBoxLayout()
        tab_operacion.setLayout(layout)

        titulo=QtWidgets.QLabel("Sistema de Ensayo Mecánico")
        titulo.setStyleSheet("font-size:20px;font-weight:bold")
        titulo.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(titulo)

        config_box=QtWidgets.QGroupBox("Configuración del ensayo")
        config_layout=QtWidgets.QHBoxLayout()

        self.input_vel=QtWidgets.QLineEdit()
        self.input_vel.setPlaceholderText("Velocidad")

        self.unit_box=QtWidgets.QComboBox()
        self.unit_box.addItems(["mm/s","mm/min"])

        self.input_fmax=QtWidgets.QLineEdit()
        self.input_fmax.setPlaceholderText("Fuerza máxima (kN)")

        self.input_file=QtWidgets.QLineEdit()
        self.input_file.setPlaceholderText("Nombre archivo")

        config_layout.addWidget(self.input_vel)
        config_layout.addWidget(self.unit_box)
        config_layout.addWidget(self.input_fmax)
        config_layout.addWidget(self.input_file)

        config_box.setLayout(config_layout)
        layout.addWidget(config_box)

        self.label_archivo = QtWidgets.QLabel("Archivo: ---")
        self.label_archivo.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.label_archivo)

        self.estado=QtWidgets.QLabel("● DETENIDO")
        self.estado.setAlignment(QtCore.Qt.AlignCenter)
        self.estado.setStyleSheet("font-size:18px;color:red")
        layout.addWidget(self.estado)

        grid=QtWidgets.QGridLayout()

        self.dispF=DigitalDisplay("Fuerza","kN")
        self.dispFmax=DigitalDisplay("Fuerza Máxima","kN")
        self.dispD=DigitalDisplay("Desplazamiento","mm")
        self.dispP=DigitalDisplay("Presión","MPa")
        self.dispT=DigitalDisplay("Temperatura","°C")
        self.dispV=DigitalDisplay("Velocidad","mm/s")

        grid.addWidget(self.dispF,0,0)
        grid.addWidget(self.dispFmax,0,1)
        grid.addWidget(self.dispD,0,2)
        grid.addWidget(self.dispP,1,0)
        grid.addWidget(self.dispT,1,1)
        grid.addWidget(self.dispV,1,2)

        layout.addLayout(grid)

        botones=QtWidgets.QHBoxLayout()

        self.btn_start=QtWidgets.QPushButton("INICIAR")
        self.btn_stop=QtWidgets.QPushButton("STOP")
        self.btn_reset=QtWidgets.QPushButton("RESET")
        self.btn_return=QtWidgets.QPushButton("RETORNAR")

        botones.addWidget(self.btn_start)
        botones.addWidget(self.btn_stop)
        botones.addWidget(self.btn_reset)
        botones.addWidget(self.btn_return)

        layout.addLayout(botones)

        layout2=QtWidgets.QGridLayout()
        tab_graficos.setLayout(layout2)

        self.plot_f=pg.PlotWidget(title="Fuerza vs Tiempo")
        self.plot_d=pg.PlotWidget(title="Desplazamiento vs Tiempo")
        self.plot_fd=pg.PlotWidget(title="Fuerza vs Desplazamiento")

        layout2.addWidget(self.plot_f,0,0)
        layout2.addWidget(self.plot_d,0,1)
        layout2.addWidget(self.plot_fd,1,0,1,2)

        self.curve_f=self.plot_f.plot(pen='r')
        self.curve_d=self.plot_d.plot(pen='g')
        self.curve_fd=self.plot_fd.plot(pen='w')

        self.serial=SerialWorker(port="COM3")
        self.serial.data_received.connect(self.update_data)
        self.serial.start()

        self.btn_start.clicked.connect(self.start_test)
        self.btn_stop.clicked.connect(self.stop_test)
        self.btn_reset.clicked.connect(self.reset_test)
        self.btn_return.clicked.connect(self.return_home)

    # RESTO DEL CÓDIGO ORIGINAL SIN MODIFICAR

    def start_test(self):

        self.running=True
        self.F_max_registrada = 0

        self.estado.setText("● ENSAYO EN CURSO")
        self.estado.setStyleSheet("font-size:18px;color:green")

        vel=float(self.input_vel.text())

        if self.unit_box.currentText()=="mm/min":
            vel=vel/60

        self.velocidad_guardada=vel
        self.serial.send_command(f"VEL={vel}")

        filename=self.input_file.text()

        if filename=="":
            filename=time.strftime("ensayo_%Y%m%d_%H%M%S")

        self.label_archivo.setText(f"Archivo: {filename}")

        self.csv_file=open(filename+".csv","w",newline="")
        self.csv_writer=csv.writer(self.csv_file)
        self.csv_writer.writerow(["t","F","D","P","T"])

    def stop_test(self):

        self.running=False
        self.serial.send_command("VEL=0")

        self.estado.setText("● DETENIDO")
        self.estado.setStyleSheet("font-size:18px;color:red")

        if self.csv_file:
            self.csv_file.close()

    def reset_test(self):

        self.t_data=[]
        self.f_data=[]
        self.d_data=[]

        self.curve_f.setData([])
        self.curve_d.setData([])
        self.curve_fd.setData([])

        self.F_max_registrada = 0
        self.dispFmax.setValue(0)

    def return_home(self):

        vel = -abs(self.velocidad_guardada)*2
        self.serial.send_command(f"VEL={vel}")

    def update_data(self,t,F,D,P,T):

        self.dispF.setValue(F)
        self.dispD.setValue(D)
        self.dispP.setValue(P)
        self.dispT.setValue(T)
        self.dispV.setValue(self.velocidad_guardada)

        if F > self.F_max_registrada:
            self.F_max_registrada = F

        self.dispFmax.setValue(self.F_max_registrada)

        if not self.running:
            return

        self.t_data.append(t)
        self.f_data.append(F)
        self.d_data.append(D)

        self.curve_f.setData(self.t_data,self.f_data)
        self.curve_d.setData(self.t_data,self.d_data)
        self.curve_fd.setData(self.d_data,self.f_data)

        if self.csv_writer:
            self.csv_writer.writerow([t,F,D,P,T])


if __name__ == "__main__":

    app=QtWidgets.QApplication(sys.argv)

    window=Dashboard()
    window.show()

    sys.exit(app.exec_())
