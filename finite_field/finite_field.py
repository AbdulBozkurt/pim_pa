import finite_field.prime_numbers as prime_numbers
import mod_arith.modarith as mod
__all__ = ["FiniteField", "get_safe_field"]


def clean_list(a: list) -> list:
    """Cleans a list defining a polynomial of all leading zeros"""
    while a[0] == 0:
        a.pop(0)
    return a


def multiply(a, b):
    # initialize result polynom-array with length a + b
    result = [0 for x in range(len(a) + len(b) - 1)]
    for i, a_element in enumerate(a):
        for j, b_element in enumerate(b):
            result[i+j] += a_element * b_element
    return result


def add(a: list, b: list, p: int) -> list:
    if len(a) < len(b):
        temp = b.copy()
        b = a.copy()
        a = temp
    b = list(reversed(b))
    for i in range(len(a)-len(b)):
        b.append(0)

    result = list()
    for i, e in enumerate(reversed(b)):
        result.append(mod.mod((e + a[i]), p))
    return result


def generate_poly(factors: dict, p: int) -> list:
    poly = [0 for x in range(max(factors)+1)]
    for i in factors:
        poly[i] = factors[i] % p
    return list(reversed(poly))


def get_safe_field():
    """Returns a FiniteField with parameters safe for use in cryptographic context"""
    temp = {128: 2, 97: -2, 0: -1}
    p = 340282366762482138434845932244680310783
    poly = generate_poly(temp, p)
    return FiniteField(p, poly)


class FiniteField:

    def __init__(self, p: int, poly: list):
        if not prime_numbers.prime_test(p):
            raise ValueError('The given base {0} is not a prime number.'.format(p))
        self.p = p
        for i, f in enumerate(poly):
            poly[i] = mod.mod(f, p)
        self.poly = clean_list(poly)
        # generate the reducing-polynomial
        r_pol = list()
        for f in poly[1:]:
            index = mod.mod((-f * pow(poly[0], -1, self.p)), self.p)
            r_pol.append(index)
        self.r_pol = r_pol
        # TODO maybe check for irreducible polynomial

    def __str__(self):
        # TODO implement for polynomial
        return "Base: {0}".format(self.p)

    def __eq__(self, other):
        if not isinstance(other, FiniteField):
            return False
        for i, j in self.poly, other.poly:
            if i != j:
                return False
        return self.p == other.p

    def reduce_poly(self, a: list):
        # clean the given lists of leading zeros
        a = clean_list(a)

        while len(a) >= len(self.poly):
            factor = a[0]
            a[0] = 0
            temp = [0 for x in range(len(a))]
            temp[len(self.poly) - 1] = factor
            temp = multiply(temp, self.r_pol)
            a = add(a, temp, self.p)
            a = clean_list(a)

        return a

