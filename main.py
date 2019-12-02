import genetico as gen
import numpy as np
from matplotlib import pyplot as plt    # Librería para graficación


AG = gen.Genetico(1000,-5,5,0.01)
evoluciones = []

for i in range(50):
    print("------------ ITERACION NUMERO {} ------------".format(i+1))
    AG.cruzar()
    AG.mutar()
    AG.decodificar()
    AG.seleccion()
    elite = AG.poblacion[0]
    pc = AG.longitudX()
    print(elite[:pc],elite[pc:])
    x,y = AG.binToDec(elite[:pc]), AG.binToDec(elite[pc:])
    x,y = AG.transformar(x,y)
    print("el valor de Z es: ",20+x**2+y**2-10*(np.cos(2*np.pi*y)+np.cos(2*np.pi*x)))
    print("(x,y) = ({},{})".format(x,y))
    evoluciones.append(round(AG.apt[0],2))
    print(evoluciones)
    