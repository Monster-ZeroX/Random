import unittest
from src.calculator import Calculator

class TestCalculator(unittest.TestCase):
    def test_init(self):
        calc = Calculator()
        self.assertEqual(calc.value, 0)
