__all__ = ["prime_test"]

import random


def prime_test(p: int) -> bool:
    """Checks, whether a given integer p is prime"""
    for i in range(100):
        a = random.randrange(1, p-1)
        if pow(a, p-1, p) != 1:
            return False
    return True


def find_prime(bit: int) -> int:
    """Finds and returns a prime number with the specified bit-length"""
    n = 0
    r = 2**bit
    while True:
        n = random.randrange(r//4, r)
        if prime_test(n):
            break
    return n


if __name__ == "__main__":
    print(find_prime(128))
