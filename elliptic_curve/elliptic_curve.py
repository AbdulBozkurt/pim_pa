from finite_field.finite_field_element import FiniteFieldElement
__all__ = ["EllipticCurve"]


class EllipticCurve:

    def __init__(self, a: FiniteFieldElement, b: FiniteFieldElement):
        """Initializes an EllipticCurve by providing it with two parameters of type
        FiniteFieldElement. Checks first, whether the discriminant of the given
        parameters are not equal to 0. If they are equal to 0, then raise ValueError."""
        e1 = FiniteFieldElement([-1], a.field)
        e2 = FiniteFieldElement([4], a.field)
        e3 = FiniteFieldElement([27], a.field)
        discriminant = e1 * (e2 * (a * a * a) + e3 * (b * b))

        if discriminant.e == 0:
            raise ValueError('The determinant -(4{0}^3 + 27{1}^2) equals 0.'.format(a, b))
        self.a = a
        self.b = b
        self.field = a.field

    def __str__(self):
        return "(Curve: y^2 = x^3 + {0}x + {1})".format(self.a.e, self.b.e)

    def __eq__(self, other):
        """Checks, whether the curve is equal to another one."""
        return self.a == other.a and self.b == other.b
