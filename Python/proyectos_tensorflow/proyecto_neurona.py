import tensorflow as tf
import numpy as np
import threading #miski herramienta para mas tarde

import matplotlib.pyplot as plt

#Tamaño asignado de dato por neurona, asi como 
neurona = np.random.choice([0, 1], size = 8)
print("Neurona activa, consultando...", neurona)

sensores = np.random.choice ([0, 1], size = 4)

minimos = sensores 
maximos = sensores 

neurona [4:] = minimos 
neurona [:4] = maximos

print('estado actual de los sensores...', sensores)
print('Estado actual de la neurona', neurona)

if np.array_equal(neurona, [0, 0, 1, 1, 0, 0, 1, 1],):
    print('Seguir Recto')
elif np.array_equal(neurona, [0, 1, 0, 1, 0, 1, 0, 1]):
    print('Girar a la Derecha')
elif np.array_equal(neurona, [1, 0, 1, 0, 1, 0, 1, 0]):
    print('Girar a la Izquierda')


