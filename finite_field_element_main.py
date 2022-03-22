from finite_field.finite_field import get_safe_field
from finite_field.finite_field_element import FiniteFieldElement

e1 = FiniteFieldElement([10], get_safe_field())
e2 = FiniteFieldElement([3], get_safe_field())
print(e1+e2)
print(e1-e2)
print(e1*e2)
