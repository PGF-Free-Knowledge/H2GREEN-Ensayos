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

        self.setWindowTitle("Sistema Ensayo Tracción")
        self.setGeometry(100,100,1500,900)

        self.running=False
        self.velocidad_guardada=0

        self.fuerza_max = 0
        self.ventana_rotura = []
        self.rotura_activa = False
        self.muestras_minimas = 20

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

        titulo=QtWidgets.QLabel("Sistema de Ensayo Mecánico Servo-Controlado")
        titulo.setStyleSheet("font-size:20px;font-weight:bold")
        titulo.setAlignment(QtCore.Qt.AlignCenter)

        layout.addWidget(titulo)

        # CONFIGURACION
        config_box=QtWidgets.QGroupBox("Configuración del ensayo")
        config_layout=QtWidgets.QHBoxLayout()

        self.input_vel=QtWidgets.QLineEdit()
        self.input_vel.setPlaceholderText("Velocidad")

        self.unit_box=QtWidgets.QComboBox()
        self.unit_box.addItems(["mm/s","mm/min"])

        self.input_fmax=QtWidgets.QLineEdit()
        self.input_fmax.setPlaceholderText("Fuerza máxima")

        self.input_file=QtWidgets.QLineEdit()
        self.input_file.setPlaceholderText("Nombre archivo")

        config_layout.addWidget(self.input_vel)
        config_layout.addWidget(self.unit_box)
        config_layout.addWidget(self.input_fmax)
        config_layout.addWidget(self.input_file)

        config_box.setLayout(config_layout)
        layout.addWidget(config_box)

        # ESTADO
        self.estado=QtWidgets.QLabel("● DETENIDO")
        self.estado.setAlignment(QtCore.Qt.AlignCenter)
        self.estado.setStyleSheet("font-size:18px;color:red")

        layout.addWidget(self.estado)

        # VARIABLES
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

        botones.addWidget(self.btn_start)
        botones.addWidget(self.btn_stop)

        layout.addLayout(botones)

        # GRAFICOS
        layout2=QtWidgets.QGridLayout()
        tab_graficos.setLayout(layout2)

        self.plot_f=pg.PlotWidget(title="Fuerza vs Tiempo")
        self.plot_d=pg.PlotWidget(title="Desplazamiento vs Tiempo")
        self.plot_p=pg.PlotWidget(title="Presión vs Tiempo")
        self.plot_t=pg.PlotWidget(title="Temperatura vs Tiempo")
        self.plot_fd=pg.PlotWidget(title="Fuerza vs Desplazamiento")

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

        self.btn_start.clicked.connect(self.start_test)
        self.btn_stop.clicked.connect(self.stop_test)

    # ===============================

    def start_test(self):

        self.running=True
        self.rotura_activa=False
        self.ventana_rotura=[]

        self.estado.setText("● ENSAYO EN CURSO")
        self.estado.setStyleSheet("font-size:18px;color:green")

        try:
            vel=float(self.input_vel.text())

            if self.unit_box.currentText()=="mm/min":
                vel=vel/60

            self.velocidad_guardada=vel
            self.serial.send_command(f"VEL={vel}")

        except:
            pass

        try:
            self.fuerza_max=float(self.input_fmax.text())
        except:
            self.fuerza_max=0

        filename=self.input_file.text()
        if filename=="":
            filename=time.strftime("ensayo_%Y%m%d_%H%M%S")

        self.csv_file=open(filename+".csv","w",newline="")
        self.csv_writer=csv.writer(self.csv_file)
        self.csv_writer.writerow(["t","F","D","P","T"])

    # ===============================

    def stop_test(self):

        self.running=False

        self.estado.setText("● DETENIDO")
        self.estado.setStyleSheet("font-size:18px;color:red")

        self.serial.send_command("VEL=0")

        if self.csv_file:
            self.csv_file.close()

    # ===============================

    def update_data(self,t,F,D,P,T):

        self.dispF.setValue(F)
        self.dispD.setValue(D)
        self.dispP.setValue(P)
        self.dispT.setValue(T)
        self.dispV.setValue(self.velocidad_guardada)

        if not self.running:
            return

        # ---- CORTE POR FUERZA ----
        if self.fuerza_max > 0 and F >= self.fuerza_max:
            self.stop_test()
            self.estado.setText("● DETENIDO POR FUERZA MAX")
            return

        # ---- DETECCION ROTURA ----
        self.ventana_rotura.append(F)

        if len(self.ventana_rotura) > 10:
            self.ventana_rotura.pop(0)

        if len(self.f_data) > self.muestras_minimas:

            promedio = sum(self.ventana_rotura)/len(self.ventana_rotura)

            if promedio > 0.05:
                if F < promedio * 0.6:
                    self.stop_test()
                    self.estado.setText("● ROTURA DETECTADA")
                    return

        # ---- GUARDAR ----
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

        if self.csv_writer:
            self.csv_writer.writerow([t,F,D,P,T])


# ===============================
# MAIN
# ===============================

if __name__ == "__main__":

    app=QtWidgets.QApplication(sys.argv)

    window=Dashboard()
    window.show()

    sys.exit(app.exec_())
