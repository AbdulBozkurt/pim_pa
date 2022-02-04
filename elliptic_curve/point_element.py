from finite_field.finite_field_element import FiniteFieldElement
from finite_field.finite_field import FiniteField


class PointElement:

    def __init__(self, x: FiniteFieldElement, y: FiniteFieldElement):

        if x.field != y.field:
            raise ValueError('The bases of  the given elements are not equal.')
        self.x = x
        self.y = y
        # TODO: inherit A from elliptic curve
        self.a = FiniteFieldElement(2, x.field)

    def __str__(self):
        return "(Point: ({0}|{1}) )".format(self.x.e, self.y.e)

    def __add__(self, other):
        # TODO: use this or the formulas from http://hyperelliptic.org ?
        if self.x != other.x:
            slope = (other.y - self.y) / (other.x - self.x)
            x3 = slope * slope - self.x - other.x
            y3 = slope * (self.x - x3) - self.y
            return PointElement(x3, y3)

        elif self == other and self.y != 0:
            e1 = FiniteFieldElement(3, self.x.field)
            e2 = FiniteFieldElement(2, self.x.field)
            slope = (e1 * self.x * self.x + self.a) / (e2 * self.y)
            x3 = slope * slope - self.x - self.x
            y3 = slope * (self.x - x3) - self.y
            return PointElement(x3, y3)
        else:
            # TODO: rather raising error or handle infinity with projective coordinates ?
            raise ValueError('Point at Infinity')

    def __sub__(self, other):
        return self + (-other)

    def __neg__(self):
        i = FiniteFieldElement(-1, self.y.field)
        return PointElement(self.x, self.y * i)


if __name__ == '__main__':
    element1 = FiniteFieldElement(3, FiniteField(17))
    element2 = FiniteFieldElement(5, FiniteField(17))
    p1 = PointElement(element1, element2)
    p2 = PointElement(element2, element1)
    print(p1)
    print(-p1)
    print(p1+p2)
    print(p1-p2)
