from finite_field.finite_field import generate_poly, FiniteField
from finite_field.finite_field_element import FiniteFieldElement

if __name__ == '__main__':
    temp_poly = {3: 1, 2: 1, 1: 3, 0: 1}
    p = 7
    poly = generate_poly(temp_poly, p)
    field = FiniteField(p, poly)

    temp_poly = {4: 16, 3: 24, 2: 49, 1: 30, 0: 25}
    p = 7
    poly = generate_poly(temp_poly, p)

    print(FiniteFieldElement(poly, field))
