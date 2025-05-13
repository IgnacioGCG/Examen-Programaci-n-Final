import unittest
from Simulacion.src.Estado_Cuantico import EstadoCuantico
from Simulacion.src.Operador_Cuantico import OperadorCuantico

class TestOperadorCuantico(unittest.TestCase):
    def test_aplicar_x(self):
        estado = EstadoCuantico("q1", [0, 1], "computacional")  # |1>
        X = OperadorCuantico("X", [[0, 1], [1, 0]])
        nuevo = X.aplicar(estado)
        self.assertAlmostEqual(nuevo.vector[0], 1.0)
        self.assertAlmostEqual(nuevo.vector[1], 0.0)

    def test_aplicar_hadamard(self):
        estado = EstadoCuantico("q0", [1, 0], "computacional")  # |0>
        H = OperadorCuantico("H", [[0.707, 0.707], [0.707, -0.707]])
        resultado = H.aplicar(estado)
        self.assertAlmostEqual(resultado.vector[0], 0.707, places=2)
        self.assertAlmostEqual(resultado.vector[1], 0.707, places=2)

if __name__ == "__main__":
    unittest.main()
