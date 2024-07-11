import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import os

# Clase base para superficies 3D
class Superficie3D:
    def __init__(self, x_range, y_range):
        self.x_range = x_range
        self.y_range = y_range
        self.x, self.y = np.meshgrid(np.linspace(x_range[0], x_range[1], 100), np.linspace(y_range[0], y_range[1], 100))

    def calcular_z(self):
        raise NotImplementedError("Este método debe ser implementado por las subclases")

    def generar_datos(self):
        self.z = self.calcular_z()
        return self.x, self.y, self.z

    def obtener_parametros(self):
        return {'x_range': self.x_range, 'y_range': self.y_range}

    def calcular_area(self):
        raise NotImplementedError("Este método debe ser implementado por las subclases")

    def calcular_volumen(self):
        raise NotImplementedError("Este método debe ser implementado por las subclases")

# Clase para representar un plano
class Plano(Superficie3D):
    def __init__(self, x_range, y_range, pendiente):
        super().__init__(x_range, y_range)
        self.pendiente = pendiente

    def calcular_z(self):
        return self.pendiente * self.x

    def obtener_parametros(self):
        parametros = super().obtener_parametros()
        parametros['pendiente'] = self.pendiente
        parametros['tipo_superficie'] = 'Plano'
        return parametros

    def calcular_area(self):
        return np.abs(self.x_range[1] - self.x_range[0]) * np.abs(self.y_range[1] - self.y_range[0])

    def calcular_volumen(self):
        return 0

# Clase para representar un paraboloide
class Paraboloide(Superficie3D):
    def __init__(self, x_range, y_range, coef):
        super().__init__(x_range, y_range)
        self.coef = coef

    def calcular_z(self):
        return self.coef * (self.x**2 + self.y**2)

    def obtener_parametros(self):
        parametros = super().obtener_parametros()
        parametros['coeficiente'] = self.coef
        parametros['tipo_superficie'] = 'Paraboloide'
        return parametros

    def calcular_area(self):
        return np.pi * (self.x_range[1]**2 - self.x_range[0]**2)

    def calcular_volumen(self):
        return (2/3) * np.pi * self.coef * (self.x_range[1]**3 - self.x_range[0]**3)

# Clase para representar una sinusoide
class Sinusoide(Superficie3D):
    def __init__(self, x_range, y_range, frecuencia):
        super().__init__(x_range, y_range)
        self.frecuencia = frecuencia

    def calcular_z(self):
        return np.sin(self.frecuencia * np.sqrt(self.x**2 + self.y**2))

    def obtener_parametros(self):
        parametros = super().obtener_parametros()
        parametros['frecuencia'] = self.frecuencia
        parametros['tipo_superficie'] = 'Sinusoide'
        return parametros

    def calcular_area(self):
        return np.inf  # Área infinita para una sinusoide

    def calcular_volumen(self):
        return np.inf  # Volumen infinito para una sinusoide

# Clase para representar un hiperboloide de una hoja
class HiperboloideDeUnaHoja(Superficie3D):
    def __init__(self, x_range, y_range, a, b, c):
        super().__init__(x_range, y_range)
        self.a = a
        self.b = b
        self.c = c

    def calcular_z(self):
        return np.sqrt((self.x**2 / self.a**2) - (self.y**2 / self.b**2) - 1) * self.c

    def obtener_parametros(self):
        parametros = super().obtener_parametros()
        parametros['a'] = self.a
        parametros['b'] = self.b
        parametros['c'] = self.c
        parametros['tipo_superficie'] = 'HiperboloideDeUnaHoja'
        return parametros

    def calcular_area(self):
        return 2 * np.pi * self.c * self.a * self.b

    def calcular_volumen(self):
        return (4/3) * np.pi * self.a * self.b * self.c

# Clase para representar una esfera
class Esfera(Superficie3D):
    def __init__(self, x_range, y_range, r):
        super().__init__(x_range, y_range)
        self.r = r

    def calcular_z(self):
        return np.sqrt(self.r**2 - self.x**2 - self.y**2)

    def obtener_parametros(self):
        parametros = super().obtener_parametros()
        parametros['radio'] = self.r
        parametros['tipo_superficie'] = 'Esfera'
        return parametros

    def calcular_area(self):
        return 4 * np.pi * self.r**2

    def calcular_volumen(self):
        return (4/3) * np.pi * self.r**3

# Clase para representar un cilindro
class Cilindro(Superficie3D):
    def __init__(self, x_range, y_range, r):
        super().__init__(x_range, y_range)
        self.r = r

    def calcular_z(self):
        return np.sqrt(self.r**2 - self.x**2)

    def obtener_parametros(self):
        parametros = super().obtener_parametros()
        parametros['radio'] = self.r
        parametros['tipo_superficie'] = 'Cilindro'
        return parametros

    def calcular_area(self):
        return 2 * np.pi * self.r * (self.x_range[1] - self.x_range[0])

    def calcular_volumen(self):
        return np.pi * self.r**2 * (self.x_range[1] - self.x_range[0])

# Clase para representar un cono
class Cono(Superficie3D):
    def __init__(self, x_range, y_range, a):
        super().__init__(x_range, y_range)
        self.a = a

    def calcular_z(self):
        return np.sqrt(self.a**2 * (self.x**2 + self.y**2))

    def obtener_parametros(self):
        parametros = super().obtener_parametros()
        parametros['a'] = self.a
        parametros['tipo_superficie'] = 'Cono'
        return parametros

    def calcular_area(self):
        return np.pi * self.a * np.sqrt((self.x_range[1]**2) + (self.y_range[1]**2))

    def calcular_volumen(self):
        return (1/3) * np.pi * self.a**2 * (self.x_range[1] - self.x_range[0])

# Función para guardar la configuración actual en un archivo CSV
def guardar_configuracion_csv(superficie, filename):
    datos = superficie.generar_datos()
    parametros = superficie.obtener_parametros()
    area = superficie.calcular_area()
    volumen = superficie.calcular_volumen()

    new_data = {
        'Dimensiones': [parametros],
        'Area': [area],
        'Volumen': [volumen]
    }

    # Debugging messages
    st.write("Parametros:", parametros)
    st.write("Area:", area)
    st.write("Volumen:", volumen)

    if os.path.exists(filename):
        df = pd.read_csv(filename)
        st.write("Archivo CSV existente cargado.")
    else:
        df = pd.DataFrame(columns=['Dimensiones', 'Area', 'Volumen'])
        st.write("Nuevo archivo CSV creado.")

    df = pd.concat([df, pd.DataFrame(new_data)], ignore_index=True)

    st.write("Datos a guardar en CSV:")
    st.write(df)

    df.to_csv(filename, index=False)
    st.write("Configuración guardada en CSV.")

# Función para listar configuraciones guardadas en CSV
def listar_configuraciones_guardadas_csv(filename):
    if os.path.exists(filename):
        return pd.read_csv(filename)
    else:
        return pd.DataFrame(columns=['Dimensiones', 'Area', 'Volumen'])

# Función para seleccionar y mostrar la superficie
def mostrar_superficie():
    st.sidebar.subheader("Seleccione el tipo de superficie:")
    opciones_superficie = ['Plano', 'Paraboloide', 'Sinusoide', 'Hiperboloide de una hoja', 'Esfera', 'Cilindro', 'Cono']
    tipo_superficie = st.sidebar.selectbox("Tipo de Superficie", opciones_superficie)

    # Crear una nueva instancia de superficie basada en la selección del usuario
    if tipo_superficie == 'Plano':
        pendiente = st.sidebar.number_input("Ingrese la pendiente del plano:", min_value=-10.0, max_value=10.0, step=0.1)
        superficie = Plano((-5, 5), (-5, 5), pendiente)
    elif tipo_superficie == 'Paraboloide':
        coef = st.sidebar.number_input("Ingrese el coeficiente del paraboloide:", min_value=0.1, max_value=10.0, step=0.1)
        superficie = Paraboloide((-5, 5), (-5, 5), coef)
    elif tipo_superficie == 'Sinusoide':
        frecuencia = st.sidebar.number_input("Ingrese la frecuencia de la sinusoide:", min_value=0.1, max_value=10.0, step=0.1)
        superficie = Sinusoide((-5, 5), (-5, 5), frecuencia)
    elif tipo_superficie == 'Hiperboloide de una hoja':
        a = st.sidebar.number_input("Ingrese el valor de a:", min_value=0.1, max_value=10.0, step=0.1)
        b = st.sidebar.number_input("Ingrese el valor de b:", min_value=0.1, max_value=10.0, step=0.1)
        c = st.sidebar.number_input("Ingrese el valor de c:", min_value=0.1, max_value=10.0, step=0.1)
        superficie = HiperboloideDeUnaHoja((-5, 5), (-5, 5), a, b, c)
    elif tipo_superficie == 'Esfera':
        r = st.sidebar.number_input("Ingrese el radio de la esfera:", min_value=0.1, max_value=10.0, step=0.1)
        superficie = Esfera((-5, 5), (-5, 5), r)
    elif tipo_superficie == 'Cilindro':
        r = st.sidebar.number_input("Ingrese el radio del cilindro:", min_value=0.1, max_value=10.0, step=0.1)
        superficie = Cilindro((-5, 5), (-5, 5), r)
    elif tipo_superficie == 'Cono':
        a = st.sidebar.number_input("Ingrese el valor de a del cono:", min_value=0.1, max_value=10.0, step=0.1)
        superficie = Cono((-5, 5), (-5, 5), a)

    # Generar los datos para la superficie seleccionada
    x, y, z = superficie.generar_datos()

    # Crear una figura con Plotly
    fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
    fig.update_layout(title='Superficie 3D', autosize=False, width=700, height=700,
                      margin=dict(l=65, r=50, b=65, t=90))

    # Mostrar la figura
    st.plotly_chart(fig)

    # Guardar configuración
    st.sidebar.subheader("Guardar configuración")
    if st.sidebar.button("Guardar"):
        guardar_configuracion_csv(superficie, "configuraciones.csv")
        st.sidebar.success("¡Configuración guardada!")

# Función principal
def main():
    st.title("Visualización de Superficies 3D")
    mostrar_superficie()

    # Listar configuraciones guardadas
    st.subheader("Configuraciones Guardadas")
    configuraciones_guardadas = listar_configuraciones_guardadas_csv("configuraciones.csv")
    st.dataframe(configuraciones_guardadas)

if __name__ == "__main__":
    main()