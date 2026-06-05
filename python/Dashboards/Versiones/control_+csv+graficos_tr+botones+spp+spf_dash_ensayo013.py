import sys
import time
import csv
import numpy as np
import serial
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg


# ===============================
# THREAD DE LECTURA SERIAL
# ===============================

class SerialWorker(QtCore.QThread):
    data_received = QtCore.pyqtSignal(float, float, float, float, float)

    def __init__(self, port="COM4", baudrate=9600):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.running = True

    def run(self):
        try:
            ser = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)

            while self.running:
                line = ser.readline().decode(errors='ignore').strip()

                if line.startswith("t="):

                    parts = line.split(";")

                    try:
                        P = float(parts[1].split("=")[1])
                        F = float(parts[2].split("=")[1])
                        D = float(parts[3].split("=")[1])
                        T = float(parts[5].split("=")[1])
                        t = float(parts[0].split("=")[1])

                        self.data_received.emit(t, F, D, P, T)

                    except:
                        pass

        except Exception as e:
            print("Error Serial:", e)

    def stop(self):
        self.running = False
        self.quit()
        self.wait()


# ===============================
# DASHBOARD
# ===============================

class Dashboard(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema de Ensayo - Control Real")
        self.setGeometry(100, 100, 1500, 950)

        self.running = False

        self.t_data = []
        self.f_data = []
        self.d_data = []
        self.p_data = []
        self.temp_data = []

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(main_layout)

        # ===== GRID SUPERIOR =====
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

        # ===== FUERZA vs DESPLAZAMIENTO =====
        self.plot_fd = pg.PlotWidget(title="Fuerza vs Desplazamiento")
        main_layout.addWidget(self.plot_fd)

        self.plot_fd.setLabel('left', 'Fuerza')
        self.plot_fd.setLabel('bottom', 'Desplazamiento')

        self.curve_fd = self.plot_fd.plot(pen='w')

        # ===== BOTONES =====
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

        # ===== SERIAL THREAD =====
        self.serial_thread = SerialWorker(port="COM4")
        self.serial_thread.data_received.connect(self.update_data)
        self.serial_thread.start()


    def start_test(self):
        self.running = True


    def stop_test(self):
        self.running = False


    def reset_graphs(self):
        self.t_data.clear()
        self.f_data.clear()
        self.d_data.clear()
        self.p_data.clear()
        self.temp_data.clear()


    def update_data(self, t, F, D, P, T):

        if not self.running:
            return

        self.t_data.append(t)
        self.f_data.append(F)
        self.d_data.append(D)
        self.p_data.append(P)
        self.temp_data.append(T)

        self.curve_f.setData(self.t_data, self.f_data)
        self.curve_d.setData(self.t_data, self.d_data)
        self.curve_p.setData(self.t_data, self.p_data)
        self.curve_t.setData(self.t_data, self.temp_data)
        self.curve_fd.setData(self.d_data, self.f_data)


    def closeEvent(self, event):
        self.serial_thread.stop()
        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec_())
