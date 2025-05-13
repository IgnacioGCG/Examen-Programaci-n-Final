import json
import numpy as np

class EstadoCuantico:
    def __init__(self, identificador, vector_estado, base):
        self.identificador = identificador
        self.vector_estado = np.array(vector_estado, dtype=complex)
        self.base = base

    def aplicar_operador(self, matriz_operador):
        matriz_operador = np.array(matriz_operador, dtype=complex)
        self.vector_estado = np.dot(matriz_operador, self.vector_estado)

    def medir_probabilidades(self):
        probabilidades = np.abs(self.vector_estado) ** 2
        return probabilidades

    def a_diccionario(self):
        return {
            "identificador": self.identificador,
            "vector_estado": self.vector_estado.tolist(),
            "base": self.base
        }

    @staticmethod
    def desde_diccionario(datos):
        return EstadoCuantico(datos["identificador"], datos["vector_estado"], datos["base"])


class SistemaCuantico:
    def __init__(self):
        self.estados = {}

    def listar_estados(self):
        for identificador, estado in self.estados.items():
            print(f"ID: {identificador}, Vector: {estado.vector_estado}, Base: {estado.base}")

    def agregar_estado(self, identificador, vector_estado, base):
        if identificador in self.estados:
            raise ValueError(f"El estado con ID '{identificador}' ya existe.")
        self.estados[identificador] = EstadoCuantico(identificador, vector_estado, base)

    def aplicar_operador_a_estado(self, identificador, matriz_operador):
        if identificador not in self.estados:
            raise ValueError(f"El estado con ID '{identificador}' no se encontró.")
        self.estados[identificador].aplicar_operador(matriz_operador)

    def medir_estado(self, identificador):
        if identificador not in self.estados:
            raise ValueError(f"El estado con ID '{identificador}' no se encontró.")
        probabilidades = self.estados[identificador].medir_probabilidades()
        print(f"Probabilidades para el estado '{identificador}': {probabilidades}")
        return probabilidades

    def guardar_en_archivo(self, nombre_archivo):
        with open(nombre_archivo, 'w') as archivo:
            json.dump([estado.a_diccionario() for estado in self.estados.values()], archivo)

    def cargar_desde_archivo(self, nombre_archivo):
        with open(nombre_archivo, 'r') as archivo:
            datos = json.load(archivo)
            self.estados = {item["identificador"]: EstadoCuantico.desde_diccionario(item) for item in datos}


# Ejemplo de uso
if __name__ == "__main__":
    sistema = SistemaCuantico()

    # Agregar un estado cuántico
    sistema.agregar_estado("q1", [1, 0], "computacional")

    # Listar estados
    sistema.listar_estados()

    # Aplicar una puerta X (operador de Pauli-X)
    puerta_x = [[0, 1], [1, 0]]
    sistema.aplicar_operador_a_estado("q1", puerta_x)

    # Medir probabilidades
    sistema.medir_estado("q1")

    # Guardar en archivo
    sistema.guardar_en_archivo("estados_cuanticos.json")

    # Cargar desde archivo
    sistema.cargar_desde_archivo("estados_cuanticos.json")
    sistema.listar_estados()