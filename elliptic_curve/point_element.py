from finite_field.finite_field_element import FiniteFieldElement
from finite_field.finite_field import FiniteField
from elliptic_curve import EllipticCurve
from algorithm import get_daa_bits, get_naf_bits


class PointElement:
    # TODO: give curve element
    def __init__(self, x: FiniteFieldElement, y: FiniteFieldElement, curve: EllipticCurve):

        if x.field != y.field:
            raise ValueError('The bases of  the given elements are not equal.')
        self.x = x
        self.y = y
        self.curve = curve

    def __str__(self):
        return "(Point: ({0}|{1}) )".format(self.x.e, self.y.e)

    def __add__(self, other):
        # TODO: use this or the formulas from http://hyperelliptic.org ?
        # TODO: check which formulas are the most efficient
        if self.x != other.x:
            slope = (other.y - self.y) / (other.x - self.x)
            x3 = slope * slope - self.x - other.x
            y3 = slope * (self.x - x3) - self.y
            return PointElement(x3, y3, self.curve)

        elif self == other and self.y != 0:
            e1 = FiniteFieldElement(3, self.x.field)
            e2 = FiniteFieldElement(2, self.x.field)
            slope = (e1 * self.x * self.x + self.curve.a) / (e2 * self.y)
            x3 = slope * slope - self.x - self.x
            y3 = slope * (self.x - x3) - self.y
            return PointElement(x3, y3, self.curve)
        else:
            # TODO: rather raising error or handle infinity with projective coordinates ?
            raise ValueError('Point at Infinity')

    def __sub__(self, other):
        return self + (-other)

    def __neg__(self):
        i = FiniteFieldElement(-1, self.y.field)
        return PointElement(self.x, self.y * i, self.curve)

    def is_on_curve(self):

        left = self.y * self.y
        right = self.x * self.x * self.x + self.curve.a * self.x + self.curve.b
        return left == right

    def scalar_mul(self, n: int):
        return

    def double_and_add(self, n: int):
        # TODO: check if point is on curve

        e1 = FiniteFieldElement(0, self.curve.a)
        e2 = FiniteFieldElement(0, self.curve.a)
        result = PointElement(e1, e2, self.curve)
        tmp = result

        for bit in get_daa_bits(n):
            if bit == 1:
                result = result + tmp
            tmp = tmp * 2

        return result

    def non_adjacent_form(self, n: int):
        # TODO: implement addition and doubling in point-class

        e1 = FiniteFieldElement(0, self.curve.a)
        e2 = FiniteFieldElement(0, self.curve.a)
        result = PointElement(e1, e2, self.curve)
        tmp = result

        for bit in get_naf_bits(n):
            if bit == 1:
                result = result + tmp
            tmp = tmp * 2

        return result


if __name__ == '__main__':
    element1 = FiniteFieldElement(3, FiniteField(17))
    element2 = FiniteFieldElement(5, FiniteField(17))
    curve_param_a = FiniteFieldElement(2, FiniteField(17))
    curve_param_b = FiniteFieldElement(3, FiniteField(17))
    curve1 = EllipticCurve(curve_param_a, curve_param_b)
    p1 = PointElement(element1, element2, curve1)
    p2 = PointElement(element2, element1, curve1)
    print(p1.is_on_curve())
    print(p2.is_on_curve())
    print(-p1)
    print(p1+p2)
    print(p1-p2)
    print(p1+p1)
