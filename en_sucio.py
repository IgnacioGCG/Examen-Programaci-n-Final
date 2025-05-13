import csv
import ast  # Para convertir la cadena del vector a una lista de Python
from Estado_Cuantico import EstadoCuantico

class RepositorioDeEstados:
    def __init__(self):
        self.estados = {}

    def listar_estados(self):
        # Mostrar los estados en el repositorio
        if not self.estados:
            return "No hay estados registrados."
        return [str(estado) for estado in self.estados.values()]

    def agregar_estado(self, id, vector, base):
        # Verificar si el estado ya existe
        if id in self.estados:
            print(f"Error: ya existe un estado con identificador '{id}'")
            return
        # Crear el estado y agregarlo al repositorio
        estado = EstadoCuantico(id, vector, base)
        self.estados[id] = estado

    def obtener_estado(self, id):
        # Obtener un estado por su identificador
        return self.estados.get(id, None)

    def aplicar_operador(self, id_estado, operador, nuevo_id=None):
        # Aplicar un operador a un estado cuántico
        estado = self.obtener_estado(id_estado)
        if estado is None:
            print(f"Error: no se encontró el estado con identificador '{id_estado}'")
            return
        nuevo_estado = operador.aplicar(estado)
        if nuevo_id is None:
            nuevo_id = f"{id_estado}_{operador.nombre}"
        self.agregar_estado(nuevo_id, nuevo_estado.vector, nuevo_estado.base)

    def medir_estado(self, id):
        # Medir el estado y mostrar las probabilidades
        estado = self.obtener_estado(id)
        if estado is None:
            print(f"Error: no se encontró el estado con identificador '{id}'")
            return
        probabilidades = estado.medir()
        print(f"Medición del estado '{id}' (base {estado.base}):")
        for i, p in enumerate(probabilidades):
            print(f" - Estado base {i}: {p*100:.2f}%")

    def guardar(self, archivo):
        # Guardar los estados en un archivo CSV
        with open(archivo, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            # Escribir la cabecera
            writer.writerow(['id', 'base', 'vector'])
            # Escribir los estados
            for estado in self.estados.values():
                # Serializar el vector como una cadena
                writer.writerow([estado.id, estado.base, str(estado.vector)])

    def cargar(self, archivo):
        # Cargar los estados desde un archivo CSV
        with open(archivo, mode='r') as file:
            reader = csv.reader(file, delimiter=',')
            next(reader)  # Saltar la cabecera
            for row in reader:
                id = row[0]
                base = row[1]
                # Convertir la cadena del vector a una lista de Python
                vector = ast.literal_eval(row[2])
                self.agregar_estado(id, vector, base)

# Crear un repositorio de estados
repo = RepositorioDeEstados()

# Agregar algunos estados
repo.agregar_estado("q0", [1.0, 0.0], "computacional")
repo.agregar_estado("plus", [0.707, 0.707], "computacional")

# Guardar los estados en un archivo
repo.guardar("estados.csv")

# Cargar los estados desde el archivo
repo2 = RepositorioDeEstados()
repo2.cargar("estados.csv")
print(repo2.listar_estados())  # Debería mostrar los estados cargados
