import sys
import time
import serial
import numpy as np
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
            print("Error Serial:", e)


    def send_command(self, cmd):

        if self.ser and self.ser.is_open:
            self.ser.write((cmd + "\n").encode())


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

        self.setWindowTitle("Sistema de Ensayo - Control Velocidad")
        self.setGeometry(100, 100, 1500, 950)

        self.running = False

        self.offset_F = None
        self.offset_D = None
        self.offset_t = None

        self.t_data = []
        self.f_data = []
        self.d_data = []
        self.p_data = []
        self.temp_data = []

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(main_layout)

        # =========================
        # SETPOINTS
        # =========================

        sp_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(sp_layout)

        self.input_sp_p = QtWidgets.QLineEdit()
        self.input_sp_p.setPlaceholderText("SP_P")

        self.input_vel = QtWidgets.QLineEdit()
        self.input_vel.setPlaceholderText("VEL mm/s")

        self.btn_send_sp = QtWidgets.QPushButton("Enviar SP")

        sp_layout.addWidget(self.input_sp_p)
        sp_layout.addWidget(self.input_vel)
        sp_layout.addWidget(self.btn_send_sp)

        self.btn_send_sp.clicked.connect(self.send_setpoints)

        # =========================
        # GRAFICAS
        # =========================

        grid = QtWidgets.QGridLayout()
        main_layout.addLayout(grid)

        self.plot_f = pg.PlotWidget(title="Fuerza vs Tiempo")
        self.plot_d = pg.PlotWidget(title="Desplazamiento vs Tiempo")
        self.plot_p = pg.PlotWidget(title="Presión vs Tiempo")
        self.plot_t = pg.PlotWidget(title="Temperatura vs Tiempo")

        grid.addWidget(self.plot_f, 0, 0)
        grid.addWidget(self.plot_d, 0, 1)
        grid.addWidget(self.plot_p, 1, 0)
        grid.addWidget(self.plot_t, 1, 1)

        self.curve_f = self.plot_f.plot(pen='r')
        self.curve_d = self.plot_d.plot(pen='g')
        self.curve_p = self.plot_p.plot(pen='b')
        self.curve_t = self.plot_t.plot(pen='y')

        self.plot_fd = pg.PlotWidget(title="Fuerza vs Desplazamiento")
        main_layout.addWidget(self.plot_fd)

        self.curve_fd = self.plot_fd.plot(pen='w')

        # =========================
        # BOTONES
        # =========================

        control_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(control_layout)

        self.btn_start = QtWidgets.QPushButton("INICIAR")
        self.btn_stop = QtWidgets.QPushButton("STOP")
        self.btn_reset = QtWidgets.QPushButton("RESET")

        control_layout.addWidget(self.btn_start)
        control_layout.addWidget(self.btn_stop)
        control_layout.addWidget(self.btn_reset)

        self.btn_start.clicked.connect(self.start_test)
        self.btn_stop.clicked.connect(self.stop_test)
        self.btn_reset.clicked.connect(self.reset_graphs)

        # =========================
        # SERIAL
        # =========================

        self.serial_thread = SerialWorker(port="COM4")

        self.serial_thread.data_received.connect(self.update_data)

        self.serial_thread.start()


    # =========================
    # ENVIAR SETPOINTS
    # =========================

    def send_setpoints(self):

        try:
            sp_p = float(self.input_sp_p.text())
            self.serial_thread.send_command(f"SP_P={sp_p}")
        except:
            pass


    # =========================
    # START
    # =========================

    def start_test(self):

        self.reset_graphs()

        try:
            vel = float(self.input_vel.text())
            self.serial_thread.send_command(f"VEL={vel}")
        except:
            pass

        self.running = True


    # =========================
    # STOP
    # =========================

    def stop_test(self):

        self.running = False

        self.serial_thread.send_command("VEL=0")


    # =========================
    # RESET
    # =========================

    def reset_graphs(self):

        self.t_data.clear()
        self.f_data.clear()
        self.d_data.clear()
        self.p_data.clear()
        self.temp_data.clear()

        self.offset_F = None
        self.offset_D = None
        self.offset_t = None


    # =========================
    # ACTUALIZAR DATOS
    # =========================

    def update_data(self, t, F, D, P, T):

        if not self.running:
            return

        if self.offset_F is None:

            self.offset_F = F
            self.offset_D = D
            self.offset_t = t

        F_corr = F - self.offset_F
        D_corr = D - self.offset_D
        t_corr = t - self.offset_t

        self.t_data.append(t_corr)
        self.f_data.append(F_corr)
        self.d_data.append(D_corr)
        self.p_data.append(P)
        self.temp_data.append(T)

        self.curve_f.setData(self.t_data, self.f_data)
        self.curve_d.setData(self.t_data, self.d_data)
        self.curve_p.setData(self.t_data, self.p_data)
        self.curve_t.setData(self.t_data, self.temp_data)

        if len(self.d_data) > 5:

            d_array = np.array(self.d_data)
            f_array = np.array(self.f_data)

            idx = np.argsort(d_array)

            self.curve_fd.setData(d_array[idx], f_array[idx])


    # =========================
    # CERRAR
    # =========================

    def closeEvent(self, event):

        self.serial_thread.stop()

        event.accept()


# =========================
# MAIN
# =========================

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    window = Dashboard()

    window.show()

    sys.exit(app.exec_())
