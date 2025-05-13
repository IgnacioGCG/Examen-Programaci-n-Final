import numpy as np
from Estado_Cuantico import EstadoCuantico
from typing import List, Union


class OperadorCuantico:
    def __init__(self, nombre: str, matriz: List[List[Union[float, complex]]]):
        self.nombre = nombre
        self.matriz = np.array(matriz, dtype=complex)

        # Verificación mínima de que es cuadrada
        filas, columnas = self.matriz.shape
        if filas != columnas:
            raise ValueError("La matriz del operador debe ser cuadrada (n x n).")

    def aplicar(self, estado: EstadoCuantico) -> EstadoCuantico:
        if len(self.matriz) != len(estado.vector):
            raise ValueError("Dimensión de la matriz y el estado no coinciden.")

        nuevo_vector = np.dot(self.matriz, estado.vector)

        nuevo_id = f"{estado.id}_{self.nombre}"
        return EstadoCuantico(nuevo_id, nuevo_vector, estado.base)

    def __str__(self):
        return f"Operador '{self.nombre}' con matriz:\n{self.matriz}"

    def __repr__(self):
        return self.__str__()

