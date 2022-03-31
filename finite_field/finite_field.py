import random
import mod_arith.modarith as mod
__all__ = ["FiniteField", "get_safe_field", "generate_poly"]


def prime_test(p: int) -> bool:
    """Checks, whether a given integer p is prime"""
    for i in range(100):
        a = random.randrange(1, p-1)
        if mod.mod_pow(a, p-1, p) != 1:
            return False
    return True


def clean_list(a: list) -> list:
    """Cleans a list defining a polynomial of all leading zeros"""
    if len(a) == 0:
        return a
    while a[0] == 0:
        a.pop(0)
        if len(a) == 0:
            return a
    return a


def multiply(a: list, b: list, p: int) -> list:
    """Multiplies two given polynomials with the factors modulo p"""
    result = [0] * (len(a) + len(b) - 1)
    for i, a_element in enumerate(a):
        for j, b_element in enumerate(b):
            result[i+j] += a_element * b_element
    return [i % p for i in result]


def add(a: list, b: list, p: int) -> list:
    """Adds two given polynomials with the factors modulo p"""
    if len(a) < len(b):
        temp = b.copy()
        b = a.copy()
        a = temp
    b = list(reversed(b))
    for i in range(len(a)-len(b)):
        b.append(0)

    result = list()
    for i, e in enumerate(reversed(b)):
        result.append(mod.mod_add(e, a[i], p))
    return result


def generate_poly(factors: dict, p: int) -> list:
    """Generates a list defining a polynomial from a dictionary giving the factors at specific points
        and a prime number p to calculate the modulo from"""
    poly = [0 for _ in range(max(factors)+1)]
    for i in factors:
        poly[i] = mod.mod(factors[i], p)
    return list(reversed(poly))


def get_safe_field():
    """Returns a FiniteField with parameters safe for use in cryptographic context"""
    temp_poly = {19: 1, 18: 1, 17: 13, 16: 46, 15: 57, 14: 94, 13: 7, 12: 19, 11: 100, 10: 15,
                 9: 15, 8: 51, 7: 66, 6: 82, 5: 8, 4: 92, 3: 4, 2: 3, 1: 1, 0: 80}
    p = 103
    poly = generate_poly(temp_poly, p)
    return FiniteField(p, poly)


class FiniteField:

    def __init__(self, p: int, poly: list):
        """Constructor for FiniteField-objects"""
        if not prime_test(p):
            raise ValueError('The given base {0} is not a prime number.'.format(p))
        self.p = p
        for i, f in enumerate(poly):
            poly[i] = mod.mod(f, p)
        self.poly = clean_list(poly)
        # generate the reducing-polynomial
        r_pol = list()
        for f in poly[1:]:
            index = mod.mod_mul(-f, mod.mod_inv(poly[0], self.p), self.p)
            r_pol.append(index)
        self.r_pol = r_pol

    def __str__(self):
        if not self.poly:
            return "(Base: {0}, Poly: 0)".format(self.p)
        else:
            s = ""
            temp = list(reversed(self.poly))
            for i, el in enumerate(temp):
                s = "{0}*x^{1}".format(el, i) + " + " + s
            return "Field: (Base: {0}, Poly: {1})".format(self.p, s[:-7])

    def __eq__(self, other):
        """Overloading the "="-operator to be able to compare two objects of this class"""
        if not isinstance(other, FiniteField):
            return False
        for i, j in zip(self.poly, other.poly):
            if i != j:
                return False
        return self.p == other.p

    def reduce_poly(self, a: list):
        """Reduces a given polynomial using the polynomial defining the current FiniteField"""
        # clean the given lists of leading zeros
        a = (clean_list(a))

        while len(a) >= len(self.poly):
            factor = a[0]
            a[0] = 0
            temp = [0 for _ in range(len(a))]
            temp[len(self.poly) - 1] = factor
            temp = multiply(temp, self.r_pol, self.p)
            a = add(a, temp, self.p)
            a = clean_list(a)

        for i in range(len(a)):
            a[i] = mod.mod(a[i], self.p)
        return a
