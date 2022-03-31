import mod_arith.modarith as mod
from finite_field.finite_field import FiniteField
from sympy.polys.domains import ZZ
from sympy.polys.galoistools import gf_gcdex

__all__ = ["FiniteFieldElement"]


class FiniteFieldElement:

    def __init__(self, e: list, field: FiniteField):
        """Constructor for FiniteFieldElement-objects"""
        if not isinstance(e, list):
            raise ValueError('The given element object is not of type list')
        if not isinstance(field, FiniteField):
            raise ValueError('The given field object is not of type finite field')
        self.field = field
        self.e = field.reduce_poly(e)

    def __str__(self):
        if not self.e:
            return "(Element: 0, {0})".format(self.field)
        else:
            s = ""
            temp = list(reversed(self.e))
            for i, el in enumerate(temp):
                s = "{0}*x^{1}".format(el, i) + " + " + s
            return "(Element: {0},\n {1})".format(s[:-7], self.field)

    def __add__(self, other):
        """Overloading the "+"-operator to be able to add two objects of this class"""
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
            result.append(mod.mod_add(e, a[i], self.field.p))
        return FiniteFieldElement(result, self.field)

    def __sub__(self, other):
        """Overloading the "-"-operator to be able to subtract two objects of this class"""
        if not isinstance(other, FiniteFieldElement):
            raise ValueError('Tried to add a object that is not of type FiniteFieldElement but of type: {0}'
                             .format(type(other)))
        if self.field != other.field:
            raise ArithmeticError('Cannot add two elements from different finite fields. '
                                  'Given bases were {0} and {1}'.format(self.field, other.field))
        temp = other.e.copy()
        for i in range(len(other.e)):
            temp[i] = -other.e[i]
        other = FiniteFieldElement(temp, self.field)
        return self + other

    def __mul__(self, other):
        """Overloading the "*"-operator to be able to multiply two objects of this class"""
        if not isinstance(other, FiniteFieldElement):
            raise ValueError('Tried to add a object that is not of type FiniteFiledElement but of type: {0}'
                             .format(type(other)))
        if self.field != other.field:
            raise ArithmeticError('Cannot subtract two elements from different finite fields. '
                                  'Given bases were {0} and {1}'.format(self.field, other.field))
        # initialize result polynomial-array with length a + b
        result = [0 for _ in range(len(self.e) + len(other.e) - 1)]
        for i, a_element in enumerate(self.e):
            for j, b_element in enumerate(other.e):
                result[i + j] += mod.mod_mul(a_element, b_element, self.field.p)
        return FiniteFieldElement(result, self.field)

    def __truediv__(self, other):
        """Overloading the "/"-operator to be able to divide two objects of this class"""
        if not isinstance(other, FiniteFieldElement):
            raise ValueError('Tried to add a object that is not of type FiniteFiledElement but of type: {0}'
                             .format(type(other)))
        if self.field != other.field:
            raise ArithmeticError('Cannot subtract two elements from different finite fields. '
                                  'Given bases were {0} and {1}'.format(self.field, other.field))
        s, t, g = gf_gcdex(ZZ.map(other.e), ZZ.map(self.field.poly), self.field.p, ZZ)
        inverse = FiniteFieldElement(s, self.field)
        return inverse * self

    def __eq__(self, other):
        """Overloading the "="-operator to be able to compare two objects of this class"""
        if isinstance(other, int):
            if other == 0:
                return len(self.e) == 0
            else:
                raise ValueError("Cannot compare FiniteFieldElement to integers.")
        if not isinstance(other, FiniteFieldElement):
            raise ValueError("Cannot compare FiniteFieldElement to object of type {0}".format(type(other)))
        if self.field != other.field:
            raise ValueError(f"Cannot compare two elements from different finite fields. Given bases were {self.field} "
                             f"and {other.field}.")
        if len(self.e) != len(other.e):
            return False
        for i, j in zip(self.e, other.e):
            if i != j:
                return False
        return True
