"""
@author Rodrigo Fuentes
@version 1
"""

import matplotlib.pyplot as plt
import tqdm
import numpy as np


class punto:
    def __init__(self, x, h):
        self._x = x
        self._h = h
        self._tipo
        self._RRR = 575


class corte:
    def __init__(self, dh):
        # Ancho y largo de corte en metros
        self._alto = 2500
        self._ancho = 3430

        self._dh = dh

        # Ancho y largo de matriz, en puntos
        self._x = int(float(self._alto) / dh)
        self._h = int(float(self._ancho) / dh)

        self._matrix = np.ones((self._x, self._h))
        self.fijarTipoCelda()

    def mostrarDim(self):
        """
        Muestra dimensiones de la matriz
        ######################################
        ##m[0][h]                    m[x][h]##
        ##                                  ##
        ##m[0][0]                    m[x][0]##
        ######################################
        """
        # Ancho
        print len(self._matrix)
        # Largo
        print len(self._matrix[0])

    def plot(self):
        """
        Grafica
        :return: None
        """
        fig = plt.figure()
        ax = fig.add_subplot(111)

        # Se agrega grafico al plot
        cax = ax.imshow(self._matrix, interpolation='none')

        #Invertir eje y (https://stackoverflow.com/questions/2051744/reverse-y-axis-in-pyplot)
        plt.gca().invert_yaxis()

        fig.colorbar(cax)
        plt.show()

    def fijarTipoCelda(self):
        """
        Define si una celda corresponde a piso, agua, nieve o chimenea
        #Por ahora, solo diferencia piso de agua
        """
        for i in range(0, int(1550 / self._dh)):
            for j in range(0, self._alto):
                if j > 0:
                    self._matrix[j][i] = 4
                else:
                    self._matrix[j][i] = 1

        for i in range(int(1550 / self._dh), int(1830 / self._dh)):
            for j in range(0, self._alto):
                if j > (93.0 / 280) * (i - 1550):
                    self._matrix[j][i] = 4
                else:
                    self._matrix[j][i] = 10

        for i in range(int(1830 / self._dh), int(2630 / self._dh)):
            for j in range(0, self._alto):
                if j > (1522.0 / 800) * (i - 1830) + 93:
                    self._matrix[j][i] = 4
                else:
                    self._matrix[j][i] = 10

        for i in range(int(2630. / self._dh), int(2930 / self._dh)):
            for j in range(0, self._alto):
                if j > (-2.0 / 3) * (i - 2630) + 1522:
                    self._matrix[j][i] = 4
                else:
                    self._matrix[j][i] = 10

        for i in range(int(2930 / self._dh), int(3430 / self._dh)):
            for j in range(0, self._alto):
                if j > (722.5 / 500) * (i - 2930) + 1415:
                    self._matrix[j][i] = 4
                else:
                    self._matrix[j][i] = 10


c = corte(1)
c.mostrarDim()
c.plot()
