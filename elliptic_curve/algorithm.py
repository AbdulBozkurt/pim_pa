def get_daa_bits(n: int):
    """ Generates the binary digits of n, starting
    from the least significant bit."""
    while n:
        yield n & 1
        n >>= 1


def get_naf_bits(n: int):
    # TODO: implement naf
    """ Generates the binary digits of n, starting
    from the least significant bit."""
    while n:
        yield n & 1
        n >>= 1
