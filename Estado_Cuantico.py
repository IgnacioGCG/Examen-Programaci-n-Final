import numpy as np

class EstadoCuantico:
    def __init__(self, identificador, vector_estado, base):
        self.identificador = identificador
        self.vector_estado = np.array(vector_estado, dtype=complex)
        self.base = base
        self.normalizar()

    def normalizar(self):
        norma = np.linalg.norm(self.vector_estado)
        if norma == 0:
            raise ValueError("El vector de estado no puede tener norma cero.")
        self.vector_estado /= norma

    def medir(self):
        return np.abs(self.vector_estado) ** 2

    def __str__(self):
        return f"{self.identificador}: {self.vector_estado.tolist()} en base {self.base}"

    def a_diccionario(self):
        return {
            "identificador": self.identificador,
            "vector_estado": self.vector_estado.tolist(),
            "base": self.base
        }

    @staticmethod
    def desde_diccionario(datos):
        return EstadoCuantico(
            datos["identificador"],
            datos["vector_estado"],
            datos["base"]
        )
