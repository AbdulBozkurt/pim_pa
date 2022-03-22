from finite_field.finite_field_element import FiniteFieldElement
__all__ = ["EllipticCurve"]


class EllipticCurve:

    def __init__(self, a: FiniteFieldElement, b: FiniteFieldElement):
        """Initializes an EllipticCurve by providing it with two parameters of type
        FiniteFieldElement. Checks first, whether the determinant of the given
        parameters are not equal to 0. If they are equal to 0, then raise ValueError."""
        e1 = FiniteFieldElement([-1], a.field)
        e2 = FiniteFieldElement([4], a.field)
        e3 = FiniteFieldElement([27], a.field)
        determinant = e1 * (e2 * (a * a * a) + e3 * (b * b))

        if determinant.e == 0:
            raise ValueError('The determinant -(4{0}^3 + 27{1}^2) equals 0.'.format(a, b))
        self.a = a
        self.b = b
        self.field = a.field

    def __str__(self):
        return "(Curve: y^2z = x^3 + {0}xz^2 + {1}z^3)".format(self.a.e, self.b.e)

    def __eq__(self, other):
        """Checks, whether the curve is equal to another one."""
        return self.a == other.a and self.b == other.b
