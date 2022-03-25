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

p1 = 18374 * generator
print(generator)
print(p1)
print(generator.is_on_curve())
print(p1.is_on_curve())
# p2 = p1 + p1
# p3 = p1 - p2
# p4 = p2 + p2
# p5 = p1 - p1
# scalar = 34
# p6 = scalar * p1
#
# print(" P1: %s" % p1)
# print("-P1: %s" % -p1)
# print(" P2: %s" % p2)
# print("P1-P2: %s" % p3)
# print("P2+P2: %s" % p4)
# print("P1-P1: %s" % p5)
# print("%s*P1: %s\n" % (scalar, p6))
#
# print("P1 on curve: %s" % p1.is_on_curve())
# print("P2 on curve: %s" % p2.is_on_curve())
# print("P1-P2 on curve: %s" % p3.is_on_curve())
# print("P2+P2 on curve: %s" % p4.is_on_curve())
# print("P1-P1 on curve: %s" % p5.is_on_curve())
# # Point: ([111614102573067424927652398299318724279]:[171041964748245813741138639535351797219])
# print("%s*P1 on curve: %s" % (scalar, p6.is_on_curve()))
