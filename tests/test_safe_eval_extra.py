import unittest
from calculator import safe_eval

class TestSafeEvalExtra(unittest.TestCase):
    def test_unary_ops(self):
        self.assertEqual(safe_eval('-5'), -5)
        self.assertEqual(safe_eval('+5'), 5)

    def test_division_by_zero(self):
        with self.assertRaises(ValueError):
            safe_eval('1/0')

    def test_invalid_constant(self):
        with self.assertRaises(ValueError):
            safe_eval('"hello"')

    def test_unsupported_function(self):
        with self.assertRaises(ValueError):
            safe_eval('open(1)')

    def test_invalid_function_args(self):
        # sqrt expects one argument; two should raise ValueError
        with self.assertRaises(ValueError):
            safe_eval('sqrt(1, 2)')

if __name__ == '__main__':
    unittest.main()
