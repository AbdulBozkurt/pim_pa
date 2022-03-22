from elliptic_curve.elliptic_curve import EllipticCurve
from finite_field.finite_field import get_safe_field
from finite_field.finite_field_element import FiniteFieldElement

field = get_safe_field()
param_a = FiniteFieldElement([2], get_safe_field())
param_b = FiniteFieldElement([3], get_safe_field())
weierstrass = EllipticCurve(param_a, param_b)
print(weierstrass)
