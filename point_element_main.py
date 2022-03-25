from elliptic_curve.elliptic_curve import EllipticCurve
from elliptic_curve.point_element import PointElement
from finite_field.finite_field import get_safe_field, generate_poly, FiniteField
from finite_field.finite_field_element import FiniteFieldElement

#   Polynomial of degree 19 over F_103
temp_poly = {19: 1, 18: 1, 17: 13, 16: 46, 15: 57, 14: 94, 13: 7, 12: 19, 11: 100, 10: 15,
             9: 15, 8: 51, 7: 66, 6: 82, 5: 8, 4: 92, 3: 4, 2: 3, 1: 1, 0: 80}
p = 103
poly = generate_poly(temp_poly, p)
field = FiniteField(p, poly)

#   Elliptic Curve over F_p^k
a = generate_poly({4: 1}, p)  # curve-parameter a = x^4
b = generate_poly({6: 1}, p)  # curve-parameter b = x^6
curve_param_a = FiniteFieldElement(a, field)
curve_param_b = FiniteFieldElement(b, field)
curve = EllipticCurve(curve_param_a, curve_param_b)

#   Generator of the Elliptic Curve
e1 = generate_poly({18: 25, 17: 8, 16: 31, 15: 62, 14: 36, 13: 66, 12: 48, 11: 44, 10: 70,
                    9: 89, 8: 40, 7: 28, 6: 1, 5: 2, 4: 16, 3: 58, 2: 29, 1: 12, 0: 24}, p)
e2 = generate_poly({18: 71, 17: 15, 16: 98, 15: 41, 14: 85, 13: 6, 12: 6, 11: 62, 10: 63,
                    9: 71, 8: 87, 7: 34, 6: 68, 5: 38, 4: 58, 3: 2, 2: 16, 1: 8, 0: 70}, p)
e3 = generate_poly({0: 1}, p)
element1 = FiniteFieldElement(e1, field)
element2 = FiniteFieldElement(e2, field)
element3 = FiniteFieldElement(e3, field)
generator = PointElement(element1, element2, element3, curve)

#   Another Point on the Elliptic Curve
e1 = generate_poly({18: 4, 17: 60, 16: 52, 15: 16, 14: 93, 13: 52, 12: 65, 11: 68, 10: 30,
                    9: 32, 8: 34, 7: 100, 6: 30, 5: 69, 4: 30, 3: 23, 2: 7, 1: 58, 0: 35}, p)
e2 = generate_poly({18: 61, 17: 76, 16: 31, 15: 29, 14: 66, 13: 73, 12: 81, 11: 7, 10: 93,
                    9: 83, 8: 2, 7: 48, 6: 87, 5: 52, 4: 39, 3: 67, 2: 16, 1: 13, 0: 85}, p)
e3 = generate_poly({0: 1}, p)
element1 = FiniteFieldElement(e1, field)
element2 = FiniteFieldElement(e2, field)
element3 = FiniteFieldElement(e3, field)
p1 = PointElement(element1, element2, element3, curve)
added = generator + generator + generator
amultiplied = 3*generator
# print("Generator: %s" % generator)
# print("P1: %s" % p1)
print("P111 on curve: %s" % added.is_on_curve(), amultiplied.is_on_curve())
