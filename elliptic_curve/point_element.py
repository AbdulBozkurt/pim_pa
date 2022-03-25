import json

from elliptic_curve.elliptic_curve import EllipticCurve
from finite_field.finite_field_element import FiniteFieldElement

__all__ = ["PointElement"]


def get_daa_bits(n: int):
    """ Generates the binary digits of n, starting
    from the least significant bit."""
    while n:
        yield n & 1
        n >>= 1


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
        return "(Point: ({0}:{1}:{2}))".format(self.x, self.y, self.z)

    # noinspection PyPep8Naming
    def __add__(self, other: "PointElement") -> "PointElement":
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

        if self.x != other.x:
            tmp2 = FiniteFieldElement([2], self.x.field)
            # 14M for addition: 12M + 2S
            y1z2 = self.y * other.z
            x1z2 = self.x * other.z
            z1z2 = self.z * other.z
            u = other.y * self.z - y1z2
            uu = u * u
            v = other.x * self.z - x1z2
            vv = v * v
            vvv = v * vv
            R = vv * x1z2
            A = uu * z1z2 - vvv - tmp2 * R
            x3 = v * A
            y3 = u * (R-A) - vvv * y1z2
            z3 = vvv * z1z2

            return PointElement(x3, y3, z3, self.curve)

        elif self == other and self.y != 0:
            tmp3 = FiniteFieldElement([3], self.x.field)
            tmp2 = FiniteFieldElement([2], self.x.field)
            # 11M for doubling: 5M + 6S
            xx = self.x * self.x
            zz = self.z * self.z
            w = self.curve.a * zz + tmp3 * xx
            s = tmp2 * self.y * self.z
            ss = s * s
            sss = s * ss
            R = self.y * s
            RR = R * R
            B = (self.x + R) * (self.x + R) - xx - RR
            h = w * w - tmp2 * B
            x3 = h * s
            y3 = w * (B-h) - tmp2 * RR
            z3 = sss

            return PointElement(x3, y3, z3, self.curve)

        else:
            return self.point_at_infinity()

    def __sub__(self, other: "PointElement") -> "PointElement":
        """Calculates the subtraction of two points."""
        return self + (-other)

    def __neg__(self) -> "PointElement":
        """Calculates the negation of a point by multiplying its y-coordinate with -1."""
        i = FiniteFieldElement([-1], self.y.field)
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
        x3 = FiniteFieldElement([0], self.x.field)
        y3 = FiniteFieldElement([1], self.y.field)
        z3 = FiniteFieldElement([0], self.z.field)
        return PointElement(x3, y3, z3, self.curve)

    def is_on_curve(self) -> bool:
        """Checks, whether the point is on its elliptic curve, by inserting them
        into the curve. If both sides of the equation are not equal,
        then raise ValueError."""
        left = (self.y * self.y * self.z)
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

    def generate_sub_group(self) -> list:
        """Generates all unique points, that can be calculated by adding
        the point to itself."""

        tmp = self
        sub_group = [tmp]
        while tmp != self.point_at_infinity():
            tmp = self + tmp
            sub_group.append(tmp)
        return sub_group

    def serialize(self):
        return json.dumps({"x": self.x.e, "y": self.y.e, "z": self.z.e})

    @staticmethod
    def deserialize(string_representation: str, curve: EllipticCurve) -> "PointElement":
        json_dict = json.loads(string_representation)
        x = FiniteFieldElement(json_dict['x'], curve.field)
        y = FiniteFieldElement(json_dict['y'], curve.field)
        z = FiniteFieldElement(json_dict['z'], curve.field)

        return PointElement(x, y, z, curve)
