import unittest
from modarith import *


class MyTestCase(unittest.TestCase):

    def test_add_success(self):
        result = mod_add(35, 42, 11)
        self.assertEqual(0, result)

    def test_sub_success(self):
        result = mod_sub(35, 42, 11)
        self.assertEqual(4, result)

    def test_mul_success(self):
        result = mod_mul(5, 3, 11)
        self.assertEqual(4, result)

    def test_div_success(self):
        result = mod_div(5, 3, 11)
        self.assertEqual(9, result)

    def test_inv_success(self):
        result = mod_inv(8, 11)
        self.assertEqual(7, result)

    def test_error_zero_k(self):
        functions = (mod_add, mod_sub, mod_div, mod_mul)
        for func in functions:
            try:
                func(5, 4, 0)
            except ValueError:
                continue
            self.fail(f"Test of function {func.__name__} should fail, because k = 0 is not allowed")

    def test_error_zero_k_inv(self):
        try:
            mod_inv(5, 0)
        except ValueError:
            return
        self.fail("Test of function mod_inv should fail, because k = 0 is not allowed")

    def test_error_negative_k(self):
        functions = (mod_add, mod_sub, mod_div, mod_mul)
        for func in functions:
            try:
                func(5, 4, -1)
            except ValueError:
                continue
            self.fail(f"Test of function {func.__name__} should fail, because k < 0 is not allowed")

    def test_error_negative_k_inv(self):
        try:
            mod_inv(5, -1)
        except ValueError:
            return
        self.fail("Test of function mod_inv should fail, because k < 0 is not allowed")

    def test_error_inv_not_mutual_prime(self):
        try:
            mod_inv(5, 15)
        except ValueError:
            return
        self.fail("Test of function mod_inv should fail, because x and k are not mutually prime")

    def test_error_negative_euclidean(self):
        params = ((-8, -5), (-7, 4), (15, -4))
        for param in params:
            try:
                euclidean_alg(*param)
            except ValueError:
                continue
            self.fail(f"Test of function euclidean_alg should fail with parameters {param},"
                      " because they are not allowed to be negative")

    def test_euclidean_success(self):
        x = 127
        y = 532
        gcd = euclidean_alg(x, y)
        self.assertTrue((x % gcd) == 0, f"{gcd} was result, but does not divide {x}")
        self.assertTrue((y % gcd) == 0, f"{gcd} was result, but does not divide {y}")
        smaller_one = min(x, y)
        for i in range(gcd + 1, smaller_one):
            self.assertTrue(((x % i) != 0) or ((y % i) != 0), f"gcd {gcd} was not the greatest divisor. {i} is greater")

    def test_ext_euclidean_success(self):
        x = 127
        y = 532
        d, s, t = extended_euclidean_alg(x, y)
        self.assertTrue(d == s * x + t * y, f"results d = {d}, s = {s} and t = {t} did not satisfy the equation "
                                            f"d == s * x + t * y with x = {x} and y = {y}")

    def test_mod_pow(self):
        x = 2
        y = 10
        k = 10
        result = mod_pow(x, y, k)
        self.assertEqual(result, pow(x, y, k))


if __name__ == '__main__':
    unittest.main()
