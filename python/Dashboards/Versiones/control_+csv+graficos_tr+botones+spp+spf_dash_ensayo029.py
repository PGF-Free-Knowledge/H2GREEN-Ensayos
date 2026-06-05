import sys
import time
import serial
import numpy as np
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
import pyqtgraph.exporters
import csv

# =========================
# SERIAL THREAD
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

            print("Error serial:",e)

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

        central=QtWidgets.QWidget()
        self.setCentralWidget(central)

        main_layout=QtWidgets.QVBoxLayout()
        central.setLayout(main_layout)

        # =========================
        # TABS
        # =========================

        self.tabs=QtWidgets.QTabWidget()
        main_layout.addWidget(self.tabs)

        self.tab_operacion=QtWidgets.QWidget()
        self.tab_graficas=QtWidgets.QWidget()
        self.tab_resultados=QtWidgets.QWidget()

        self.tabs.addTab(self.tab_operacion,"Operación")
        self.tabs.addTab(self.tab_graficas,"Gráficas")
        self.tabs.addTab(self.tab_resultados,"Resultados")

        self.build_operacion()
        self.build_graficas()
        self.build_resultados()

        # SERIAL

        self.serial=SerialWorker(port="COM4")
        self.serial.data_received.connect(self.update_data)
        self.serial.start()

    # =========================
    # TAB OPERACION
    # =========================

    def build_operacion(self):

        layout=QtWidgets.QVBoxLayout()
        self.tab_operacion.setLayout(layout)

        indicadores=QtWidgets.QGridLayout()

        self.label_F=QtWidgets.QLabel("0 N")
        self.label_D=QtWidgets.QLabel("0 mm")
        self.label_P=QtWidgets.QLabel("0 bar")
        self.label_T=QtWidgets.QLabel("0 °C")

        font=self.label_F.font()
        font.setPointSize(18)

        for lbl in [self.label_F,self.label_D,self.label_P,self.label_T]:
            lbl.setFont(font)

        indicadores.addWidget(QtWidgets.QLabel("Fuerza"),0,0)
        indicadores.addWidget(self.label_F,0,1)

        indicadores.addWidget(QtWidgets.QLabel("Desplazamiento"),1,0)
        indicadores.addWidget(self.label_D,1,1)

        indicadores.addWidget(QtWidgets.QLabel("Presión"),2,0)
        indicadores.addWidget(self.label_P,2,1)

        indicadores.addWidget(QtWidgets.QLabel("Temperatura"),3,0)
        indicadores.addWidget(self.label_T,3,1)

        layout.addLayout(indicadores)

        params=QtWidgets.QHBoxLayout()

        self.input_vel=QtWidgets.QLineEdit()
        self.input_vel.setPlaceholderText("Velocidad")

        self.unit_box=QtWidgets.QComboBox()
        self.unit_box.addItems(["mm/s","mm/min"])

        self.btn_set_vel=QtWidgets.QPushButton("Set Velocidad")

        self.input_fmax=QtWidgets.QLineEdit()
        self.input_fmax.setPlaceholderText("Fuerza Max")

        params.addWidget(self.input_vel)
        params.addWidget(self.unit_box)
        params.addWidget(self.btn_set_vel)
        params.addWidget(self.input_fmax)

        layout.addLayout(params)

        self.btn_set_vel.clicked.connect(self.set_velocity)

        controles=QtWidgets.QHBoxLayout()

        self.btn_start=QtWidgets.QPushButton("INICIAR")
        self.btn_stop=QtWidgets.QPushButton("STOP")
        self.btn_reset=QtWidgets.QPushButton("RESET")
        self.btn_return=QtWidgets.QPushButton("RETORNAR")

        controles.addWidget(self.btn_start)
        controles.addWidget(self.btn_stop)
        controles.addWidget(self.btn_reset)
        controles.addWidget(self.btn_return)

        layout.addLayout(controles)

        self.btn_start.clicked.connect(self.start_test)
        self.btn_stop.clicked.connect(self.stop_test)
        self.btn_reset.clicked.connect(self.reset_graphs)
        self.btn_return.clicked.connect(self.return_actuator)

    # =========================
    # TAB GRAFICAS
    # =========================

    def build_graficas(self):

        layout=QtWidgets.QGridLayout()
        self.tab_graficas.setLayout(layout)

        self.plot_f=pg.PlotWidget(title="Fuerza vs Tiempo")
        self.plot_d=pg.PlotWidget(title="Desplazamiento vs Tiempo")
        self.plot_p=pg.PlotWidget(title="Presión vs Tiempo")
        self.plot_t=pg.PlotWidget(title="Temperatura vs Tiempo")

        layout.addWidget(self.plot_f,0,0)
        layout.addWidget(self.plot_d,0,1)
        layout.addWidget(self.plot_p,1,0)
        layout.addWidget(self.plot_t,1,1)

        self.curve_f=self.plot_f.plot(pen='r')
        self.curve_d=self.plot_d.plot(pen='g')
        self.curve_p=self.plot_p.plot(pen='b')
        self.curve_t=self.plot_t.plot(pen='y')

        self.plot_fd=pg.PlotWidget(title="Fuerza vs Desplazamiento")
        layout.addWidget(self.plot_fd,2,0,1,2)

        self.curve_fd=self.plot_fd.plot(pen='w')

    # =========================
    # TAB RESULTADOS
    # =========================

    def build_resultados(self):

        layout=QtWidgets.QVBoxLayout()
        self.tab_resultados.setLayout(layout)

        self.res_fmax=QtWidgets.QLabel("Fuerza Max: -")
        self.res_dmax=QtWidgets.QLabel("Desplazamiento Max: -")
        self.res_time=QtWidgets.QLabel("Tiempo Total: -")

        layout.addWidget(self.res_fmax)
        layout.addWidget(self.res_dmax)
        layout.addWidget(self.res_time)

    # =========================
    # VELOCIDAD
    # =========================

    def set_velocity(self):

        try:

            vel=float(self.input_vel.text())

            if self.unit_box.currentText()=="mm/min":
                vel=vel/60

            self.velocidad_guardada=vel

            print("Velocidad guardada:",vel)

        except:
            pass

    # =========================
    # START
    # =========================

    def start_test(self):

        self.reset_graphs()

        self.running=True

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

        if self.csv_file:
            self.csv_file.close()
            self.csv_file=None

        self.export_results()

    # =========================
    # EXPORTAR RESULTADOS
    # =========================

    def export_results(self):

        if len(self.f_data)==0:
            return

        fmax=max(self.f_data)
        dmax=max(self.d_data)
        tmax=max(self.t_data)

        self.res_fmax.setText(f"Fuerza Max: {fmax:.2f} N")
        self.res_dmax.setText(f"Desplazamiento Max: {dmax:.2f} mm")
        self.res_time.setText(f"Tiempo Total: {tmax:.2f} s")

        try:

            exporter=pg.exporters.ImageExporter(self.plot_fd.plotItem)

            filename=time.strftime("grafica_FD_%Y%m%d_%H%M%S.png")

            exporter.export(filename)

            print("Grafica exportada:",filename)

        except Exception as e:

            print("No se pudo exportar imagen:",e)

    # =========================
    # RETORNO
    # =========================

    def return_actuator(self):

        self.serial.send_command("VEL=-2")

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

        self.label_F.setText(f"{F:.2f} N")
        self.label_D.setText(f"{D:.2f} mm")
        self.label_P.setText(f"{P:.2f} bar")
        self.label_T.setText(f"{T:.2f} °C")

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

        self.curve_f.setData(self.t_data,self.f_data)
        self.curve_d.setData(self.t_data,self.d_data)
        self.curve_p.setData(self.t_data,self.p_data)
        self.curve_t.setData(self.t_data,self.temp_data)

        if len(self.d_data)>5:

            d=np.array(self.d_data)
            f=np.array(self.f_data)

            if np.ptp(d)>0:
                idx=np.argsort(d)
                self.curve_fd.setData(d[idx],f[idx])

        if self.Fmax and F_corr>=self.Fmax:

            print("Fuerza maxima alcanzada")
            self.stop_test()

        if self.csv_writer:
            self.csv_writer.writerow([t_corr,F_corr,D_corr,P,T])

    # =========================
    # CIERRE
    # =========================

    def closeEvent(self,event):

        self.serial.stop()

        if self.csv_file:
            self.csv_file.close()

        event.accept()


# =========================
# MAIN
# =========================

if __name__ == "__main__":

    app=QtWidgets.QApplication(sys.argv)

    window=Dashboard()
    window.show()

    sys.exit(app.exec_())
