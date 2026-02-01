import unittest
from calculator import safe_eval
import math

class TestSafeEval(unittest.TestCase):
    def test_basic_arithmetic(self):
        self.assertEqual(safe_eval('2+4'), 6)
        self.assertEqual(safe_eval('2 + 4'), 6)
        self.assertEqual(safe_eval('3*5'), 15)
        self.assertEqual(safe_eval('(2+3)*4'), 20)

    def test_division_and_mod(self):
        self.assertEqual(safe_eval('10/2'), 5.0)
        self.assertEqual(safe_eval('5%2'), 1)

    def test_power_caret_and_operator(self):
        self.assertEqual(safe_eval('2**3'), 8)
        # support '^' which is normalized to '**'
        self.assertEqual(safe_eval('2^3'), 8)

    def test_functions(self):
        self.assertAlmostEqual(safe_eval('sqrt(9)'), 3.0)
        self.assertAlmostEqual(safe_eval('sin(0)'), 0.0)
        self.assertAlmostEqual(safe_eval('cos(0)'), 1.0)
        # log(8,2) == 3
        self.assertAlmostEqual(safe_eval('log(8,2)'), 3.0)

    def test_errors(self):
        with self.assertRaises(ValueError):
            safe_eval('import os')
        with self.assertRaises(ValueError):
            safe_eval('os.system("ls")')

if __name__ == '__main__':
    unittest.main()
