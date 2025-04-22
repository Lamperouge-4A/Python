# Simulación de la ramificación de un río usando un modelo de crecimiento fractal
import numpy as np
import random
import matplotlib.pyplot as plt

def generate_river_branching(iterations=5, angle=np.pi/4, length=1, scale=0.7):
    """
    Genera un sistema de ramificación de río usando recursividad similar a un fractal.
    """
    def branch(x, y, angle, length, depth):
        if depth == 0:
            return
        x_end = x + length * np.cos(angle)
        y_end = y + length * np.sin(angle)
        plt.plot([x, x_end], [y, y_end], 'b-', lw=2)

        # Generar dos nuevas ramas con ángulos modificados
        branch(x_end, y_end, angle + random.uniform(0.2, 0.5) * np.pi, length * scale, depth - 1)
        branch(x_end, y_end, angle - random.uniform(0.2, 0.5) * np.pi, length * scale, depth - 1)

    plt.figure(figsize=(6, 8))
    branch(0, 0, np.pi / 2, length, iterations)
    plt.title("Simulación de la ramificación de un río")
    plt.axis("off")
    plt.show()

# Generar y mostrar el río fractal
generate_river_branching()
