"""
@author Rodrigo Fuentes
@version 1
"""

import matplotlib.pyplot as plt
import tqdm
import numpy as np
import math


class punto:
    def __init__(self, x, h):
        self._x = x
        self._h = h
        self._tipo
        self._RRR = 575


class corte:
    def __init__(self, dh, T=0):
        # Ancho y largo de corte en metros
        self._alto = 2500
        self._ancho = 4000

        self._dh = dh
        self._alturaMar = 100

        # Hora del dia
        self._T = T

        # Ancho y largo de matriz, en puntos
        self._h = int(float(self._alto) / dh)
        self._x = int(float(self._ancho) / dh)

        self._matrix = np.ones((self._h, self._x))
        self.fijarCondicionesBorde()

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

        # Invertir eje y (https://stackoverflow.com/questions/2051744/reverse-y-axis-in-pyplot)
        plt.gca().invert_yaxis()

        fig.colorbar(cax)
        plt.show()

    def fijarCondicionesBorde(self):
        """
        Fija las condiciones de borde
        """

        # Tramo 1, arriba: Aire; #abajo: Mar hasta cierta distancia
        for i in range(0, int(1430 / self._dh)):
            for j in range(0, self._h):
                if j > self._alturaMar:
                    self._matrix[j][i] = 100 #### AIRE
                else:
                    if 0 <= self._T <= 8:
                        self._matrix[j][i] = 4 #### AGUA

                    elif self._T in range(9, 17):
                        self._matrix[j][i] = 2 * self._T - 12 #### AGUA

                    else:
                        self._matrix[j][i] = -2 * self._T + 52 #### AGUA

        # Chimeneas
        for i in range(int(1430 / self._dh), int(1550 / self._dh)):
            for j in range(0, self._h):
                if j > self._alturaMar:
                    self._matrix[j][i] = 100 #### AIRE
                elif j <= self._alturaMar:
                    self._matrix[j][i] = 450*(math.cos(3.14*self._T/12)+2) ##### CHIMENEAS


        # Tramo 2, arriba: Aire; #abajo: Terreno;
        for i in range(int(1550 / self._dh), int(1830 / self._dh)):
            for j in range(0, self._h):
                if j > 0.33 * i - 514.82 + self._alturaMar:
                    self._matrix[j][i] = 100 ##### AIRE
                else:
                    self._matrix[j][i] = 10 #### SUELO

        # Primera montana
        for i in range(int(1830 / self._dh), int(2630 / self._dh)):
            for j in range(0, self._h):
                if j > 1.9 * i - 3388.58 + self._alturaMar:
                    self._matrix[j][i] = 100 ##### AIRE
                else:
                    self._matrix[j][i] = 10 ##### SUELO

        # Primera montana
        for i in range(int(2630. / self._dh), int(2930 / self._dh)):
            for j in range(0, self._h):
                if j > -0.67 * i + 3368.33 + self._alturaMar:
                    self._matrix[j][i] = 100 ##### AIRE
                else:
                    self._matrix[j][i] = 10 ##### SUELO

        # Segunda montana
        for i in range(int(2930 / self._dh), int(3430 / self._dh)):
            for j in range(0, self._h):
                if j > 0.99 * i - 1471.05 + self._alturaMar:
                    self._matrix[j][i] = 100
                else:
                    if j > self._alturaMar + 1800:
                        self._matrix[j][i] = 0  ##### NIEVE
                    else:
                        self._matrix[j][i] = 10 ##### SUELO

        # Segunda montana
        for i in range(int(3430 / self._dh), int(4000 / self._dh)):
            for j in range(0, self._h):
                if j > -0.95 * i + 0.95 * 3430 + 1909.5 + self._alturaMar:
                    self._matrix[j][i] = 100 ##### AIRE
                else:
                    if j > self._alturaMar + 1800:
                        self._matrix[j][i] = 0 ##### NIEVE
                    else:
                        self._matrix[j][i] = 10 ##### SUELO


c = corte(1, 13)
c.mostrarDim()
c.plot()
