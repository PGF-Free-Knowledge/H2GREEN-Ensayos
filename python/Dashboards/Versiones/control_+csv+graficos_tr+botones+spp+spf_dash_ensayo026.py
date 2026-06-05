import sys
import time
import serial
import numpy as np
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
import pyqtgraph.exporters
import csv
import os


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
        self.setGeometry(100,100,1500,950)

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

        if not os.path.exists("ensayos"):
            os.makedirs("ensayos")

        central=QtWidgets.QWidget()
        self.setCentralWidget(central)

        layout=QtWidgets.QVBoxLayout()
        central.setLayout(layout)

        # =========================
        # PARAMETROS
        # =========================

        param_layout=QtWidgets.QHBoxLayout()
        layout.addLayout(param_layout)

        self.input_vel=QtWidgets.QLineEdit()
        self.input_vel.setPlaceholderText("Velocidad")

        self.unit_box=QtWidgets.QComboBox()
        self.unit_box.addItems(["mm/s","mm/min"])

        self.btn_set_vel=QtWidgets.QPushButton("Set Velocidad")

        self.input_fmax=QtWidgets.QLineEdit()
        self.input_fmax.setPlaceholderText("Fuerza Max")

        param_layout.addWidget(self.input_vel)
        param_layout.addWidget(self.unit_box)
        param_layout.addWidget(self.btn_set_vel)
        param_layout.addWidget(self.input_fmax)

        self.btn_set_vel.clicked.connect(self.set_velocity)

        # =========================
        # RESULTADOS
        # =========================

        result_layout=QtWidgets.QHBoxLayout()
        layout.addLayout(result_layout)

        self.label_fmax=QtWidgets.QLabel("Fuerza Max: ---")
        self.label_rigidez=QtWidgets.QLabel("Rigidez: ---")

        result_layout.addWidget(self.label_fmax)
        result_layout.addWidget(self.label_rigidez)

        # =========================
        # GRAFICAS
        # =========================

        grid=QtWidgets.QGridLayout()
        layout.addLayout(grid)

        self.plot_f=pg.PlotWidget(title="Fuerza vs Tiempo")
        self.plot_d=pg.PlotWidget(title="Desplazamiento vs Tiempo")
        self.plot_p=pg.PlotWidget(title="Presión vs Tiempo")
        self.plot_t=pg.PlotWidget(title="Temperatura vs Tiempo")

        grid.addWidget(self.plot_f,0,0)
        grid.addWidget(self.plot_d,0,1)
        grid.addWidget(self.plot_p,1,0)
        grid.addWidget(self.plot_t,1,1)

        self.curve_f=self.plot_f.plot(pen='r')
        self.curve_d=self.plot_d.plot(pen='g')
        self.curve_p=self.plot_p.plot(pen='b')
        self.curve_t=self.plot_t.plot(pen='y')

        self.plot_fd=pg.PlotWidget(title="Fuerza vs Desplazamiento")
        layout.addWidget(self.plot_fd)

        self.curve_fd=self.plot_fd.plot(pen='w')

        # =========================
        # BOTONES
        # =========================

        control=QtWidgets.QHBoxLayout()
        layout.addLayout(control)

        self.btn_start=QtWidgets.QPushButton("INICIAR")
        self.btn_stop=QtWidgets.QPushButton("STOP")
        self.btn_reset=QtWidgets.QPushButton("RESET")
        self.btn_return=QtWidgets.QPushButton("RETORNAR")

        control.addWidget(self.btn_start)
        control.addWidget(self.btn_stop)
        control.addWidget(self.btn_reset)
        control.addWidget(self.btn_return)

        self.btn_start.clicked.connect(self.start_test)
        self.btn_stop.clicked.connect(self.stop_test)
        self.btn_reset.clicked.connect(self.reset_graphs)
        self.btn_return.clicked.connect(self.return_actuator)

        # =========================
        # SERIAL
        # =========================

        self.serial=SerialWorker(port="COM4")
        self.serial.data_received.connect(self.update_data)
        self.serial.start()


    def set_velocity(self):

        try:

            vel=float(self.input_vel.text())

            if self.unit_box.currentText()=="mm/min":
                vel=vel/60

            self.velocidad_guardada=vel

            print("Velocidad guardada:",vel)

        except:
            pass


    def start_test(self):

        self.reset_graphs()

        self.running=True

        try:
            self.Fmax=float(self.input_fmax.text())
        except:
            self.Fmax=None

        filename="ensayos/ensayo_"+time.strftime("%Y%m%d_%H%M%S")+".csv"

        self.csv_file=open(filename,"w",newline="")
        self.csv_writer=csv.writer(self.csv_file)

        self.csv_writer.writerow(["t","F","D","P","T"])

        print("Archivo creado:",filename)

        self.serial.send_command(f"VEL={self.velocidad_guardada}")


    def stop_test(self):

        self.running=False

        self.serial.send_command("VEL=0")

        if self.csv_file:
            self.csv_file.close()
            self.csv_file=None

        self.export_results()


    def return_actuator(self):

        self.serial.send_command("VEL=-2")


    def reset_graphs(self):

        self.t_data.clear()
        self.f_data.clear()
        self.d_data.clear()
        self.p_data.clear()
        self.temp_data.clear()

        self.offset_F=None
        self.offset_D=None
        self.offset_t=None


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

        if self.Fmax and F_corr>=self.Fmax:

            print("Fuerza maxima alcanzada")

            self.label_fmax.setText(f"Fuerza Max: {round(F_corr,2)}")

            self.stop_test()

        if self.csv_writer:

            self.csv_writer.writerow([t_corr,F_corr,D_corr,P,T])


    def export_results(self):

    # Verificar cantidad mínima de datos
        if len(self.d_data) < 20:
            return

        try:

            d = np.array(self.d_data)
            f = np.array(self.f_data)

            n = min(30, len(d))

            coef = np.polyfit(d[:n], f[:n], 1)

            rigidez = coef[0]

            self.label_rigidez.setText(f"Rigidez: {round(rigidez,2)} N/mm")
        
        except:

            print("No se pudo calcular rigidez:")
    
        try:

            exporter = pyqtgraph.exporters.ImageExporter(self.plot_fd.plotItem)

            nombre = "ensayos/curva_FD_" + time.strftime("%Y%m%d_%H%M%S") + ".png"

            exporter.export(nombre)

            print("Curva exportada:", nombre)

        except Exception as e:

            print("Error exportando imagen:", e)

#.....
    def closeEvent(self,event):

        self.serial.stop()

        if self.csv_file:
            self.csv_file.close()

        event.accept()


if __name__=="__main__":

    app=QtWidgets.QApplication(sys.argv)

    window=Dashboard()
    window.show()

    sys.exit(app.exec_())
