from elliptic_curve.elliptic_curve import *
from elliptic_curve.point_element import *
from finite_field.finite_field import *
from finite_field.finite_field_element import *

__all__ = ["EllipticCurve", "FiniteField", "PointElement", "FiniteFieldElement", "curve1", "q", "ip", "port",
           "sub_group_size", "verbose"]

# change the following values, if you want to change the ip, port, or if you enable/disable verbose printing
ip = "127.0.0.1"
port = 10666
verbose = True

field = get_safe_field()

a = generate_poly({4: 1}, field.p)  # curve-parameter a
b = generate_poly({6: 1}, field.p)  # curve-parameter b
curve_param_a = FiniteFieldElement(a, field)
curve_param_b = FiniteFieldElement(b, field)
curve1 = EllipticCurve(curve_param_a, curve_param_b)

#   Generator of the Elliptic Curve
e1 = generate_poly({18: 25, 17: 8, 16: 31, 15: 62, 14: 36, 13: 66, 12: 48, 11: 44, 10: 70,
                    9: 89, 8: 40, 7: 28, 6: 1, 5: 2, 4: 16, 3: 58, 2: 29, 1: 12, 0: 24}, field.p)
e2 = generate_poly({18: 71, 17: 15, 16: 98, 15: 41, 14: 85, 13: 6, 12: 6, 11: 62, 10: 63,
                    9: 71, 8: 87, 7: 34, 6: 68, 5: 38, 4: 58, 3: 2, 2: 16, 1: 8, 0: 70}, field.p)
e3 = generate_poly({0: 1}, field.p)
element1 = FiniteFieldElement(e1, field)
element2 = FiniteFieldElement(e2, field)
element3 = FiniteFieldElement(e3, field)
q = PointElement(element1, element2, element3, curve1)

sub_group_size = 175350605307710078811724140841853552259
