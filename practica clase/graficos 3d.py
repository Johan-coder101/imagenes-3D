import numpy as np

class Superficie3D:
    def __init__(self, x_range, y_range):
        self.x_range = x_range
        self.y_range = y_range
        self.x, self.y = np.meshgrid(np.linspace(x_range[0], x_range[1], 100), np.linspace(y_range[0],  y_range[1], 100))

    def calcular_z(self):
        raise NotImplementedError("Este método debe ser implementado por las subclases")

    def generar_datos(self):
        self.z = self.calcular_z()
        return self.x, self.y, self.z
    
class Plano(Superficie3D):
    def __init__(self, x_range, y_range, pendiente):
        super().__init__(x_range, y_range)
        self.pendiente = pendiente

    def calcular_z(self):
        return self.pendiente * self.x

class Paraboloide(Superficie3D):
    def __init__(self, x_range, y_range, coef):
        super().__init__(x_range, y_range)
        self.coef = coef

    def calcular_z(self):
        return self.coef * (self.x**2 + self.y**2)

class Sinusoide(Superficie3D):
    def __init__(self, x_range, y_range, frecuencia):
        super().__init__(x_range, y_range)
        self.frecuencia = frecuencia

    def calcular_z(self):
        return np.sin(self.frecuencia * np.sqrt(self.x**2 + self.y**2))

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Visualizador3D:
    def __init__(self, superficie):
        self.superficie = superficie

    def mostrar_con_matplotlib(self):
        x, y, z = self.superficie.generar_datos()
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(x, y, z, cmap='viridis')
        plt.show()

import plotly.graph_objects as go

class Visualizador3DPlotly(Visualizador3D):
    def mostrar_con_plotly(self):
        x, y, z = self.superficie.generar_datos()
        fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
        fig.update_layout(title='Superficie 3D', autosize=False, width=800, height=800)
        fig.show()
def main():
    print("Seleccione el tipo de superficie:")
    print("1. Plano")
    print("2. Paraboloide")
    print("3. Sinusoide")
    tipo = int(input("Ingrese el número de su elección: "))

    if tipo == 1:
        pendiente = float(input("Ingrese la pendiente del plano: "))
        superficie = Plano((-5, 5), (-5, 5), pendiente)
    elif tipo == 2:
        coef = float(input("Ingrese el coeficiente del paraboloide: "))
        superficie = Paraboloide((-5, 5), (-5, 5), coef)
    elif tipo == 3:
        frecuencia = float(input("Ingrese la frecuencia de la sinusoide: "))
        superficie = Sinusoide((-5, 5), (-5, 5), frecuencia)
    else:
        print("Opción no válida.")
        return

    visualizador = Visualizador3DPlotly(superficie)
    visualizador.mostrar_con_plotly()

if __name__ == "__main__":
    main()
