import finite_field.finite_field_element as field


class PointElement:

    def __init__(self, x: field.FiniteFieldElement, y: field.FiniteFieldElement):

        if not x.p == y.p:
            raise ValueError('The bases of  the given elements are not equal.')

        self.x = x
        self.y = y

    def __str__(self):
        return "(Point: ({0}|{1}) )".format(self.x.e, self.y.e)

    def addition(self, other, a):
        # TODO: eea for inverse of elements

        if self:
            # x
            # slope 1:  y2 - y1 / x2 - x1
            # slope 2:  3 * x1^2 + A / 2 * y1
            return "addition"
        elif other:
            return "doubling"
        else:
            return "point at infinity"


if __name__ == '__main__':
    element1 = field.FiniteFieldElement(3, 17)
    element2 = field.FiniteFieldElement(5, 17)
    p1 = PointElement(element1, element2)
    print(p1)
