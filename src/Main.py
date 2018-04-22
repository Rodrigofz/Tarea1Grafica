import Corte as cor
import matplotlib.pyplot as plt
import numpy as np

"""
@author: Rodrigo Fuentes
"""

class Main:
    def __init__(self):
        self._tol = 0.1
        self._dh = 20

    def modeloSinIterar(self, dh = 20, t = 0, usarRho = False, omega = 0, tol = 0.1):
        c = cor.Corte(dh, t, usarRho, omega, tol)
        c.plot()

    def modeloConIterar(self, dh = 20, t = 0, usarRho = False, omega = 0, tol = 0.1 ):
        c = cor.Corte(dh, t, usarRho, omega, tol)
        c.start()
        c.plot()

    # Requerimientos: Parte 3
    def reqParte3(self):
        listaTiempos = [0, 8, 12, 16, 20]

        # Cuado omega es cero, la clase corte busca el optimo con la formula vista
        listaOmegas = [1.2, 1.4, 1.6, 1.8, 0]

        # Para graficar
        ejeX = []
        ejeY = []

        for t in listaTiempos:
            # Decidi explorar distintos omegas para un mismo tiempo. Hacerlo para cada
            # uno era demasiado tiempo y muchos graficos.
            # Para los demas tiempos se calcula el omega optimo
            if t == 12:
                for w in listaOmegas:
                    print 'Tiempo: ' + str(t) + ', Omega: ' + str(w)
                    c = cor.Corte(self._dh, T=t, omega=w, tol=self._tol)
                    tiempoEjecucion = c.start()

                    # Para graficar numero de iteraciones
                    ejeX.append(c._omega)
                    ejeY.append(tiempoEjecucion)

                    c.plot()

                plt.plot(ejeX, ejeY)
                plt.title("Numero de iteraciones para distintos valores de omega")
                plt.xlabel("Omega")
                plt.ylabel("Numero de iteraciones")
                plt.show()

            else:
                print 'Tiempo: ' + str(t)
                c = cor.Corte(self._dh, T=t, tol=self._tol)
                c.start()
                c.plot()

    # Requerimientos: Parte 4
    def reqParte4(self):
        listaTiempos = [0, 8, 12, 16, 20]

        # Se probaran estos tiempos solo con el omega optimo
        omega = 0

        for t in listaTiempos:
            c = cor.Corte(self._dh, T=t, tol=self._tol, usarRho=True, omega=omega)
            print "Tiempo: " + str(t) + ", Omega: " + str(c._omega)
            c.start()
            c.plot()

    def temperaturasMedias(self, usarRho = False):
        listaTiempos = [0, 8, 12, 16, 20]
        listaTemperaturas = []

        for t in listaTiempos:
            print str(t)
            c = cor.Corte(self._dh, T=t,usarRho= usarRho, tol=self._tol)
            c.start()
            listaT = []
            for i in range(len(c._matrix[0]) - 1):
                for j in range(len(c._matrix) - 1):
                    if c._matrixTipos[j][i] == -1:
                        listaT.append(c._matrix[j][i])
            media = np.median(listaT)
            listaTemperaturas.append(media)

        plt.xlabel("Tiempo [horas]")
        plt.ylabel("Temperatura media [grados Celsius]")
        plt.title("Temperatura media para diferentes horas")
        plt.plot(listaTiempos, listaTemperaturas)
        plt.show()

    def temperaturasMediasLocales(self, distMaxima = 300, usarRho = False):
        listaTiempos = [0, 8, 12, 16, 20]
        listaTemperaturas = []

        for t in listaTiempos:
            print str(t)
            c = cor.Corte(self._dh, T=t, usarRho=usarRho, tol=self._tol)
            c.start()
            listaT = []
            for i in range(len(c._matrix[0]) - 1):
                for j in range(len(c._matrix) - 1):
                    dist = ((i * self._dh - 1490) ** 2 + (j * self._dh) ** 2) ** 0.5
                    if c._matrixTipos[j][i] == -1 and dist < distMaxima:
                        listaT.append(c._matrix[j][i])
            media = np.median(listaT)
            listaTemperaturas.append(media)

        plt.xlabel("Tiempo [horas]")
        plt.ylabel("Temperatura media [grados Celsius]")
        plt.title("Temperatura media para diferentes horas a una distancia menor a " + str(distMaxima))
        plt.plot(listaTiempos, listaTemperaturas)
        plt.show()



