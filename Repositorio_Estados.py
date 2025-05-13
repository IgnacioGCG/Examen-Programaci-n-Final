from Estado_Cuantico import EstadoCuantico
from Operador_Cuantico import OperadorCuantico
from typing import Dict, List


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

    def aplicar_operador(self, id_estado: str, operador: OperadorCuantico, nuevo_id: str = None):
        if id_estado not in self.estados:
            raise KeyError(f"No existe estado con ID '{id_estado}'.")

        estado_original = self.estados[id_estado]
        estado_resultante = operador.aplicar(estado_original)

        # Determinar identificador del nuevo estado
        id_resultado = nuevo_id or f"{id_estado}_{operador.nombre}"

        # Si se sobrescribe el estado original
        if id_resultado == id_estado:
            self.estados[id_estado] = estado_resultante
        else:
            if id_resultado in self.estados:
                raise ValueError(f"Ya existe un estado con ID '{id_resultado}', no se puede sobrescribir.")
            estado_resultante.id = id_resultado
            self.estados[id_resultado] = estado_resultante

        return estado_resultante  # Opcional: útil para inspección inmediata
