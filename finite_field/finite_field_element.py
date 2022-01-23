import mod_arith.modarith as mod
from finite_field.finite_field import FiniteField


class FiniteFieldElement:

    def __init__(self, e=0, field=None):
        if type(e) != int:
            raise ValueError('The given element object is not of type int')
        self.e = e
        if type(field) != FiniteField:
            raise ValueError('The given field object is not of type finite field')
        self.field = field

    def __str__(self):
        return "(Element: {0}, {1})".format(self.e, self.field)

    def __add__(self, other):
        if self.field != other.field:
            raise ArithmeticError('Cannot add two elements from different finite fields. '
                                  'Given bases were {0} and {1}'.format(self.field, other.field))
        e = mod.mod_add(self.e, other.e, self.field.p)
        return FiniteFieldElement(e, self.field)

    def __sub__(self, other):
        if self.field != other.field:
            raise ArithmeticError('Cannot subtract two elements from different finite fields. '
                                  'Given bases were {0} and {1}'.format(self.field, other.field))
        e = mod.mod_sub(self.e, other.e, self.field.p)
        return FiniteFieldElement(e, self.field)

    def __mul__(self, other):
        if self.field != other.field:
            raise ArithmeticError('Cannot multiply two elements from different finite fields. '
                                  'Given bases were {0} and {1}'.format(self.field, other.field))
        e = mod.mod_mul(self.e, other.e, self.field.p)
        return FiniteFieldElement(e, self.field)

    def __truediv__(self, other):
        if self.field != other.field:
            raise ArithmeticError('Cannot divide two elements from different finite fields. '
                                  'Given bases were {0} and {1}'.format(self.field, other.field))
        e = mod.mod_div(self.e, other.e, self.field.p)
        return FiniteFieldElement(e, self.field)

    def inv(self):
        return FiniteFieldElement(1, self.field)/self


if __name__ == '__main__':
    e1 = FiniteFieldElement(10, FiniteField(11))
    e2 = FiniteFieldElement(3, FiniteField(11))
    print(e2.inv())
    print(e1+e2)
    print(e1-e2)
    print(e1*e2)
    print(e1/e2)
