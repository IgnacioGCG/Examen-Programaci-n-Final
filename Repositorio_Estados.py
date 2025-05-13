from Estado_Cuantico import EstadoCuantico
from Operador_Cuantico import OperadorCuantico
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

    def agregar_estado(self, id: str, vector, base: str):
        if id in self.estados:
            raise ValueError(f"Error: ya existe un estado con identificador '{id}'.")
        nuevo_estado = EstadoCuantico(id, vector, base)
        self.estados[id] = nuevo_estado

    def obtener_estado(self, id: str) -> EstadoCuantico:
        if id not in self.estados:
            raise KeyError(f"No se encontró el estado con ID '{id}'.")
        return self.estados[id]

    def eliminar_estado(self, id: str):
        if id not in self.estados:
            raise KeyError(f"No se puede eliminar: no existe estado con ID '{id}'.")
        del self.estados[id]

    def aplicar_operador(self, id_estado: str, operador: OperadorCuantico, nuevo_id: str = None) -> EstadoCuantico:
        """
        Aplica un operador cuántico a un estado existente en el repositorio.
        - Si se proporciona `nuevo_id`, el resultado se guarda con ese ID (error si ya existe).
        - Si no se da `nuevo_id`, se usa el formato `id_estado_operador.nombre` (error si ya existe).
        - No se sobrescribe el estado original por defecto.
        - Valida que la dimensión del operador y del estado coincidan.
        """
        if id_estado not in self.estados:
            raise KeyError(f"No existe estado con ID '{id_estado}'.")

        estado_original = self.estados[id_estado]

        # Verificar dimensiones
        dim_estado = len(estado_original.vector)
        dim_op = len(operador.matriz)
        if dim_op != dim_estado or any(len(fila) != dim_estado for fila in operador.matriz):
            raise ValueError(f"Dimensión del operador ({dim_op}x{dim_op}) no coincide con el estado ({dim_estado}).")

        estado_resultante = operador.aplicar(estado_original)

        # Determinar ID del nuevo estado
        id_resultado = nuevo_id or f"{id_estado}_{operador.nombre}"

        # Verificar si ya existe ese ID
        if id_resultado in self.estados:
            raise ValueError(f"Ya existe un estado con ID '{id_resultado}', no se puede sobrescribir.")

        estado_resultante.id = id_resultado
        self.estados[id_resultado] = estado_resultante

        return estado_resultante
    def medir_estado(self, id: str) -> None:
        """
        Mide el estado cuántico con el ID dado, calcula probabilidades y muestra
        resultados formateados en consola. Las probabilidades se normalizan si es necesario.
        """
        if id not in self.estados:
            print(f"[Error] No existe el estado con ID '{id}'.")
            return

        estado = self.estados[id]
        amplitudes = estado.vector
        base = estado.base

        # Calcular módulo al cuadrado de cada amplitud
        probabilidades = [abs(a)**2 for a in amplitudes]
        suma = sum(probabilidades)

        # Normalización por seguridad (en caso de error numérico)
        if abs(suma - 1.0) > 1e-6:
            probabilidades = [p / suma for p in probabilidades]

        print(f"Medición del estado '{estado.id}' (base {base}):")
        for i, p in enumerate(probabilidades):
            print(f" - Estado base {i}: {round(p * 100, 2)}%")

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
            with open(archivo, newline='', mode='r') as file:
                reader = csv.reader(file, delimiter=';')
                for fila in reader:
                    if len(fila) != 3:
                        print(f"Fila malformada: {fila}")
                        continue
                    id, base, vector_str = fila
                    try:
                        vector = ast.literal_eval(vector_str)  # más seguro que eval()
                        self.agregar_estado(id, vector, base)
                    except (SyntaxError, ValueError) as e:
                        print(f"Error al interpretar vector del estado '{id}': {e}")
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