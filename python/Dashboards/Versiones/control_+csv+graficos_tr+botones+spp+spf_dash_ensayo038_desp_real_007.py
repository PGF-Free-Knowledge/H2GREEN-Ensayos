import sys
import time
import serial
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg

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
# SERIAL THREAD
# ===============================

class SerialWorker(QtCore.QThread):

    data_received = QtCore.pyqtSignal(float,float,float,float,float)

    def __init__(self,port="COM3",baudrate=9600):
        super().__init__()
        self.port=port
        self.baudrate=baudrate
        self.running=True
        self.ser=None

    def run(self):

        try:
            self.ser=serial.Serial(self.port,self.baudrate,timeout=0.1)
            time.sleep(2)

            while self.running:

                line=self.ser.readline().decode(errors='ignore').strip()

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

        self.setWindowTitle("Sistema Ensayo Tracción - FINAL")
        self.setGeometry(100,100,1500,900)

        self.running=False
        self.velocidad_guardada=0

        self.f_max=9999
        self.fuerza_max_historica=0

        self.t_data=[]
        self.f_data=[]
        self.d_data=[]
        self.p_data=[]
        self.temp_data=[]

        tabs=QtWidgets.QTabWidget()
        self.setCentralWidget(tabs)

        tab_op=QtWidgets.QWidget()
        tab_graph=QtWidgets.QWidget()

        tabs.addTab(tab_op,"Operación")
        tabs.addTab(tab_graph,"Gráficos")

        layout=QtWidgets.QVBoxLayout()
        tab_op.setLayout(layout)

        # TITULO
        titulo=QtWidgets.QLabel("Sistema de Ensayo Mecánico")
        titulo.setAlignment(QtCore.Qt.AlignCenter)
        titulo.setStyleSheet("font-size:20px;font-weight:bold")
        layout.addWidget(titulo)

        # CONFIG
        config=QtWidgets.QHBoxLayout()

        self.input_vel=QtWidgets.QLineEdit()
        self.input_vel.setPlaceholderText("Velocidad")

        self.unit_box=QtWidgets.QComboBox()
        self.unit_box.addItems(["mm/s","mm/min"])

        self.input_fmax=QtWidgets.QLineEdit()
        self.input_fmax.setPlaceholderText("Fuerza máxima")

        config.addWidget(self.input_vel)
        config.addWidget(self.unit_box)
        config.addWidget(self.input_fmax)

        layout.addLayout(config)

        # ESTADO
        self.estado=QtWidgets.QLabel("● DETENIDO")
        self.estado.setAlignment(QtCore.Qt.AlignCenter)
        self.estado.setStyleSheet("color:red;font-size:18px")
        layout.addWidget(self.estado)

        # DISPLAYS
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

        # BOTONES
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

        # GRAFICOS
        layout2=QtWidgets.QGridLayout()
        tab_graph.setLayout(layout2)

        self.plot_f=pg.PlotWidget(title="F vs t")
        self.plot_d=pg.PlotWidget(title="D vs t")
        self.plot_p=pg.PlotWidget(title="P vs t")
        self.plot_t=pg.PlotWidget(title="T vs t")
        self.plot_fd=pg.PlotWidget(title="F vs D")

        layout2.addWidget(self.plot_f,0,0)
        layout2.addWidget(self.plot_d,0,1)
        layout2.addWidget(self.plot_p,1,0)
        layout2.addWidget(self.plot_t,1,1)
        layout2.addWidget(self.plot_fd,2,0,1,2)

        self.curve_f=self.plot_f.plot(pen='r')
        self.curve_d=self.plot_d.plot(pen='g')
        self.curve_p=self.plot_p.plot(pen='b')
        self.curve_t=self.plot_t.plot(pen='y')
        self.curve_fd=self.plot_fd.plot(pen='w')

        # SERIAL
        self.serial=SerialWorker(port="COM3")
        self.serial.data_received.connect(self.update_data)
        self.serial.start()

        # EVENTOS
        self.btn_start.clicked.connect(self.start_test)
        self.btn_stop.clicked.connect(self.stop_test)
        self.btn_reset.clicked.connect(self.reset_test)
        self.btn_return.clicked.connect(self.return_home)

    # ===============================

    def start_test(self):

        self.running=True
        self.fuerza_max_historica=0

        self.estado.setText("● ENSAYO EN CURSO")
        self.estado.setStyleSheet("color:green")

        try:
            vel=float(self.input_vel.text())
            if self.unit_box.currentText()=="mm/min":
                vel/=60

            self.velocidad_guardada=vel
            self.serial.send_command(f"VEL={vel}")

        except:
            pass

        try:
            self.f_max=float(self.input_fmax.text())
        except:
            self.f_max=9999

    # ===============================

    def stop_test(self):

        self.running=False
        self.estado.setText("● DETENIDO")
        self.estado.setStyleSheet("color:red")

        self.serial.send_command("VEL=0")

    # ===============================

    def reset_test(self):

        self.t_data=[]
        self.f_data=[]
        self.d_data=[]
        self.p_data=[]
        self.temp_data=[]

        self.curve_f.setData([])
        self.curve_d.setData([])
        self.curve_p.setData([])
        self.curve_t.setData([])
        self.curve_fd.setData([])

        self.estado.setText("● RESET")
        self.estado.setStyleSheet("color:orange")

    # ===============================

    def return_home(self):

        velocidad_retorno = -abs(self.velocidad_guardada)*2
        self.serial.send_command(f"VEL={velocidad_retorno}")

    # ===============================

    def update_data(self,t,F,D,P,T):

        self.dispF.setValue(F)
        self.dispD.setValue(D)
        self.dispP.setValue(P)
        self.dispT.setValue(T)
        self.dispV.setValue(self.velocidad_guardada)

        if not self.running:
            return

        self.t_data.append(t)
        self.f_data.append(F)
        self.d_data.append(D)
        self.p_data.append(P)
        self.temp_data.append(T)

        self.curve_f.setData(self.t_data,self.f_data)
        self.curve_d.setData(self.t_data,self.d_data)
        self.curve_p.setData(self.t_data,self.p_data)
        self.curve_t.setData(self.t_data,self.temp_data)
        self.curve_fd.setData(self.d_data,self.f_data)

        # CORTE POR FUERZA
        if F >= self.f_max:
            self.estado.setText("⚠ CORTE POR FUERZA")
            self.serial.send_command("VEL=0")
            self.running=False

        # DETECCION ROTURA
        if F > self.fuerza_max_historica:
            self.fuerza_max_historica = F

        if self.fuerza_max_historica > 0.1:
            if F < self.fuerza_max_historica * 0.6:
                self.estado.setText("💥 ROTURA DETECTADA")
                self.serial.send_command("VEL=0")
                self.running=False


# ===============================
# MAIN
# ===============================

if __name__ == "__main__":

    app=QtWidgets.QApplication(sys.argv)

    window=Dashboard()
    window.show()

    sys.exit(app.exec_())
