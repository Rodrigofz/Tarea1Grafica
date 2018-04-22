"""
@author Rodrigo Fuentes
@version 1
"""

import matplotlib.pyplot as plt
import numpy as np
import math


class Corte:
    ##### CONSTRUCTOR
    def __init__(self, dh, T=0, usarRho=False, omega=0, tol=1):
        self._dh = dh
        self._alturaMar = 100

        # Ancho y largo de corte en metros
        self._alto = 2000 + self._alturaMar
        self._ancho = 4000

        # Hora del dia
        self._T = T

        # Tolerancia
        self.tol = tol

        # Ancho y largo de matriz, en puntos
        self._h = int(float(self._alto) / dh)
        self._x = int(float(self._ancho) / dh)

        # Creacion de matrices y fijacion de condiciones de borde
        self._matrix = np.ones((self._h, self._x))
        self._matrixTipos = np.zeros((self._h, self._x))
        self.fijarCondicionesBorde()

        # Omega (Si no es dado, calcula el optimo)
        if omega == 0:
            self._omega = self.w_optimo()
        else:
            self._omega = omega

        if usarRho:
            self._rho = lambda x, y: 1 / math.sqrt(x ** 2 + y ** 2 + 120)
        else:
            self._rho = lambda x, y: 0

    ################################################################
    ##### GENERACION DE TERRENO
    def primeraColumna(self):
        i = 0
        for j in range(self._alturaMar / self._dh, self._h):
            if 0 <= self._T <= 8:
                self._matrix[j][i] = 4 - 6.0 * j * self._dh / 1000

            elif self._T in range(9, 17):
                self._matrix[j][i] = 2 * self._T - 12 - 6.0 * j * self._dh / 1000

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

        # Pequenha subida
        for i in range(int(1550 / self._dh), int(1830 / self._dh)):
            for j in range(0, self._h):
                if j * self._dh > 0.33 * i * self._dh - 514.82 + self._alturaMar:
                    self._matrixTipos[j][i] = -1
                    self._matrix[j][i] = self._matrix[j][0]  ##### AIRE
                else:
                    self._matrix[j][i] = 20  #### SUELO

        # Primera montana: Subida
        for i in range(int(1830 / self._dh), int(2630 / self._dh)):
            for j in range(0, self._h):
                if j * self._dh > 1.9 * i * self._dh - 3388.58 + self._alturaMar:
                    self._matrixTipos[j][i] = -1
                    self._matrix[j][i] = self._matrix[j][0]  ##### AIRE
                else:
                    self._matrix[j][i] = 20  ##### SUELO

        # Primera montana: Bajada
        for i in range(int(2630. / self._dh), int(2930 / self._dh)):
            for j in range(0, self._h):
                if j * self._dh > -0.67 * i * self._dh + 3368.33 + self._alturaMar:
                    self._matrixTipos[j][i] = -1
                    self._matrix[j][i] = self._matrix[j][0]  ##### AIRE
                else:
                    self._matrix[j][i] = 20  ##### SUELO

        # Segunda montana: Subida
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

        # Segunda montana: Bajada
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

    ################################################################
    ##### PLOTEO
    def plot(self):
        """
        Basado en codigo de Pablo Pizarro
        Grafica
        :return: None
        """

        fig = plt.figure()
        ax = fig.add_subplot(111)

        cfg = plt.gcf()

        # Se agrega grafico al plot
        cax = ax.imshow(self._matrix, interpolation='none', vmax=100)

        # Invertir eje y
        plt.gca().invert_yaxis()

        fig.colorbar(cax)

        # Setear labels de ejes
        plt.xlabel("Ancho [celdas]")
        plt.ylabel("Altura [celdas]")

        # Setear titulo
        plt.title("Temperatura en t=" + str(int(self._T)))
        cfg.canvas.set_window_title("Temperatura en t=" + str(int(self._T)))
        plt.show()

    ################################################################
    ##### ITERACIONES: Codigo tomado del Auxiliar 3, de Pablo Pizarro
    def _single_iteration(self, matrix_new, matrix_old, omega, usarRho=False):
        for x in range(1, self._x - 1):
            for y in range(self._h - 1):
                # Valor anterior de la matriz promediado
                prom = 0
                # General
                if self._matrixTipos[y][x] == -1:
                    rho = self._rho(np.abs(x * self._dh - 1490), np.abs(y * self._dh - self._alturaMar))
                    abajo       = matrix_old[y - 1][x]
                    arriba      = matrix_old[y + 1][x]
                    izquierda   = matrix_old[y][x - 1]
                    derecha     = matrix_old[y][x + 1]
                    actual      = matrix_old[y][x]

                    prom = 0.25 * (abajo + arriba + izquierda + derecha - 4 * actual - (self._dh ** 2) * rho)

                    matrix_new[y][x] = matrix_old[y][x] + prom * omega

    @staticmethod
    def _convergio(mat_old, mat_new, tol):
        not_zero = (mat_new != 0)
        diff_relativa = (mat_old - mat_new)[not_zero]
        max_diff = np.max(np.fabs(diff_relativa))
        return [max_diff < tol, max_diff]

    def start(self):
        # Clonamos las matrices
        mat_new = np.copy(self._matrix)

        # Inicia variables
        niters = 0
        run = True
        converg = []
        omega = self._omega - 1
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
    ################################################################
