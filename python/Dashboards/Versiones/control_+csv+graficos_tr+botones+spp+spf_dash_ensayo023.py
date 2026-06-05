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

        self.setWindowTitle("Sistema de Ensayo - Dashboard PRO")
        self.setGeometry(100,100,1600,950)

        self.running=False

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
# PANEL CONTROL
# =========================

        control=QtWidgets.QGridLayout()
        main_layout.addLayout(control)


        self.test_name=QtWidgets.QLineEdit()
        self.test_name.setPlaceholderText("Nombre ensayo")

        self.input_vel=QtWidgets.QLineEdit()
        self.input_vel.setPlaceholderText("Velocidad")

        self.unit_box=QtWidgets.QComboBox()
        self.unit_box.addItems(["mm/s","mm/min"])

        self.input_fmax=QtWidgets.QLineEdit()
        self.input_fmax.setPlaceholderText("Fuerza máxima (kN)")


        self.btn_set_vel=QtWidgets.QPushButton("Set Velocidad")


        control.addWidget(QtWidgets.QLabel("Ensayo"),0,0)
        control.addWidget(self.test_name,0,1)

        control.addWidget(QtWidgets.QLabel("Velocidad"),0,2)
        control.addWidget(self.input_vel,0,3)

        control.addWidget(self.unit_box,0,4)

        control.addWidget(self.btn_set_vel,0,5)

        control.addWidget(QtWidgets.QLabel("Fmax"),0,6)
        control.addWidget(self.input_fmax,0,7)



# =========================
# INDICADORES
# =========================

        indicators=QtWidgets.QHBoxLayout()
        main_layout.addLayout(indicators)

        self.lblF=QtWidgets.QLabel("F = 0")
        self.lblD=QtWidgets.QLabel("D = 0")
        self.lblP=QtWidgets.QLabel("P = 0")
        self.lblT=QtWidgets.QLabel("T = 0")

        indicators.addWidget(self.lblF)
        indicators.addWidget(self.lblD)
        indicators.addWidget(self.lblP)
        indicators.addWidget(self.lblT)



# =========================
# GRÁFICAS
# =========================

        grid=QtWidgets.QGridLayout()
        main_layout.addLayout(grid)

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
        main_layout.addWidget(self.plot_fd)

        self.curve_fd=self.plot_fd.plot(pen='w')



# =========================
# BOTONES
# =========================

        buttons=QtWidgets.QHBoxLayout()
        main_layout.addLayout(buttons)

        self.btn_start=QtWidgets.QPushButton("INICIAR")
        self.btn_stop=QtWidgets.QPushButton("STOP")
        self.btn_reset=QtWidgets.QPushButton("RESET")

        buttons.addWidget(self.btn_start)
        buttons.addWidget(self.btn_stop)
        buttons.addWidget(self.btn_reset)



# =========================
# SERIAL
# =========================

        self.serial=SerialWorker("COM4")

        self.serial.data_received.connect(self.update_data)

        self.serial.start()



# =========================
# EVENTOS
# =========================

        self.btn_set_vel.clicked.connect(self.send_velocity)
        self.btn_start.clicked.connect(self.start_test)
        self.btn_stop.clicked.connect(self.stop_test)
        self.btn_reset.clicked.connect(self.reset_graphs)



# =========================
# VELOCIDAD
# =========================

    def send_velocity(self):

        try:

            vel=float(self.input_vel.text())

            if self.unit_box.currentText()=="mm/min":

                vel=vel/60

            self.serial.send_command(f"VEL={vel}")

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

        name=self.test_name.text()

        if name=="":
            name="ensayo"

        filename=name+"_"+time.strftime("%Y%m%d_%H%M%S")+".csv"

        self.csv_file=open(filename,"w",newline="")
        self.csv_writer=csv.writer(self.csv_file)

        self.csv_writer.writerow(["t","F","D","P","T"])



# =========================
# STOP
# =========================

    def stop_test(self):

        self.running=False

        self.serial.send_command("VEL=0")

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
# UPDATE
# =========================

    def update_data(self,t,F,D,P,T):

        if not self.running:
            return


        if self.offset_F is None:

            self.offset_F=F
            self.offset_D=D
            self.offset_t=t


        F=F-self.offset_F
        D=D-self.offset_D
        t=t-self.offset_t


        self.lblF.setText(f"F = {F:.2f}")
        self.lblD.setText(f"D = {D:.2f}")
        self.lblP.setText(f"P = {P:.2f}")
        self.lblT.setText(f"T = {T:.2f}")


        if self.Fmax and F>self.Fmax:

            print("Fuerza máxima alcanzada")

            self.stop_test()
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


        if len(self.d_data)>5:

            d=np.array(self.d_data)
            f=np.array(self.f_data)

            idx=np.argsort(d)

            self.curve_fd.setData(d[idx],f[idx])


        if self.csv_writer:

            self.csv_writer.writerow([t,F,D,P,T])



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

    window=Dashboard()

    window.show()

    sys.exit(app.exec_())
