from typing import Tuple

__all__ = ["mod_add", "mod_sub", "mod_mul", "mod_inv", "mod_div", "euclidean_alg", "extended_euclidean_alg", "mod"]


def normalize_params(x: int, y: int, k: int) -> Tuple[int, int, int]:
    """Normalizes the parameters of a mod arith function.
    This means the first two parameters will be converted to the corresponding representative of their congruence class
    mod k; and k will be checked whether it is greater than 1."""
    if k <= 1:
        raise ValueError(f"Parameter k should not be <= 1. Given: {k}")
    return (x % k), y % k, k


def mod_add(x: int, y: int, k: int) -> int:
    """Calculates (x + y) mod k."""
    x, y, k = normalize_params(x, y, k)
    return (x + y) % k


def mod(x: int, k: int) -> int:
    """Calculates x mod k"""
    return x % k


def _mod(x: int, k: int) -> int:
    """Calculates x mod k (without %)
    Warning: inefficient"""
    if k == 0:
        raise ZeroDivisionError(f"Tried dividing {x} mod {k}")
    if k < 0:
        raise ValueError(f"Modulo division with negative divider not supported")
    return x - ((x // k) * k)  # that's basically x % k


def mod_sub(x: int, y: int, k: int) -> int:
    """Calculates (x - y) mod k."""
    x, y, k = normalize_params(x, y, k)
    return (x - y) % k


def mod_mul(x: int, y: int, k: int) -> int:
    """Calculates (x * y) mod k."""
    x, y, k = normalize_params(x, y, k)
    return (x * y) % k


def mod_inv(x: int, k: int) -> int:
    """Calculates the multiplicative inverse of the congruence class x mod k, if possible.
    If it isn't possible, raise ValueError."""
    x, _, k = normalize_params(x, 1, k)
    d, s, t = extended_euclidean_alg(x, k)
    s %= k
    if d != 1:
        raise ValueError(f"Parameters x = {x} and k = {k} must be mutually prime. GCD was {d}")
    return s


def mod_div(x: int, y: int, k: int) -> int:
    """Calculates (x / y) mod k, if possible.
    If it isn't possible, raise ValueError."""
    x, y, k = normalize_params(x, y, k)
    return (x * mod_inv(y, k)) % k


def extended_euclidean_alg(x: int, y: int) -> Tuple[int, int, int]:
    """Calculates d, t and s via the extended euclidean algorithm, so that d = s * x + t * y."""
    if x < 0:
        raise ValueError(f"Parameter x should not be < 0. Given: {x}")
    if y < 0:
        raise ValueError(f"Parameter y should not be < 0. Given: {y}")
    if x < y:
        d, s, t = extended_euclidean_alg(y, x)
        return d, t, s
    if y == 0:
        return x, 1, 0
    d, s, t = extended_euclidean_alg(y, (x % y))
    return d, t, s - (x // y) * t


def euclidean_alg(x: int, y: int) -> int:
    """Calculates the greatest common divider via the euclidean algorithm."""
    if x < 0:
        raise ValueError(f"Parameter x should not be < 0. Given: {x}")
    if y < 0:
        raise ValueError(f"Parameter y should not be < 0. Given: {y}")
    if x < y:
        x, y = y, x
    while y != 0:
        x, y = y, (x % y)
    return x
