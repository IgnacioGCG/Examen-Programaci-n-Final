# tests/test_sistema_cuantico.py
import unittest
import tempfile
import os
from src.Estado_Cuantico import EstadoCuantico
from src.Operador_Cuantico import OperadorCuantico
from src.Repositorio_Estados import RepositorioDeEstados

class TestSistemaCuantico(unittest.TestCase):

    def test_creacion_estado_y_medicion_trivial(self):
        estado = EstadoCuantico("q0", [1, 0], "computacional")
        probs = estado.medir()
        self.assertAlmostEqual(probs[0], 1.0)
        self.assertAlmostEqual(probs[1], 0.0)

    def test_agregar_y_listar_estados(self):
        repo = RepositorioDeEstados()
        repo.agregar_estado("q0", [1, 0], "computacional")
        repo.agregar_estado("q1", [0, 1], "computacional")
        estados = repo.listar_estados()
        self.assertEqual(len(estados), 2)
        self.assertIn("ID: q0", estados[0] + estados[1])
        self.assertIn("ID: q1", estados[0] + estados[1])

    def test_agregar_estado_duplicado(self):
        repo = RepositorioDeEstados()
        repo.agregar_estado("q0", [1, 0], "computacional")
        with self.assertRaises(ValueError):
            repo.agregar_estado("q0", [0, 1], "computacional")

    def test_operador_x_aplicado_a_0(self):
        estado = EstadoCuantico("q0", [1, 0], "computacional")
        X = OperadorCuantico("X", [[0, 1], [1, 0]])
        resultado = X.aplicar(estado)
        esperado = [0, 1]
        for i in range(len(esperado)):
            self.assertAlmostEqual(resultado.vector[i], esperado[i])

    def test_hadamard_doble(self):
        estado = EstadoCuantico("psi", [1, 0], "computacional")
        H = OperadorCuantico("H", [[0.70710678, 0.70710678], [0.70710678, -0.70710678]])
        estado_1 = H.aplicar(estado)
        estado_2 = H.aplicar(estado_1)
        esperado = [1, 0]
        for i in range(len(esperado)):
            self.assertAlmostEqual(estado_2.vector[i], esperado[i], places=2)

    def test_medicion_estado_equilibrado(self):
        estado = EstadoCuantico("plus", [0.70710678, 0.70710678], "computacional")
        probs = estado.medir()
        self.assertAlmostEqual(probs[0], 0.5, places=1)
        self.assertAlmostEqual(probs[1], 0.5, places=1)

    def test_persistencia_guardar_y_cargar(self):
        repo = RepositorioDeEstados()
        repo.agregar_estado("q0", [1, 0], "computacional")
        repo.agregar_estado("q1", [0, 1], "computacional")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
            temp_path = temp_file.name

        try:
            repo.guardar(temp_path)

            nuevo_repo = RepositorioDeEstados()
            nuevo_repo.cargar(temp_path)
            estados = nuevo_repo.listar_estados()
            self.assertEqual(len(estados), 2)
            self.assertIn("ID: q0", estados[0] + estados[1])
            self.assertIn("ID: q1", estados[0] + estados[1])
        finally:
            os.remove(temp_path)

if __name__ == '__main__':
    unittest.main()
