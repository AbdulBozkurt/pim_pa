from finite_field.finite_field_element import FiniteFieldElement
from finite_field.finite_field import FiniteField, get_safe_field
from elliptic_curve import EllipticCurve
from algorithm import get_daa_bits, get_naf_bits
__all__ = ["PointElement"]


class PointElement:
    def __init__(self, x: FiniteFieldElement, y: FiniteFieldElement, z: FiniteFieldElement, curve: EllipticCurve):
        """Initializes an PointElement by providing it with three coordinates of type
        FiniteFieldElement and the corresponding curve. Checks first, whether the fields of the
        given elements are equal. If they are not equal, then raise ValueError."""
        if x.field != y.field:
            raise ValueError('The bases of  the given elements are not equal.')
        self.x = x
        self.y = y
        self.z = z
        self.curve = curve

    def __str__(self) -> str:
        return "(Point: ({0}:{1}:{2}))".format(self.x.e, self.y.e, self.z.e)

    def __add__(self, other: "PointElement") -> "PointElement":
        """Adds two points to retrieve a new one.
        Performs different calculations depending on the coordinates.
        """
        if not self.is_on_curve() or not other.is_on_curve():
            raise ValueError('One or more points are not on the curve.')

        # handles addition with Point at Infinity
        if self.z.e == 0 and other.z.e == 0:
            return self.point_at_infinity()
        elif self.z != other.z:
            if other.z.e == 0:
                return self
            else:
                return other

        if self.x != other.x:
            slope = (other.y - self.y) / (other.x - self.x)
            x3 = slope * slope - self.x - other.x
            y3 = slope * (self.x - x3) - self.y
            return PointElement(x3, y3, self.z, self.curve)
        elif self == other and self.y != 0:
            tmp1 = FiniteFieldElement(3, self.x.field)
            tmp2 = FiniteFieldElement(2, self.x.field)
            slope = (tmp1 * self.x * self.x + self.curve.a) / (tmp2 * self.y)
            x3 = slope * slope - self.x - self.x
            y3 = slope * (self.x - x3) - self.y
            return PointElement(x3, y3, self.z, self.curve)
        else:
            return self.point_at_infinity()

    def __sub__(self, other: "PointElement") -> "PointElement":
        """Calculates the subtraction of two points."""
        return self + (-other)

    def __neg__(self) -> "PointElement":
        """Calculates the negation of a point by multiplying its y-coordinate with -1."""
        i = FiniteFieldElement(-1, self.y.field)
        return PointElement(self.x, self.y * i, self.z, self.curve)

    def __eq__(self, other: "PointElement") -> bool:
        """Checks, whether the point is equal to another one."""
        return self.x == other.x and self.y == other.y and self.z == other.z and self.curve == other.curve

    def __mul__(self, other: int) -> "PointElement":
        """Calculates the scalar product of the point with a given Integer
        in a more efficient way by using the double-and-add-algorithm.
        INSERT DESCRIPTION HERE"""
        if not self.is_on_curve():
            raise ValueError('The given point is not on the curve.')
        if other < 1:
            raise ValueError('n must be a positive integer.')

        result = self.point_at_infinity()
        tmp = self

        for i in get_daa_bits(other):
            if i == 1:
                result = result + tmp
            tmp = tmp + tmp
        return result

    def __rmul__(self, other: int) -> "PointElement":
        return self * other

    def point_at_infinity(self) -> "PointElement":
        x3 = FiniteFieldElement(0, self.x.field)
        y3 = FiniteFieldElement(1, self.y.field)
        z3 = FiniteFieldElement(0, self.z.field)
        return PointElement(x3, y3, z3, self.curve)

    def is_on_curve(self) -> bool:
        """Checks, whether the point is on its elliptic curve, by inserting them
        into the curve. If both sides of the equation are not equal,
        then raise ValueError."""
        left = self.y * self.y * self.z
        right = (self.x * self.x * self.x
                 + self.curve.a * self.x * self.z * self.z
                 + self.curve.b * self.z * self.z * self.z)
        return left == right

    def scalar_mul(self, n: int) -> "PointElement":
        """Calculates the scalar product of the point with a given Integer
        by adding the point to itself."""
        if not self.is_on_curve():
            raise ValueError('The given point is not on the curve.')
        if n < 1:
            raise ValueError('n must be a positive integer.')

        tmp = self
        for i in range(n - 1):
            tmp = tmp + self
        return tmp

    def double_and_add(self, n: int) -> "PointElement":
        """Calculates the scalar product of the point with a given Integer
        in a more efficient way by using the double-and-add-algorithm.
        INSERT DESCRIPTION HERE"""
        if not self.is_on_curve():
            raise ValueError('The given point is not on the curve.')
        if n < 1:
            raise ValueError('n must be a positive integer.')

        result = self.point_at_infinity()
        tmp = self

        for i in get_daa_bits(n):
            if i == 1:
                result = result + tmp
            tmp = tmp + tmp
        return result

    def non_adjacent_form(self, n: int) -> "PointElement":
        """Calculates the scalar product of the point with a given Integer
        in a more efficient way by using the non-adjacent-form.
        INSERT DESCRIPTION HERE"""
        if not self.is_on_curve():
            raise ValueError('The given point is not on the curve.')
        if n < 1:
            raise ValueError('n must be a positive integer.')

        # TODO: implement
        result = self.point_at_infinity()
        tmp = self

        for i in get_naf_bits(n):
            if i == 1:
                result = result + tmp
            tmp = tmp + tmp

        return result

    def generate_sub_group(self) -> list:
        """Generates all unique points, that can be calculated by adding
        the point to itself."""
        # TODO: check if prime
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

    def serialize(self):
        return f"{self.x.e} {self.y.e} {self.z.e}"

    @staticmethod
    def deserialize(string_representation: str, curve: EllipticCurve) -> "PointElement":
        x, y, z = tuple(FiniteFieldElement(int(i), curve.field) for i in string_representation.split(" "))
        return PointElement(x, y, z, curve)


if __name__ == '__main__':
    field = get_safe_field()
    a = 340282366762482138434845932244680310780
    b = 308990863222245658030922601041482374867
    curve_param_a = FiniteFieldElement(a, field)
    curve_param_b = FiniteFieldElement(b, field)
    curve1 = EllipticCurve(curve_param_a, curve_param_b)

    e1 = 29408993404948928992877151431649155974  # x-coordinate
    e2 = 275621562871047521857442314737465260675  # y-coordinate
    e3 = 1  # z-coordinate
    element1 = FiniteFieldElement(e1, field)
    element2 = FiniteFieldElement(e2, field)
    element3 = FiniteFieldElement(e3, field)
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
    print("%s*P1: %s" % (9, 9 * p1))
    print("%s*P1 (scalar): %s" % (9, p1.scalar_mul(9)))
    print("%s*P1 (daa): %s" % (9, p1.double_and_add(9)))
    print("%s*P1 (naf): %s" % (9, p1.non_adjacent_form(9)))
    print("Order of Subgroup of P1: %s" % p1.generate_sub_group()[1])
