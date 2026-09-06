import csv


class SimuladorProbeta:

    def __init__(self):

        self.datos = []
        self.indice = 0


    def cargar(self, archivo):

        self.datos = []

        with open(archivo, newline="") as f:

            lector = csv.reader(f)

            next(lector)

            for fila in lector:

                self.datos.append(fila)

        self.indice = 0


    def siguiente(self):

        if self.indice >= len(self.datos):

            return None

        fila = self.datos[self.indice]

        self.indice += 1

        return fila