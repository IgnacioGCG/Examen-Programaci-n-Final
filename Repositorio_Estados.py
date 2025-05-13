import json
from Estado_Cuantico import EstadoCuantico

class RepositorioDeEstados:
    def __init__(self):
        self.estados = {}

    def listar_estados(self):
        for estado in self.estados.values():
            print(str(estado))

    def agregar_estado(self, identificador, vector_estado, base):
        if identificador in self.estados:
            raise ValueError(f"El estado con ID '{identificador}' ya existe.")
        self.estados[identificador] = EstadoCuantico(identificador, vector_estado, base)

    def obtener_estado(self, identificador):
        if identificador not in self.estados:
            raise ValueError(f"El estado con ID '{identificador}' no se encontró.")
        return self.estados[identificador]

    def aplicar_operador(self, id_estado, operador, nuevo_id=None):
        estado = self.obtener_estado(id_estado)
        nuevo_estado = operador.aplicar(estado)
        nuevo_estado.identificador = nuevo_id or nuevo_estado.identificador
        if nuevo_estado.identificador in self.estados:
            raise ValueError(f"El nuevo ID '{nuevo_estado.identificador}' ya existe en el repositorio.")
        self.estados[nuevo_estado.identificador] = nuevo_estado

    def medir_estado(self, identificador):
        estado = self.obtener_estado(identificador)
        probabilidades = estado.medir()
        print(f"Probabilidades de medición para '{identificador}': {probabilidades}")
        return probabilidades

    def guardar(self, archivo):
        with open(archivo, 'w') as f:
            json.dump([estado.a_diccionario() for estado in self.estados.values()], f, indent=2)

    def cargar(self, archivo):
        with open(archivo, 'r') as f:
            datos = json.load(f)
            self.estados = {
                item["identificador"]: EstadoCuantico.desde_diccionario(item)
                for item in datos
            }
