import sys
import os
__all__ = ["EllipticCurve", "FiniteField", "PointElement", "FiniteFieldElement", "curve1", "p1", "ip", "port",
           "sub_group_size", "verbose"]

# change the following values, if you want to change the ip, port, or if you enable/disable verbose printing
ip = "127.0.0.1"
port = 10666
verbose = True

sys.path.insert(0, os.getcwd())
sys.path.append("..")

import elliptic_curve.elliptic_curve
import elliptic_curve.point_element
import finite_field.finite_field
import finite_field.finite_field_element

EllipticCurve = elliptic_curve.elliptic_curve.EllipticCurve
FiniteField = finite_field.finite_field.FiniteField
PointElement = elliptic_curve.point_element.PointElement
FiniteFieldElement = finite_field.finite_field_element.FiniteFieldElement

field = FiniteField(340282366762482138434845932244680310783)
curve_param_a = FiniteFieldElement(340282366762482138434845932244680310780, field)
curve_param_b = FiniteFieldElement(308990863222245658030922601041482374867, field)
curve1 = EllipticCurve(curve_param_a, curve_param_b)
element1 = FiniteFieldElement(29408993404948928992877151431649155974, field)
element2 = FiniteFieldElement(275621562871047521857442314737465260675, field)
element3 = FiniteFieldElement(1, field)
p1 = PointElement(element1, element2, element3, curve1)
sub_group_size = 340282366762482138443322565580356624661  # p1.generate_sub_group()[1]
