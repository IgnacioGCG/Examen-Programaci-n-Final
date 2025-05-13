from typing import List, Union
import numpy as np


class EstadoCuantico:
    def __init__(self, identificador: str, vector: List[Union[float, complex]], base: str = "computacional"):
        if not vector:
            raise ValueError("El vector de estado no puede estar vacío.")
        
        self.id = identificador
        self.vector = np.array(vector, dtype=complex)
        self.base = base

        if not self._esta_normalizado():
            self._normalizar()

    def _esta_normalizado(self, tolerancia=1e-10) -> bool:
        norma = np.linalg.norm(self.vector)
        return abs(norma - 1.0) <= tolerancia

    def _normalizar(self):
        norma = np.linalg.norm(self.vector)
        if norma == 0:
            raise ValueError("El vector de estado no puede tener norma cero.")
        self.vector /= norma

    def medir(self) -> Union[List[float], dict]:
        """Calcula las probabilidades de medición en la base actual."""
        probabilidades = np.abs(self.vector) ** 2
        if self.base == "computacional":
            return {str(i): round(float(p), 6) for i, p in enumerate(probabilidades)}
        else:
            return probabilidades.tolist()

    def __str__(self) -> str:
        vector_str = [str(round(a.real, 6)) + (f"+{round(a.imag, 6)}j" if a.imag != 0 else "") for a in self.vector]
        return f"{self.id}: vector={vector_str} en base {self.base}"

    def __repr__(self) -> str:
        return self.__str__()
