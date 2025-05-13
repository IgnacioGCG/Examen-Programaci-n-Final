import numpy as np
from Estado_Cuantico import EstadoCuantico

class OperadorCuantico:
    def __init__(self, nombre, matriz):
        self.nombre = nombre
        self.matriz = np.array(matriz, dtype=complex)

    def aplicar(self, estado: EstadoCuantico):
        if self.matriz.shape[1] != estado.vector_estado.shape[0]:
            raise ValueError("Dimensiones del operador no coinciden con el estado.")
        nuevo_vector = np.dot(self.matriz, estado.vector_estado)
        return EstadoCuantico(f"{estado.identificador}_{self.nombre}", nuevo_vector, estado.base)
