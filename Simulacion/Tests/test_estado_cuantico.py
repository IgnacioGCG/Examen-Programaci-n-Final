import unittest

from Estado_Cuantico import EstadoCuantico

class TestEstadoCuantico(unittest.TestCase):
    def test_normalizacion(self):
        estado = EstadoCuantico("q0", [3, 4], "computacional")
        norma = sum(abs(a)**2 for a in estado.vector)
        self.assertAlmostEqual(norma, 1.0)

    def test_medicion_basica(self):
        estado = EstadoCuantico("q0", [1, 0], "computacional")
        probs = estado.medir()
        self.assertAlmostEqual(probs[0], 1.0)
        self.assertAlmostEqual(probs[1], 0.0)

    def test_superposicion(self):
        estado = EstadoCuantico("q_plus", [0.707, 0.707], "computacional")
        probs = estado.medir()
        self.assertAlmostEqual(probs[0], 0.5, places=2)
        self.assertAlmostEqual(probs[1], 0.5, places=2)

if __name__ == "__main__":
    unittest.main()
