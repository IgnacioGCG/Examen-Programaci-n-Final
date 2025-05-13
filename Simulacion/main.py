from Simulacion.src.Repositorio_Estados import RepositorioDeEstados
from Simulacion.src.Operador_Cuantico import OperadorCuantico

if __name__ == "__main__":
    repo = RepositorioDeEstados()

    # Crear estado |0⟩
    repo.agregar_estado("q0", [1, 0], "computacional")

    # Definir puerta X
    puerta_x = OperadorCuantico("X", [[0, 1], [1, 0]])

    # Aplicar puerta X a q0 y registrar como q0_X
    repo.aplicar_operador("q0", puerta_x, nuevo_id="q0_X")

    # Medir estado resultante
    repo.medir_estado("q0_X")

    # Guardar en archivo
    repo.guardar("estados.json")

    # Cargar desde archivo nuevo repositorio
    nuevo_repo = RepositorioDeEstados()
    nuevo_repo.cargar("estados.json")
    nuevo_repo.listar_estados()
