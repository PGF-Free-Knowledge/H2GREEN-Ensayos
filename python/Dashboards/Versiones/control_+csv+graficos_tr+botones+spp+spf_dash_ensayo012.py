import sys
import random
import time
import csv
import numpy as np
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg


class Dashboard(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema de Ensayo - Control de Fuerza")
        self.setGeometry(100, 100, 1500, 950)

        self.running = False
        self.start_time = time.time()

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
        # GRID SUPERIOR
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

        # =========================
        # FUERZA vs DESPLAZAMIENTO
        # =========================
        self.plot_fd = pg.PlotWidget(title="Fuerza vs Desplazamiento")
        main_layout.addWidget(self.plot_fd)

        self.plot_fd.setLabel('left', 'Fuerza')
        self.plot_fd.setLabel('bottom', 'Desplazamiento')

        self.curve_fd = self.plot_fd.plot(pen='w', symbol=None)

        # Activar zoom interactivo
        self.plot_fd.setMouseEnabled(x=True, y=True)

        # =========================
        # PANEL RESULTADOS
        # =========================
        results_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(results_layout)

        self.label_k = QtWidgets.QLabel("Rigidez (k): ---")
        self.label_fmax = QtWidgets.QLabel("Fuerza Máxima: ---")
        self.label_energy = QtWidgets.QLabel("Energía: ---")

        results_layout.addWidget(self.label_k)
        results_layout.addWidget(self.label_fmax)
        results_layout.addWidget(self.label_energy)

        # =========================
        # PANEL CONTROL
        # =========================
        control_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(control_layout)

        self.btn_start = QtWidgets.QPushButton("INICIAR")
        self.btn_stop = QtWidgets.QPushButton("STOP")
        self.btn_reset = QtWidgets.QPushButton("RESET")
        self.btn_save = QtWidgets.QPushButton("GUARDAR CSV")

        control_layout.addWidget(self.btn_start)
        control_layout.addWidget(self.btn_stop)
        control_layout.addWidget(self.btn_reset)
        control_layout.addWidget(self.btn_save)

        self.btn_start.clicked.connect(self.start_test)
        self.btn_stop.clicked.connect(self.stop_test)
        self.btn_reset.clicked.connect(self.reset_graphs)
        self.btn_save.clicked.connect(self.save_csv)

        # =========================
        # TIMER
        # =========================
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(100)


    def start_test(self):
        self.running = True
        self.start_time = time.time()


    def stop_test(self):
        self.running = False
        self.calculate_results()


    def reset_graphs(self):
        self.t_data.clear()
        self.f_data.clear()
        self.d_data.clear()
        self.p_data.clear()
        self.temp_data.clear()

        self.label_k.setText("Rigidez (k): ---")
        self.label_fmax.setText("Fuerza Máxima: ---")
        self.label_energy.setText("Energía: ---")


    def update_data(self):

        if not self.running:
            return

        t = time.time() - self.start_time

        # Simulación física tipo resorte
        D = 0.2 * t
        F = 2 * D + random.uniform(-0.3, 0.3)
        P = 20 + random.random()
        T = 25 + random.random()

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


    def calculate_results(self):

        if len(self.d_data) < 5:
            return

        d = np.array(self.d_data)
        f = np.array(self.f_data)

        # 1️⃣ Rigidez (ajuste lineal primeros 30%)
        n = int(len(d) * 0.3)
        coef = np.polyfit(d[:n], f[:n], 1)
        k = coef[0]

        # 2️⃣ Fuerza máxima
        fmax = np.max(f)

        # 3️⃣ Energía absorbida (integral)
        energy = np.trapz(f, d)

        self.label_k.setText(f"Rigidez (k): {k:.2f}")
        self.label_fmax.setText(f"Fuerza Máxima: {fmax:.2f}")
        self.label_energy.setText(f"Energía: {energy:.2f}")


    def save_csv(self):

        if len(self.t_data) == 0:
            return

        filename = time.strftime("ensayo_%Y%m%d_%H%M%S.csv")

        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Tiempo", "Fuerza", "Desplazamiento", "Presion", "Temperatura"])

            for i in range(len(self.t_data)):
                writer.writerow([
                    self.t_data[i],
                    self.f_data[i],
                    self.d_data[i],
                    self.p_data[i],
                    self.temp_data[i]
                ])

        print(f"Archivo guardado: {filename}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec_())
