def multiply(a, b):
    # initialize result polynom-array with length a + b
    result = [0 for x in range(len(a) + len(b) - 1)]
    for i, a_element in enumerate(a):
        for j, b_element in enumerate(b):
            result[i+j] += a_element * b_element
    return result


def add(a: list, b: list, p: int) -> list:
    if len(a) < len(b):
        temp = b.copy()
        b = a.copy()
        a = temp
    b = list(reversed(b))
    for i in range(len(a)-len(b)):
        b.append(0)

    result = list()
    for i, e in enumerate(reversed(b)):
        result.append((e + a[i]) % p)
    return result


def clean_list(a: list) -> list:
    """Cleans a list defining a polynom of all leading zeros"""
    while a[0] == 0:
        a.pop(0)
    return a


def reduce(a: list, polynom: list, p: int) -> list:
    # clean the given lists of leading zeros
    a = clean_list(a)
    polynom = clean_list(polynom)

    # generate the reducing-polynom
    r_pol = list()
    for f in polynom[1:]:
        index = (-f * pow(polynom[0], -1, p)) % p
        r_pol.append(index)

    while len(a) >= len(polynom):
        factor = a[0]
        a[0] = 0
        temp = [0 for x in range(len(a))]
        temp[len(polynom)-1] = factor
        temp = multiply(temp, r_pol)
        a = add(a, temp, p)
        a = clean_list(a)

    return a


def generate_poly(factors: dict, p: int) -> list:
    poly = [0 for x in range(max(factors)+1)]
    for i in factors:
        poly[i] = factors[i] % p
    return list(reversed(poly))


if __name__ == '__main__':
    temp = {128: 2, 97: -2, 0: -1}
    p = 340282366762482138434845932244680310783
    fp = generate_poly(temp, p)

    temp = {154: 1241, 152: 41351345}
    a = generate_poly(temp, p)
    res = reduce(a, fp, p)
    print(res)

    # 170141183381241069217422966122340155392

