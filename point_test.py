from elliptic_curve.elliptic_curve import EllipticCurve
from elliptic_curve.point_element import PointElement
from finite_field.finite_field import get_safe_field, generate_poly, FiniteField
from finite_field.finite_field_element import FiniteFieldElement

#   Polynomial of degree 19 over F_103
temp_poly = {3: 1, 2: 1, 1: 3, 0: 1}
p = 7
poly = generate_poly(temp_poly, p)
field = FiniteField(p, poly)

#   Elliptic Curve over F_p^k
a = generate_poly({4: 1}, p)  # curve-parameter a = x^4
b = generate_poly({6: 1}, p)  # curve-parameter b = x^6
curve_param_a = FiniteFieldElement(a, field)
curve_param_b = FiniteFieldElement(b, field)
curve = EllipticCurve(curve_param_a, curve_param_b)

#   Generator of the Elliptic Curve
e1 = generate_poly({1: 3, 0: 4}, p)
e2 = generate_poly({2: 6, 1: 3, 0: 1}, p)
e3 = generate_poly({0: 1}, p)
element1 = FiniteFieldElement(e1, field)
element2 = FiniteFieldElement(e2, field)
element3 = FiniteFieldElement(e3, field)
generator = PointElement(element1, element2, element3, curve)

added = generator + generator + generator + generator + generator + generator + generator + generator + generator + generator
amul = 10*generator

print("P2 on curve: %s" % added.is_on_curve(), amul.is_on_curve())
