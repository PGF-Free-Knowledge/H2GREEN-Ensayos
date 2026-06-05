import sys
import random
import time
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg


class Dashboard(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema de Ensayo - Control de Fuerza")
        self.setGeometry(100, 100, 1400, 800)

        # =========================
        # VARIABLES
        # =========================
        self.running = False
        self.start_time = time.time()

        self.t_data = []
        self.f_data = []
        self.d_data = []
        self.p_data = []
        self.temp_data = []

        # =========================
        # WIDGET CENTRAL
        # =========================
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(main_layout)

        # =========================
        # GRID DE GRÁFICAS
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
        # PANEL DE CONTROL
        # =========================
        control_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(control_layout)

        self.sp_f_input = QtWidgets.QLineEdit()
        self.sp_f_input.setPlaceholderText("SP_F")

        self.sp_p_input = QtWidgets.QLineEdit()
        self.sp_p_input.setPlaceholderText("SP_P")

        self.btn_start = QtWidgets.QPushButton("INICIAR")
        self.btn_stop = QtWidgets.QPushButton("STOP")
        self.btn_reset = QtWidgets.QPushButton("RESET")

        control_layout.addWidget(self.sp_f_input)
        control_layout.addWidget(self.sp_p_input)
        control_layout.addWidget(self.btn_start)
        control_layout.addWidget(self.btn_stop)
        control_layout.addWidget(self.btn_reset)

        # =========================
        # CONEXIONES
        # =========================
        self.btn_start.clicked.connect(self.start_test)
        self.btn_stop.clicked.connect(self.stop_test)
        self.btn_reset.clicked.connect(self.reset_graphs)

        # =========================
        # TIMER ACTUALIZACIÓN
        # =========================
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(100)  # 100 ms


    def start_test(self):
        self.running = True
        self.start_time = time.time()


    def stop_test(self):
        self.running = False


    def reset_graphs(self):
        self.t_data.clear()
        self.f_data.clear()
        self.d_data.clear()
        self.p_data.clear()
        self.temp_data.clear()


    def update_data(self):

        if not self.running:
            return

        t = time.time() - self.start_time

        # Simulación temporal (luego lo reemplazamos por serial real)
        F = 20 + 5 * random.random()
        D = 10 + 2 * random.random()
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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec_())
