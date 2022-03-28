from finite_field.finite_field import get_safe_field, FiniteField
from finite_field.finite_field_element import FiniteFieldElement


if __name__ == '__main__':
    field = FiniteField(11, [1, 2, 3])
    e1 = FiniteFieldElement([1], field)
    e2 = FiniteFieldElement([3, 0, 2, 4], field)
    print(e1/e2)
