import unittest
from Repositorio_Estados import RepositorioDeEstados
from Operador_Cuantico import OperadorCuantico

class TestRepositorioDeEstados(unittest.TestCase):
    def test_agregar_y_obtener(self):
        repo = RepositorioDeEstados()
        repo.agregar_estado("q0", [1, 0], "computacional")
        estado = repo.obtener_estado("q0")
        self.assertEqual(estado.id, "q0")
        self.assertAlmostEqual(estado.vector[0], 1.0)

    def test_no_agrega_repetido(self):
        repo = RepositorioDeEstados()
        repo.agregar_estado("q1", [0, 1], "computacional")
        with self.assertLogs(level='INFO') as log:
            repo.agregar_estado("q1", [0.5, 0.5], "computacional")
        self.assertIn("ya existe un estado", log.output[0])

    def test_aplicar_operador(self):
        repo = RepositorioDeEstados()
        repo.agregar_estado("psi", [0.707, 0.707], "computacional")
        H = OperadorCuantico("H", [[0.707, 0.707], [0.707, -0.707]])
        repo.aplicar_operador("psi", H, "psi_H")
        psi_H = repo.obtener_estado("psi_H")
        self.assertAlmostEqual(psi_H.vector[0], 1.0, places=2)
        self.assertAlmostEqual(psi_H.vector[1], 0.0, places=2)

if __name__ == "__main__":
    unittest.main()
