Se adjuntan tres archivos: Corte.py, Main.py y exe.py
-----------------------------------------------------------------------------------
Corte.py
Tiene la clase Corte, que modela lo pedido en la tarea, no es necesario ejecutarlo, puesto que esto se hace a través de Main.
-----------------------------------------------------------------------------------
Main.py
Tiene la clase Main, que instancia a la clase Corte para generar los modelos pedidos en la tarea. No es necesario ejecutarla, esto se hace desde exe.py.

####################################################################################
PARA EJECUTAR, abrir el archivo exe.py y quitarle el comentario a el o los métodos que se quieran llamar. Luego correr este archivo.
####################################################################################

La clase Main tiene los siguientes métodos:

-modeloSinIterar(self, dh = 20, t = 0, usarRho = False, omega = 0, tol = 0.1)
Todos los parametros tienen los valores por defecto mostrados por lo que se puede ejecutar directamente como modeloSinIterar( ). Genera el terreno sin iteraciones.

-modeloConIterar(self, dh = 20, t = 0, usarRho = False, omega = 0, tol = 0.1)
Todos los parametros tienen los valores por defecto mostrados, por lo que se puede ejecutar directamente como modeloSinIterar( ). Genera el terreno con iteraciones.

-reqParte3(self)
Al ejecutarlo genera todos los gráficos pedidos en la parte 3 de requerimientos en el enunciado de la tarea (demora bastante)

-reqParte4(self)
Analogo al anterior para la parte 4 (demorabastante)

-temperaturasMedias(self, usarRho = False)
Genera el grafico de temperatura media para distintos tiempos en toda la atmósfera. Se puede definir si usar o no la funcion rho. Por defecto no se ocupa.

-temperaturasMediasLocales(self)
Genera el grafico de temperatura media para distintos tiempos en un area cercana a la planta. Se puede definir la distancia a la que se grafica (por defecto 300) y si usar o no la funcion rho. Por defecto no se ocupa.
