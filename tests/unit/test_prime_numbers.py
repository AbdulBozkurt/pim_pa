import unittest
from finite_field.prime_numbers import prime_test


class TestPrimeNumbers(unittest.TestCase):

    def test_prime_success(self):
        result = prime_test(1000000000039)
        self.assertTrue(result)

    def test_prime_failure(self):
        result = prime_test(656475752464)
        self.assertFalse(result)

    # def test_find_prime_success(self):
    #     result = find_prime(128)
    #     self.assertEqual(325446522978138837575516171443162690123, result)

    # def test_prime_negative(self):
    #     try:
    #         find_prime(-128)
    #     except ValueError:
    #         return
    #     self.fail(f"Should fail because of negative input.")


if __name__ == "__main__":
    unittest.main()
