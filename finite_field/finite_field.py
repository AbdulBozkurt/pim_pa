import finite_field.prime_numbers as prime_numbers


class FiniteField:

    def __init__(self, p: int):
        if not prime_numbers.prime_test(p):
            raise ValueError('The given base {0} is not a prime number.'.format(p))
        self.p = p

    def __str__(self):
        return "Base: {0}".format(self.p)

    def __eq__(self, other):
        return self.p == other.p


