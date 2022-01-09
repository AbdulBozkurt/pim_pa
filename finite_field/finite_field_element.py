import mod_arith.modarith as mod
import prime_numbers


class FiniteFieldElement:

    def __init__(self, e=0, p=0):
        self.e = e
        if not prime_numbers.prime_test(p):
            raise ValueError('The given base {0} is not a prime number.'.format(p))
        self.p = p

    def __str__(self):
        return "(Element: {0}, Base: {1})".format(self.e, self.p)

    def __add__(self, other):
        if self.p != other.p:
            raise ArithmeticError('Cannot add two elements from different finite fields. '
                                  'Given bases were {0} and {1}'.format(self.p, other.p))
        e = mod.mod_add(self.e, other.e, self.p)
        return FiniteFieldElement(e, self.p)

    def __sub__(self, other):
        if self.p != other.p:
            raise ArithmeticError('Cannot subtract two elements from different finite fields. '
                                  'Given bases were {0} and {1}'.format(self.p, other.p))
        e = mod.mod_sub(self.e, other.e, self.p)
        return FiniteFieldElement(e, self.p)

    def __mul__(self, other):
        if self.p != other.p:
            raise ArithmeticError('Cannot multiply two elements from different finite fields. '
                                  'Given bases were {0} and {1}'.format(self.p, other.p))
        e = mod.mod_mul(self.e, other.e, self.p)
        return FiniteFieldElement(e, self.p)

    def __truediv__(self, other):
        if self.p != other.p:
            raise ArithmeticError('Cannot divide two elements from different finite fields. '
                                  'Given bases were {0} and {1}'.format(self.p, other.p))
        e = mod.mod_div(self.e, other.e, self.p)
        return FiniteFieldElement(e, self.p)


if __name__ == '__main__':
    e1 = FiniteFieldElement(10, 11)
    e2 = FiniteFieldElement(3, 11)
    print(e1+e2)
    print(e1-e2)
    print(e1*e2)
    print(e1/e2)
