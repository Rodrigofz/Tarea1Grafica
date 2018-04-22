import Tarea1 as tar
import matplotlib.pyplot as plt

"""
@author: Rodrigo Fuentes
"""

class Main:
    def __init__(self):
        self._tol = 0.1
        self._dh = 20

    #Requerimientos: Parte 3
    def reqParte3(self):
        listaTiempos = [0, 8, 12, 16, 20]

        #Cuado omega es cero, la clase corte busca el optimo con la formula vista
        listaOmegas = [ 1.2, 1.4, 1.6, 1.8, 0]

        #Para graficar
        ejeX = []
        ejeY = []

        for t in listaTiempos:
            #Decidi explorar distintos omegas para un mismo tiempo. Hacerlo para cada
            #uno era demasiado tiempo y muchos graficos.
            #Para los demas tiempos se calcula el omega optimo
            if t == 12:
                for w in listaOmegas:
                    print 'Tiempo: ' + str(t) + ', Omega: ' + str(w)
                    c = tar.Corte(self._dh, T = t, omega = w, tol = self._tol)
                    tiempoEjecucion = c.start()

                    #Para graficar numero de iteraciones
                    ejeX.append(c._omega)
                    ejeY.append(tiempoEjecucion)

                    c.plot(c._matrix)

                plt.plot(ejeX, ejeY)
                plt.title("Numero de iteraciones para distintos valores de omega")
                plt.xlabel("Omega")
                plt.ylabel("Numero de iteraciones")
                plt.show()

            else:
                print 'Tiempo: ' + str(t)
                c = tar.Corte(self._dh, T = t, tol = self._tol)
                c.start()
                c.plot(c._matrix)

    #Requerimientos: Parte 4
    def reqParte4(self):
        listaTiempos = [0, 8, 12, 16, 20]

        #Se probaran estos tiempos solo con el omega optimo
        omega = 0

        for t in listaTiempos:
            c = tar.Corte(self._dh, T=t, tol = self._tol, usarRho = True, omega = omega)
            print "Tiempo: " + str(t) + ", Omega: " + str(c._omega)
            c.start()
            c.plot(c._matrix)






m = Main()
m.reqParte4()
