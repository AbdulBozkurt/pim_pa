def get_daa_bits(n: int):
    """ Generates the binary digits of n, starting
    from the least significant bit."""
    while n:
        yield n & 1
        n >>= 1
