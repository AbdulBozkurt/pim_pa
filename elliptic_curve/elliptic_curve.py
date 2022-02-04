import finite_field.finite_field_element as field
from finite_field.finite_field_element import FiniteFieldElement
from finite_field.finite_field import FiniteField
from point_element import PointElement
from algorithm import get_daa_bits, get_naf_bits


class EllipticCurve:

    def __init__(self, a: FiniteFieldElement, b: FiniteFieldElement):

        e1 = FiniteFieldElement(-1, a.field)
        e2 = FiniteFieldElement(4, a.field)
        e3 = FiniteFieldElement(27, a.field)
        determinant = e1 * (e2 * (a * a * a) + e3 * (b * b))

        if determinant.e == 0:
            raise ValueError('The determinant -(4{0}^3 + 27{1}^2) equals 0.'.format(a, b))
        self.a = a
        self.b = b
        self.field = a.field

    def __str__(self):
        return "(Curve: y^2 = x^3 + {0}x + {1})".format(self.a.e, self.b.e)

    def is_on_curve(self, p: PointElement):
        e1 = FiniteFieldElement(2, p.x.field)
        e2 = FiniteFieldElement(3, p.x.field)

        left = p.y * p.y
        right = p.x * p.x * p.x + e1 * p.x + e2

        return left == right

    def scalar_mul(self, n: int, p: PointElement):
        return

    def double_and_add(self, n: int, p: PointElement):
        # TODO: check if point is on curve

        e1 = FiniteFieldElement(0, self.a)
        e2 = FiniteFieldElement(0, self.a)
        result = PointElement(e1, e2)
        tmp = p

        for bit in get_daa_bits(n):
            if bit == 1:
                result = result + tmp
            tmp = tmp * 2

        return result

    def non_adjacent_form(self, n: int, p: PointElement):
        # TODO: implement addition and doubling in point-class

        e1 = field.FiniteFieldElement(0, self.a)
        e2 = field.FiniteFieldElement(0, self.a)
        result = PointElement(e1, e2)
        tmp = p

        for bit in get_naf_bits(n):
            if bit == 1:
                result = result + tmp
            tmp = tmp * 2

        return result


if __name__ == '__main__':
    param_a = FiniteFieldElement(2, FiniteField(17))
    param_b = FiniteFieldElement(3, FiniteField(17))
    weierstrass = EllipticCurve(param_a, param_b)
    print(weierstrass)

    element1 = FiniteFieldElement(5, FiniteField(17))
    element2 = FiniteFieldElement(4, FiniteField(17))
    point1 = PointElement(element1, element2)

    # weierstrass.double_and_add(20, point1)
    # weierstrass.non_adjacent_form(20, point1)
