from Simulacion.src.Estado_Cuantico import EstadoCuantico
from Simulacion.src.Operador_Cuantico import OperadorCuantico
from typing import Dict, List
import csv
import ast  # Para convertir la cadena del vector a una lista de Python

class RepositorioDeEstados:
    def __init__(self):
        self.estados: Dict[str, EstadoCuantico] = {}

    def listar_estados(self) -> List[str]:
        if not self.estados:
            return ["No hay estados registrados."]
        return [str(estado) for estado in self.estados.values()]

    def agregar_estado(self, id, vector, base):
        if id in self.estados:
            print(f"Error: ya existe un estado con identificador '{id}'")
            return
        estado = EstadoCuantico(id, vector, base)
        self.estados[id] = estado
        if self.archivo_actual:
            self.guardar(self.archivo_actual)


    def obtener_estado(self, id: str) -> EstadoCuantico:
        if id not in self.estados:
            raise KeyError(f"No se encontró el estado con ID '{id}'.")
        return self.estados[id]

    def eliminar_estado(self, id: str):
        if id not in self.estados:
            raise KeyError(f"No se puede eliminar: no existe estado con ID '{id}'.")
        del self.estados[id]

    def aplicar_operador(self, id_estado, operador, nuevo_id=None):
        estado_original = self.obtener_estado(id_estado)
        if not estado_original:
            print(f"Error: no existe el estado con id '{id_estado}'")
            return

        if len(estado_original.vector) != len(operador.matriz):
            print("Error: Dimensión del operador y del estado no coinciden.")
            return

        nuevo_estado = operador.aplicar(estado_original)

        if nuevo_id:
            nuevo_estado.id = nuevo_id
        else:
            nuevo_estado.id = f"{id_estado}_{operador.nombre}"

        self.estados[nuevo_estado.id] = nuevo_estado
        if self.archivo_actual:
            self.guardar(self.archivo_actual)
    def medir_estado(self, id):
        estado = self.obtener_estado(id)
        if not estado:
            print(f"Error: estado '{id}' no encontrado.")
            return
        probabilidades = estado.medir()
        print(f"Medición del estado {estado.id} (base {estado.base}):")
        for i, p in enumerate(probabilidades):
            print(f" - Estado base {i}: {round(p * 100, 3)}%")

#NO COLAPSO DEL ESTADO
# Crear el repositorio
repo = RepositorioDeEstados()

# Crear el estado |0⟩
repo.agregar_estado("q0", [1, 0], "computacional")
repo.medir_estado("q0")  # Esperado: 100% en base 0

# Crear el estado |+⟩ (superposición equitativa)
repo.agregar_estado("plus", [0.707 + 0j, 0.707 + 0j], "computacional")
repo.medir_estado("plus")  # Esperado: Aproximadamente 50% y 50%

# Aplicar una puerta H a |0⟩, que debería transformar |0⟩ en |+⟩
H = OperadorCuantico("H", [[0.707, 0.707], [0.707, -0.707]])
repo.aplicar_operador("q0", H, "q0_H")
repo.medir_estado("q0_H")  # Esperado: Aproximadamente 50% y 50%

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
        try:
            with open(archivo, newline='') as file:
                reader = csv.reader(file, delimiter=';')
                for fila in reader:
                    if len(fila) != 3:
                        print(f"Fila malformada: {fila}")
                        continue
                    id, base, vector_str = fila
                    try:
                        vector = ast.literal_eval(vector_str)
                        self.estados[id] = EstadoCuantico(id, vector, base)
                    except Exception as e:
                        print(f"Error en vector del estado '{id}': {e}")
            self.archivo_actual = archivo
        except FileNotFoundError:
            print(f"Archivo '{archivo}' no encontrado.")

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