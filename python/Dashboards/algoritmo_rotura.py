# ==========================================================
# ALGORITMO DE DETECCIÓN DE ROTURA
# Máquina de Ensayos H2GREEN
# Universidad Técnica Federico Santa María
# ==========================================================


class AlgoritmoRotura:

    def __init__(self):

        self.reiniciar()


    def reiniciar(self):

        self.fuerza_maxima = 0.0
        self.rotura_detectada = False
        self.contador_caida = 0


    def actualizar(self, F):

        return False