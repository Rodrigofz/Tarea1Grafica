"""
@author Rodrigo Fuentes
@version 1
"""

import matplotlib.pyplot as plt
import tqdm
import numpy as np
import math


class corte:
    def __init__(self, dh, T=0):
        # Ancho y largo de corte en metros
        self._alto = 2500
        self._ancho = 4000

        self._dh = dh
        self._alturaMar = 100

        # Hora del dia
        self._T = T

        self.tol = 1

        # Ancho y largo de matriz, en puntos
        self._h = int(float(self._alto) / dh)
        self._x = int(float(self._ancho) / dh)

        self._matrix = np.ones((self._h, self._x))
        self._matrixTipos = np.zeros((self._h, self._x))
        self.fijarCondicionesBorde()

        # Omega
        self._omega = self.w_optimo()
        print self._omega

        self._rho = lambda x, y: 1 / math.sqrt(x ** 2 + y ** 2 + 120)

    def plot(self):
        """
        Basado en codigo de Pablo Pizarro
        Grafica
        :return: None
        """
        fig = plt.figure()
        ax = fig.add_subplot(111)

        # Se agrega grafico al plot
        cax = ax.imshow(self._matrix, interpolation='none', vmax = 100)

        # Invertir eje y (https://stackoverflow.com/questions/2051744/reverse-y-axis-in-pyplot)
        plt.gca().invert_yaxis()

        fig.colorbar(cax)
        plt.show()

    def primeraColumna(self):
        i = 0
        for j in range(0, self._h):
            if 0 <= self._T <= 8:
                self._matrix[j][i] = 4 - 6.0 * j * self._dh / 1000

            elif self._T in range(9, 17):
                self._matrix[j][i] = 2 * self._T - 12 - 6.0 * j * self._dh/ 1000

            else:
                self._matrix[j][i] = -2 * self._T + 52 - 6.0 * j * self._dh / 1000

    def fijarCondicionesBorde(self):
        """
        Fija las condiciones de borde
        """

        self.primeraColumna()

        # Mar
        for i in range(0, int(1430 / self._dh)):
            for j in range(0, self._h):
                if j * self._dh > self._alturaMar:
                    self._matrixTipos[j][i] = -1
                    self._matrix[j][i] = self._matrix[j][0]  #### AIRE
                else:
                    if 0 <= self._T <= 8:
                        self._matrix[j][i] = 4  #### AGUA

                    elif self._T in range(9, 17):
                        self._matrix[j][i] = 2 * self._T - 12  #### AGUA

                    else:
                        self._matrix[j][i] = -2 * self._T + 52  #### AGUA

        # Chimeneas
        for i in range(int(1430 / self._dh), int(1550 / self._dh)):
            for j in range(0, self._h):
                if j * self._dh > self._alturaMar:
                    self._matrixTipos[j][i] = -1
                    self._matrix[j][i] = self._matrix[j][0]  #### AIRE
                else:
                    self._matrix[j][i] = 450 * (math.cos(3.14 * self._T / 12) + 2)  #### CHIMENEAS

        # Tramo 2, arriba: Aire; #abajo: Terreno;
        for i in range(int(1550 / self._dh), int(1830 / self._dh)):
            for j in range(0, self._h):
                if j * self._dh > 0.33 * i * self._dh - 514.82 + self._alturaMar:
                    self._matrixTipos[j][i] = -1
                    self._matrix[j][i] = self._matrix[j][0]  ##### AIRE
                else:
                    self._matrix[j][i] = 20  #### SUELO

        # Primera montana
        for i in range(int(1830 / self._dh), int(2630 / self._dh)):
            for j in range(0, self._h):
                if j * self._dh > 1.9 * i * self._dh - 3388.58 + self._alturaMar:
                    self._matrixTipos[j][i] = -1
                    self._matrix[j][i] = self._matrix[j][0]  ##### AIRE
                else:
                    self._matrix[j][i] = 20  ##### SUELO

        # Primera montana
        for i in range(int(2630. / self._dh), int(2930 / self._dh)):
            for j in range(0, self._h):
                if j * self._dh > -0.67 * i * self._dh + 3368.33 + self._alturaMar:
                    self._matrixTipos[j][i] = -1
                    self._matrix[j][i] = self._matrix[j][0]  ##### AIRE
                else:
                    self._matrix[j][i] = 20  ##### SUELO

        # Segunda montana
        for i in range(int(2930 / self._dh), int(3430 / self._dh)):
            for j in range(0, self._h):
                if j * self._dh > 0.99 * i * self._dh - 1471.05 + self._alturaMar:
                    self._matrixTipos[j][i] = -1
                    self._matrix[j][i] = self._matrix[j][0]  #### AIRE
                else:
                    if j * self._dh > self._alturaMar + 1800:
                        self._matrix[j][i] = 0  ##### NIEVE
                    else:
                        self._matrix[j][i] = 20  ##### SUELO

        # Segunda montana
        for i in range(int(3430 / self._dh), int(4000 / self._dh)):
            for j in range(0, self._h):
                if j * self._dh > -0.95 * i * self._dh + 0.95 * 3430 + 1909.5 + self._alturaMar:
                    self._matrixTipos[j][i] = -1
                    self._matrix[j][i] = self._matrix[j][0]  ##### AIRE
                else:
                    if j * self._dh > self._alturaMar + 1800:
                        self._matrix[j][i] = 0  ##### NIEVE
                    else:
                        self._matrix[j][i] = 20  ##### SUELO

    def iterar(self):
        maxR = 1009999999999999999999999999
        while np.abs(maxR) > 0.01:
            mat = np.copy(self._matrix)
            maxRlocal = 0
            for i in range(1, self._x - 1):
                for j in range(1, self._h - 1):
                    if self._matrixTipos[j][i] == -1:
                        distPlantaX = np.abs(i * self._dh - 1490)
                        distPlantaY = np.abs(j * self._dh - self._alturaMar)
                        rho = self._rho(distPlantaX, distPlantaY)

                        r = 0.25 * (mat[j - 1][i] + mat[j + 1][i] + mat[j][i + 1] + mat[j][i - 1] + 4 * mat[j][i]) #- (self._dh ** 2) * rho )

                        self._matrix[j][i] = mat[j][i] + self._omega * r

                        maxRlocal = max(maxRlocal, r)

            maxR = min(maxR,maxRlocal)
            print maxR




    """
    def iterar(self):
        for _ in tqdm.tqdm(range(1000)):
            for i in range(1, self._x - 1):
                for j in range(1, self._h - 1):
                    if self._matrixTipos[j][i] == -1:
                        self._matrix[j][i] = self._omega * 0.25 * (
                                self._matrix[j - 1][i] + self._matrix[j + 1][i] + self._matrix[j][i + 1] +
                                self._matrix[j][i - 1] - self._dh ** 2 * self._rho(np.abs(i * self._dh - 1490), np.abs(
                            j * self._dh - self._alturaMar)))
    """

    def _single_iteration(self, matrix_new, matrix_old, omega):
        for x in range(1, self._x - 1):
            for y in range(self._h - 1):
                # Valor anterior de la matriz promediado
                prom = 0
                # General
                if self._matrixTipos[y][x] == -1:
                    prom = 0.25 * (matrix_old[y - 1][x] + matrix_old[y + 1][x] + matrix_old[y][x - 1] +
                                   matrix_old[y][x + 1] - 4 * matrix_old[y][x] - (self._dh ** 2) * self._rho(np.abs(x * self._dh - 1490), np.abs(
                           y * self._dh - self._alturaMar)))

                    matrix_new[y][x] = matrix_old[y][x] + prom * omega

    """
    #@staticmethod
    def _convergio(self, mat_old, mat_new, tol):
        not_zero = (mat_new != 0)
        diff_relativa = np.zeros((self._h, self._x))
        for x in range(1, self._x - 1):
            for y in range(self._h - 1):
                if self._matrixTipos[y][x] == -1:
                    diff_relativa[y][x] = mat_old[y][x] - mat_new[y][x]
                else:
                    diff_relativa[y][x] = 0

        max_diff = np.max(np.fabs(diff_relativa))
        print max_diff
        return [max_diff < tol, max_diff]
    """

    @staticmethod
    def _convergio(mat_old, mat_new, tol):
        not_zero = (mat_new != 0)
        diff_relativa = (mat_old - mat_new)[not_zero]
        max_diff = np.max(np.fabs(diff_relativa))
        return [max_diff < tol, max_diff]

    def start(self, omega):
        # Clonamos las matrices
        mat_new = np.copy(self._matrix)

        # Inicia variables
        niters = 0
        run = True
        converg = []
        omega = omega - 1
        if not 0 <= omega <= 1:
            raise Exception('Omega tiene un valor incorrecto')

        while run:
            mat_old = np.copy(mat_new)
            self._single_iteration(mat_new, mat_old, omega)
            niters += 1
            converg = self._convergio(mat_old, mat_new, self.tol)
            run = not converg[0]

        print 'El programa termino en {0} iteraciones, con error {1}'.format(niters, converg[1])
        self._matrix = np.copy(mat_new)
        return niters

    def w_optimo(self):
        """
        Retorna el w optimo
        :return:
        """

        def createw(n, m):
            return 4 / (2 + (math.sqrt(4 - (math.cos(math.pi / (n - 1)) + math.cos(math.pi / (m - 1))) ** 2)))

        return createw(self._x, self._h)


c = corte(20, 0)
#c.iterar()
c.start(c._omega)
c.plot()
