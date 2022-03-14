import mod_arith.modarith as mod
from finite_field.finite_field import FiniteField
__all__ = ["FiniteFieldElement"]


class FiniteFieldElement:

    def __init__(self, e=[], field=None):
        if not isinstance(e, list):
            raise ValueError('The given element object is not of type list')
        if not isinstance(field, FiniteField):
            raise ValueError('The given field object is not of type finite field')
        self.field = field
        self.e = field.reduce_poly(e)

    def __str__(self):
        # TODO for polynomial
        return "(Element: {0}, {1})".format(self.e, self.field)

    def __add__(self, other):
        if not isinstance(other, FiniteFieldElement):
            raise ValueError('Tried to add a object that is not of type FiniteFieldElement but of type: {0}'
                             .format(type(other)))
        if self.field != other.field:
            raise ArithmeticError('Cannot add two elements from different finite fields. '
                                  'Given bases were {0} and {1}'.format(self.field, other.field))
        a = self.e
        b = other.e
        if len(a) < len(b):
            temp = b.copy()
            b = a.copy()
            a = temp
        b = list(reversed(b))
        for i in range(len(a) - len(b)):
            b.append(0)
        result = list()
        for i, e in enumerate(reversed(b)):
            result.append(mod.mod((e + a[i]), self.field.p))
        return FiniteFieldElement(result, self.field)

    def __sub__(self, other):
        if not isinstance(other, FiniteFieldElement):
            raise ValueError('Tried to add a object that is not of type FiniteFieldElement but of type: {0}'
                             .format(type(other)))
        if self.field != other.field:
            raise ArithmeticError('Cannot add two elements from different finite fields. '
                                  'Given bases were {0} and {1}'.format(self.field, other.field))
        a = self.e
        b = other.e
        if len(a) < len(b):
            temp = b.copy()
            b = a.copy()
            a = temp
        b = list(reversed(b))
        for i in range(len(a) - len(b)):
            b.append(0)
        result = list()
        for i, e in enumerate(reversed(b)):
            result.append(mod.mod((e - a[i]), self.field.p))
        return FiniteFieldElement(result, self.field)

    def __mul__(self, other):
        if not isinstance(other, FiniteFieldElement):
            raise ValueError('Tried to add a object that is not of type FiniteFiledElement but of type: {0}'
                             .format(type(other)))
        if self.field != other.field:
            raise ArithmeticError('Cannot subtract two elements from different finite fields. '
                                  'Given bases were {0} and {1}'.format(self.field, other.field))
        # initialize result polynomial-array with length a + b
        result = [0 for x in range(len(self.e) + len(other.e) - 1)]
        for i, a_element in enumerate(self.e):
            for j, b_element in enumerate(other.e):
                result[i + j] += a_element * b_element
        return FiniteFieldElement(result, self.field)

    def __truediv__(self, other):
        # TODO probably dont need it anymore
        if self.field != other.field:
            raise ArithmeticError('Cannot divide two elements from different finite fields. '
                                  'Given bases were {0} and {1}'.format(self.field, other.field))
        e = mod.mod_div(self.e, other.e, self.field.p)
        return FiniteFieldElement(e, self.field)

    def __eq__(self, other):
        if isinstance(other, int):
            return self.e == other
        if self.field != other.field:
            raise ValueError(f"Cannot compare two elements from different finite fields. Given bases were {self.field} "
                             f"and {other.field}.")
        return self.e == other.e


if __name__ == '__main__':
    e1 = FiniteFieldElement(10, FiniteField(11))
    e2 = FiniteFieldElement(3, FiniteField(11))
    print(e2.inv())
    print(e1+e2)
    print(e1-e2)
    print(e1*e2)
    print(e1/e2)
