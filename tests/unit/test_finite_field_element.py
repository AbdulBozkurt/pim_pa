from finite_field import *
import unittest


class TestFiniteFieldElement(unittest.TestCase):

    def test_final_field_element(self):
        self.assertEqual(2, 2, "Should be 2")


if __name__ == "__main__":
    unittest.main()
