from finite_field.finite_field_element import FiniteFieldElement
from finite_field.finite_field import FiniteField
from elliptic_curve import EllipticCurve
from algorithm import get_daa_bits, get_naf_bits


class PointElement:
    def __init__(self, x: FiniteFieldElement, y: FiniteFieldElement, z: FiniteFieldElement, curve: EllipticCurve):
        """Initializes an PointElement by providing it with two (later three) coordinates of type
        FiniteFieldElement and the corresponding curve. Checks first, whether the fields of the
        given elements are equal. If they are not equal, then raise ValueError."""
        if x.field != y.field:
            raise ValueError('The bases of  the given elements are not equal.')
        self.x = x
        self.y = y
        self.z = z
        self.curve = curve

    def __str__(self):
        return "(Point: ({0}:{1}:{2}))".format(self.x.e, self.y.e, self.z.e)

    def __add__(self, other):
        """Adds two points to retrieve a new one.
        Performs different calculations depending on the coordinates.
        """
        # if not self.is_on_curve() or not other.is_on_curve():
        #     raise ValueError('One or more points are not on the curve.')

        # handles addition with Point at Infinity
        if self.z.e == 0 and other.z.e == 0:
            return self.point_at_infinity()
        elif self.z != other.z:
            if other.z.e == 0:
                return self
            else:
                return other

        # TODO: use this or the formulas from http://hyperelliptic.org ?
        # TODO: check which formulas are the most efficient
        if self.x != other.x:
            slope = (other.y - self.y) / (other.x - self.x)
            x3 = slope * slope - self.x - other.x
            y3 = slope * (self.x - x3) - self.y
            return PointElement(x3, y3, self.z, self.curve)
        elif self == other and self.y != 0:
            e1 = FiniteFieldElement(3, self.x.field)
            e2 = FiniteFieldElement(2, self.x.field)
            slope = (e1 * self.x * self.x + self.curve.a) / (e2 * self.y)
            x3 = slope * slope - self.x - self.x
            y3 = slope * (self.x - x3) - self.y
            return PointElement(x3, y3, self.z, self.curve)
        else:
            return self.point_at_infinity()

    def __sub__(self, other):
        """Calculates the subtraction of two points."""
        return self + (-other)

    def __neg__(self):
        """Calculates the negation of a point by multiplying its y-coordinate with -1."""
        i = FiniteFieldElement(-1, self.y.field)
        return PointElement(self.x, self.y * i, self.z, self.curve)

    def __eq__(self, other):
        """Checks, whether the point is equal to another one."""
        return self.x == other.x and self.y == other.y and self.z == other.z and self.curve == other.curve

    def point_at_infinity(self):
        x3 = FiniteFieldElement(0, self.x.field)
        y3 = FiniteFieldElement(1, self.y.field)
        z3 = FiniteFieldElement(0, self.z.field)
        return PointElement(x3, y3, z3, self.curve)

    def is_on_curve(self):
        """Checks, whether the point is on its elliptic curve, by inserting them
        into the curve. If both sides of the equation are not equal,
        then raise ValueError."""
        # TODO: eq-method in finite_field_element?
        left = self.y * self.y * self.z
        right = (self.x * self.x * self.x
                 + self.curve.a * self.x * self.z * self.z
                 + self.curve.b * self.z * self.z * self.z)
        return left.field == right.field and left.e == right.e

    def scalar_mul(self, n: int):
        """Calculates the scalar product of the point with a given Integer
        by adding the point to itself."""
        # if not self.is_on_curve():
        #     raise ValueError('The given point is not on the curve.')

        tmp = self
        for i in range(n - 1):
            tmp = tmp + self
        return tmp

    def double_and_add(self, n: int):
        """Calculates the scalar product of the point with a given Integer
        in a more efficient way by using the double-and-add-algorithm.
        INSERT DESCRIPTION HERE"""
        # if not self.is_on_curve():
        #     raise ValueError('The given point is not on the curve.')

        result = self.point_at_infinity()
        tmp = self

        for i in get_daa_bits(n):
            if i == 1:
                result = result + tmp
            tmp = tmp + tmp
        return result

    def non_adjacent_form(self, n: int):
        """Calculates the scalar product of the point with a given Integer
        in a more efficient way by using the non-adjacent-form.
        INSERT DESCRIPTION HERE"""
        if not self.is_on_curve():
            raise ValueError('The given point is not on the curve.')

        # TODO: implement
        result = self.point_at_infinity()
        tmp = self

        for i in get_naf_bits(n):
            if i == 1:
                result = result + tmp
            tmp = tmp + tmp

        return result

    def generate_sub_group(self):
        """Generates all unique points, that can be calculated by adding
        the point to itself."""
        tmp = self
        sub_group = [tmp]
        while tmp != self.point_at_infinity():
            tmp = self + tmp
            sub_group.append(tmp)
        return sub_group

    def get_generator(self):
        """Calculates the generator of an elliptic curve by finding the
        point, that equals the amount of points on its curve."""
        return


if __name__ == '__main__':
    curve_param_a = FiniteFieldElement(2, FiniteField(13))
    curve_param_b = FiniteFieldElement(3, FiniteField(13))
    curve1 = EllipticCurve(curve_param_a, curve_param_b)

    element1 = FiniteFieldElement(4, FiniteField(13))
    element2 = FiniteFieldElement(7, FiniteField(13))
    element3 = FiniteFieldElement(1, FiniteField(13))
    p1 = PointElement(element1, element2, element3, curve1)
    p2 = p1 + p1

    print("P1 on curve: %s" % p1.is_on_curve())
    print("P2 on curve: %s" % p2.is_on_curve())
    print(" P1: %s" % p1)
    print("-P1: %s" % -p1)
    print("P1+P1: %s" % (p1 + p1))
    print("P1+P2: %s" % (p1 + p2))
    print("P1-P2: %s" % (p1 - p2))
    print("P1-P1: %s" % (p1 - p1))
    print("%s*P1 (scalar): %s" % (9, p1.scalar_mul(9)))
    print("%s*P1 (daa): %s" % (9, p1.double_and_add(9)))
    print("%s*P1 (naf): %s" % (9, p1.non_adjacent_form(9)))
    print("Order of Subgroup of P1: %s" % len(p1.generate_sub_group()))
