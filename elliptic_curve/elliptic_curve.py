from finite_field.finite_field_element import FiniteFieldElement
from finite_field.finite_field import FiniteField


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

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b


if __name__ == '__main__':
    param_a = FiniteFieldElement(2, FiniteField(17))
    param_b = FiniteFieldElement(3, FiniteField(17))
    weierstrass = EllipticCurve(param_a, param_b)
    print(weierstrass)
