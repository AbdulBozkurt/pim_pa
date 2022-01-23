import finite_field.finite_field_element as field
import point_element as point
from algorithm import get_daa_bits, get_naf_bits


class EllipticCurve:

    def __init__(self, a: field. FiniteFieldElement, b: field.FiniteFieldElement,
                 x: field. FiniteFieldElement, y: field.FiniteFieldElement):

        e1 = field.FiniteFieldElement(-1, a.p)
        e2 = field.FiniteFieldElement(4, a.p)
        e3 = field.FiniteFieldElement(27, a.p)
        determinant = e1 * (e2 * (a * a * a) + e3 * (b * b))

        if determinant.e == 0:
            raise ValueError('The determinant -(4{0}^3 + 27{1}^2) equals 0.'.format(a, b))
        self.a = a
        self.b = b
        self.p = a.p

    def __str__(self):
        return "(Curve: y^2 = x^3 + {0}x + {1})".format(self.a.e, self.b.e)

    def double_and_add(self, n: int, p: point.PointElement):
        # TODO: implement addition and doubling in point-class

        e1 = field.FiniteFieldElement(0, self.p)
        e2 = field.FiniteFieldElement(0, self.p)
        result = point.PointElement(e1, e2)
        tmp = p

        for bit in get_daa_bits(n):
            if bit == 1:
                result = result + tmp
            tmp = tmp * 2

        return result

    def non_adjacent_form(self, n: int, p: point.PointElement):
        # TODO: implement addition and doubling in point-class

        e1 = field.FiniteFieldElement(0, self.p)
        e2 = field.FiniteFieldElement(0, self.p)
        result = point.PointElement(e1, e2)
        tmp = p

        for bit in get_naf_bits(n):
            if bit == 1:
                result = result + tmp
            tmp = tmp * 2

        return result


if __name__ == '__main__':
    param_a = field.FiniteFieldElement(2, 17)
    param_b = field.FiniteFieldElement(3, 17)
    element1 = field.FiniteFieldElement(5, 17)
    element2 = field.FiniteFieldElement(4, 17)
    p1 = EllipticCurve(param_a, param_b, element1, element2)
    print(p1)
