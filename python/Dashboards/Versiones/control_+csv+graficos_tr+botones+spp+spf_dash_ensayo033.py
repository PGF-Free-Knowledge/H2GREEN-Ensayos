import sys
import time
import serial
import numpy as np
import warnings
from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg
import csv

warnings.filterwarnings("ignore")


# =========================
# SERIAL WORKER
# =========================

class SerialWorker(QtCore.QThread):

    data_received = QtCore.pyqtSignal(float,float,float,float,float)

    def __init__(self,port="COM4",baudrate=9600):

        super().__init__()

        self.port=port
        self.baudrate=baudrate
        self.running=True
        self.ser=None

    def run(self):

        try:

            self.ser=serial.Serial(self.port,self.baudrate,timeout=1)

            time.sleep(2)

            while self.running:

                line=self.ser.readline().decode(errors='ignore').strip()

                if line.startswith("t="):

                    parts=line.split(";")

                    try:

                        t=float(parts[0].split("=")[1])
                        P=float(parts[1].split("=")[1])
                        F=float(parts[2].split("=")[1])
                        D=float(parts[3].split("=")[1])
                        T=float(parts[4].split("=")[1])

                        self.data_received.emit(t,F,D,P,T)

                    except:
                        pass

        except Exception as e:
            print("Serial error:",e)


    def send_command(self,cmd):

        if self.ser and self.ser.is_open:
            self.ser.write((cmd+"\n").encode())


    def stop(self):

        self.running=False

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

        self.setWindowTitle("Sistema Ensayo Tracción")
        self.setGeometry(100,100,1500,900)

        self.running=False

        self.velocidad_guardada=0

        self.offset_F=None
        self.offset_D=None
        self.offset_t=None

        self.Fmax=None

        self.t_data=[]
        self.f_data=[]
        self.d_data=[]
        self.p_data=[]
        self.temp_data=[]

        self.csv_file=None
        self.csv_writer=None

        tabs=QtWidgets.QTabWidget()

        self.setCentralWidget(tabs)

        self.tab_control=QtWidgets.QWidget()
        self.tab_graph=QtWidgets.QWidget()
        self.tab_system=QtWidgets.QWidget()

        tabs.addTab(self.tab_control,"Operación")
        tabs.addTab(self.tab_graph,"Gráficas")
        tabs.addTab(self.tab_system,"Sistema")

        self.build_control_tab()
        self.build_graph_tab()
        self.build_system_tab()

        self.serial=SerialWorker(port="COM4")

        self.serial.data_received.connect(self.update_data)

        self.serial.start()



# =========================
# DISPLAY DIGITAL
# =========================

    def create_display(self,title):

        layout=QtWidgets.QVBoxLayout()

        label_title=QtWidgets.QLabel(title)
        label_title.setAlignment(QtCore.Qt.AlignCenter)
        label_title.setFont(QtGui.QFont("Arial",12))

        value=QtWidgets.QLabel("0.00")
        value.setAlignment(QtCore.Qt.AlignCenter)

        value.setStyleSheet("""
        background-color:black;
        color:#00ff00;
        font-size:34px;
        font-family:Consolas;
        border-radius:8px;
        padding:10px;
        """)

        layout.addWidget(label_title)
        layout.addWidget(value)

        container=QtWidgets.QWidget()
        container.setLayout(layout)

        return container,value



# =========================
# TAB OPERACION
# =========================

    def build_control_tab(self):

        layout=QtWidgets.QVBoxLayout()

        self.tab_control.setLayout(layout)

        status_layout=QtWidgets.QHBoxLayout()

        self.status_led=QtWidgets.QLabel()
        self.status_led.setFixedSize(25,25)

        self.status_led.setStyleSheet("""
        background-color:red;
        border-radius:12px;
        border:2px solid black
        """)

        self.status_text=QtWidgets.QLabel("Ensayo detenido")

        status_layout.addWidget(self.status_led)
        status_layout.addWidget(self.status_text)
        status_layout.addStretch()

        layout.addLayout(status_layout)


        param_layout=QtWidgets.QHBoxLayout()

        self.input_vel=QtWidgets.QLineEdit()
        self.input_vel.setPlaceholderText("Velocidad")

        self.unit_box=QtWidgets.QComboBox()
        self.unit_box.addItems(["mm/s","mm/min"])

        self.btn_set_vel=QtWidgets.QPushButton("Set Velocidad")

        self.input_fmax=QtWidgets.QLineEdit()
        self.input_fmax.setPlaceholderText("Fuerza Máxima")

        param_layout.addWidget(self.input_vel)
        param_layout.addWidget(self.unit_box)
        param_layout.addWidget(self.btn_set_vel)
        param_layout.addWidget(self.input_fmax)

        layout.addLayout(param_layout)

        self.btn_set_vel.clicked.connect(self.set_velocity)


        grid=QtWidgets.QGridLayout()

        boxF,self.ind_F=self.create_display("Fuerza")
        boxD,self.ind_D=self.create_display("Desplazamiento")
        boxP,self.ind_P=self.create_display("Presión")
        boxT,self.ind_T=self.create_display("Temperatura")
        boxV,self.ind_V=self.create_display("Velocidad")

        grid.addWidget(boxF,0,0)
        grid.addWidget(boxD,0,1)
        grid.addWidget(boxP,0,2)
        grid.addWidget(boxT,1,0)
        grid.addWidget(boxV,1,1)

        layout.addLayout(grid)


        self.force_bar=QtWidgets.QProgressBar()
        self.force_bar.setMaximum(100)

        layout.addWidget(self.force_bar)


        control=QtWidgets.QHBoxLayout()

        self.btn_start=QtWidgets.QPushButton("INICIAR")
        self.btn_stop=QtWidgets.QPushButton("STOP")
        self.btn_reset=QtWidgets.QPushButton("RESET")
        self.btn_return=QtWidgets.QPushButton("RETORNAR")

        self.btn_start.setStyleSheet("background:#28a745;color:white;font-size:16px")
        self.btn_stop.setStyleSheet("background:#dc3545;color:white;font-size:16px")
        self.btn_reset.setStyleSheet("background:#ffc107;font-size:16px")
        self.btn_return.setStyleSheet("background:#6c757d;color:white;font-size:16px")

        control.addWidget(self.btn_start)
        control.addWidget(self.btn_stop)
        control.addWidget(self.btn_reset)
        control.addWidget(self.btn_return)

        layout.addLayout(control)

        self.btn_start.clicked.connect(self.start_test)
        self.btn_stop.clicked.connect(self.stop_test)
        self.btn_reset.clicked.connect(self.reset_graphs)
        self.btn_return.clicked.connect(self.return_actuator)



# =========================
# TAB GRAFICAS
# =========================

    def build_graph_tab(self):

        layout=QtWidgets.QVBoxLayout()

        self.tab_graph.setLayout(layout)

        grid=QtWidgets.QGridLayout()

        self.plot_f=pg.PlotWidget(title="Fuerza vs Tiempo")
        self.plot_d=pg.PlotWidget(title="Desplazamiento vs Tiempo")
        self.plot_p=pg.PlotWidget(title="Presión vs Tiempo")
        self.plot_t=pg.PlotWidget(title="Temperatura vs Tiempo")

        grid.addWidget(self.plot_f,0,0)
        grid.addWidget(self.plot_d,0,1)
        grid.addWidget(self.plot_p,1,0)
        grid.addWidget(self.plot_t,1,1)

        layout.addLayout(grid)

        self.plot_fd=pg.PlotWidget(title="Fuerza vs Desplazamiento")

        layout.addWidget(self.plot_fd)

        self.curve_f=self.plot_f.plot(pen='r')
        self.curve_d=self.plot_d.plot(pen='g')
        self.curve_p=self.plot_p.plot(pen='b')
        self.curve_t=self.plot_t.plot(pen='y')
        self.curve_fd=self.plot_fd.plot(pen='w')



# =========================
# TAB SISTEMA
# =========================

    def build_system_tab(self):

        layout=QtWidgets.QVBoxLayout()

        self.tab_system.setLayout(layout)

        text="""
Sistema de Ensayo de Tracción

Arquitectura:

PC
↓
Arduino Maestro
↓
Arduinos Esclavos

Sensores

Fuerza → Celda de carga + HX711
Desplazamiento → Sensor
Presión → Transductor
Temperatura → Sensor
"""

        label=QtWidgets.QLabel(text)
        label.setFont(QtGui.QFont("Arial",12))

        layout.addWidget(label)



# =========================
# VELOCIDAD
# =========================

    def set_velocity(self):

        try:

            vel=float(self.input_vel.text())

            if self.unit_box.currentText()=="mm/min":
                vel=vel/60

            self.velocidad_guardada=vel

            self.ind_V.setText(f"{vel:.3f}")

        except:
            pass



# =========================
# START
# =========================

    def start_test(self):

        self.reset_graphs()

        self.running=True

        self.status_led.setStyleSheet("background:green;border-radius:12px")

        self.status_text.setText("Ensayo en ejecución")

        try:
            self.Fmax=float(self.input_fmax.text())
        except:
            self.Fmax=None

        filename=time.strftime("ensayo_%Y%m%d_%H%M%S.csv")

        self.csv_file=open(filename,"w",newline="")

        self.csv_writer=csv.writer(self.csv_file)

        self.csv_writer.writerow(["t","F","D","P","T"])

        self.serial.send_command(f"VEL={self.velocidad_guardada}")



# =========================
# STOP
# =========================

    def stop_test(self):

        self.running=False

        self.serial.send_command("VEL=0")

        self.status_led.setStyleSheet("background:red;border-radius:12px")

        self.status_text.setText("Ensayo detenido")

        if self.csv_file:
            self.csv_file.close()



# =========================
# RETORNAR
# =========================

    def return_actuator(self):

        self.serial.send_command("VEL=-2")



# =========================
# RESET
# =========================

    def reset_graphs(self):

        self.t_data=[]
        self.f_data=[]
        self.d_data=[]
        self.p_data=[]
        self.temp_data=[]

        self.offset_F=None
        self.offset_D=None
        self.offset_t=None



# =========================
# UPDATE DATA
# =========================

    def update_data(self,t,F,D,P,T):

        if not self.running:
            return

        if self.offset_F is None:

            self.offset_F=F
            self.offset_D=D
            self.offset_t=t

        F_corr=F-self.offset_F
        D_corr=D-self.offset_D
        t_corr=t-self.offset_t

        self.ind_F.setText(f"{F_corr:.2f}")
        self.ind_D.setText(f"{D_corr:.2f}")
        self.ind_P.setText(f"{P:.2f}")
        self.ind_T.setText(f"{T:.2f}")

        self.t_data.append(t_corr)
        self.f_data.append(F_corr)
        self.d_data.append(D_corr)
        self.p_data.append(P)
        self.temp_data.append(T)

        self.curve_f.setData(self.t_data,self.f_data)
        self.curve_d.setData(self.t_data,self.d_data)
        self.curve_p.setData(self.t_data,self.p_data)
        self.curve_t.setData(self.t_data,self.temp_data)

        if len(self.d_data)>5:

            d=np.array(self.d_data)
            f=np.array(self.f_data)

            idx=np.argsort(d)

            self.curve_fd.setData(d[idx],f[idx])

        if self.csv_writer:

            self.csv_writer.writerow([t_corr,F_corr,D_corr,P,T])



# =========================
# CLOSE
# =========================

    def closeEvent(self,event):

        self.serial.stop()

        if self.csv_file:
            self.csv_file.close()

        event.accept()



# =========================
# MAIN
# =========================

if __name__=="__main__":

    app=QtWidgets.QApplication(sys.argv)

    app.setStyleSheet("""

    QMainWindow{
        background:#e9ecef;
    }

    QTabBar::tab{
        background:#d0d0d0;
        padding:8px;
        margin:2px;
        border-radius:4px;
    }

    QTabBar::tab:selected{
        background:#4a90e2;
        color:white;
    }

    """)

    window=Dashboard()
    window.show()

    sys.exit(app.exec_())
