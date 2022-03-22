from elliptic_curve.elliptic_curve import *
from elliptic_curve.point_element import *
from finite_field.finite_field import *
from finite_field.finite_field_element import *

__all__ = ["EllipticCurve", "FiniteField", "PointElement", "FiniteFieldElement", "curve1", "p1", "ip", "port",
           "sub_group_size", "verbose"]

# change the following values, if you want to change the ip, port, or if you enable/disable verbose printing
ip = "127.0.0.1"
port = 10666
verbose = True

field = get_safe_field()

a = 340282366762482138434845932244680310780  # curve-parameter a
b = 308990863222245658030922601041482374867  # curve-parameter b
# a_arr = generate_poly({}, field.p)
# b_arr = generate_poly({}, field.p)
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
sub_group_size = 340282366762482138443322565580356624661
