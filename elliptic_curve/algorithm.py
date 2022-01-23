def get_daa_bits(n):
    while n:
        yield n & 1
        n >>= 1


def get_naf_bits(n):
    return
