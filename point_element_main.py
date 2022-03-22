from elliptic_curve.elliptic_curve import EllipticCurve
from elliptic_curve.point_element import PointElement
from finite_field.finite_field import get_safe_field
from finite_field.finite_field_element import FiniteFieldElement

field = get_safe_field()
a = 340282366762482138434845932244680310780  # curve-parameter a
b = 308990863222245658030922601041482374867  # curve-parameter b
curve_param_a = FiniteFieldElement([a], field)
curve_param_b = FiniteFieldElement([b], field)
curve1 = EllipticCurve(curve_param_a, curve_param_b)

e1 = 29408993404948928992877151431649155974  # x-coordinate
e2 = 275621562871047521857442314737465260675  # y-coordinate
e3 = 1  # z-coordinate
element1 = FiniteFieldElement([e1], field)
element2 = FiniteFieldElement([e2], field)
element3 = FiniteFieldElement([e3], field)
p1 = PointElement(element1, element2, element3, curve1)
p2 = p1 + p1
p3 = p1 - p2
p4 = p2 + p2
p5 = p1 - p1
scalar = 340282366762482138443322565580356624661
p6 = scalar * p1

print(" P1: %s" % p1)
print("-P1: %s" % -p1)
print(" P2: %s" % p2)
print("P1-P2: %s" % p3)
print("P2+P2: %s" % p4)
print("P1-P1: %s" % p5)
print("%s*P1: %s\n" % (scalar, p6))

print("P1 on curve: %s" % p1.is_on_curve())
print("P2 on curve: %s" % p2.is_on_curve())
print("P1-P2 on curve: %s" % p3.is_on_curve())
print("P2+P2 on curve: %s" % p4.is_on_curve())
print("P1-P1 on curve: %s" % p5.is_on_curve())
# Point: ([111614102573067424927652398299318724279]:[171041964748245813741138639535351797219])
print("%s*P1 on curve: %s" % (scalar, p6.is_on_curve()))
# print("%s*P1 (scalar): %s" % (scalar, p1.scalar_mul(scalar)))
# print("%s*P1 (daa): %s" % (scalar, p1.double_and_add(scalar)))
# print("Order of Subgroup of P1: %s" % len(p1.generate_sub_group()))
