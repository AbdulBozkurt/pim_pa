import math
import random
from typing import Callable, Tuple

import modarith


def _are_mutually_prime(x: int, k: int) -> bool:
    return True in [(x % i) == 0 and (k % i) == 0 for i in range(2, min(x, k))]


class FuzzingTester:

    def __init__(self, min_rand: int, max_rand: int, n: int):
        self.min_rand = min_rand
        self.max_rand = max_rand
        self.n = n

    def run(self):

        functions = (
            self.test_extended_euclidean,
            self.test_add,
            self.test_sub,
            self.test_mul,
            self.test_inv,
            self.test_div,
            self.test_euclidean,
            self.test_mod,
            self.test_pow
        )

        def get_random_value():
            return random.randint(self.min_rand, self.max_rand)
        failure_count: int = 0
        for i in range(self.n):
            if i % (self.n // 100) == 0:
                percentage = (i * 100) // self.n
                print(f"\r[{percentage: >3}%]: run #[{i: >{len(str(self.n))}}/{self.n}] currently", flush=True, end="")
            x: int = get_random_value()
            y: int = get_random_value()
            k: int = get_random_value()
            func: Callable[[int, int, int], Tuple[Callable, Tuple, int, Exception, str]]
            for func in functions:
                result = func(x, y, k)
                if result is None:
                    continue
                failure_count += 1
                function, params, arithmetic_result, exception, msg = result
                print(f"\rfunction call {function.__name__}{params} returned {arithmetic_result} with "
                      f"error {repr(exception)}. " +
                      (f"Additional message: {msg}" if (msg is not None and len(msg) > 0) else ""), flush=True)

        print(f"\rdone with {failure_count} test failures out of {self.n * len(functions)} (n times the number of "
              f"functions)")

    @staticmethod
    def test_add(x: int, y: int, k: int):
        try:
            result = modarith.mod_add(x, y, k)
        except ValueError as err:
            if k <= 1:
                return
            else:
                return modarith.mod_add, (x, y, k), None, err, ""
        if k <= 1:
            return modarith.mod_add, (x, y, k), result, None, "expected ValueError, because k <= 1"
        if result != (x + y) % k:
            return modarith.mod_add, (x, y, k), result, None, "wrong result"

    @staticmethod
    def test_sub(x: int, y: int, k: int):
        try:
            result = modarith.mod_sub(x, y, k)
        except ValueError as err:
            if k <= 1:
                return
            else:
                return modarith.mod_sub, (x, y, k), None, err, ""
        if k <= 1:
            return modarith.mod_sub, (x, y, k), result, None, "expected ValueError, because k <= 1"
        if result != (x - y) % k:
            return modarith.mod_sub, (x, y, k), result, None, "wrong result"

    @staticmethod
    def test_mul(x: int, y: int, k: int):
        try:
            result = modarith.mod_mul(x, y, k)
        except ValueError as err:
            if k <= 1:
                return
            else:
                return modarith.mod_mul, (x, y, k), None, err, ""
        if k <= 1:
            return modarith.mod_mul, (x, y, k), result, None, "expected ValueError, because k <= 1"
        if result != (x * y) % k:
            return modarith.mod_mul, (x, y, k), result, None, "wrong result"

    # noinspection PyUnusedLocal
    @staticmethod
    def test_inv(x: int, y: int, k: int):
        try:
            result = modarith.mod_inv(x, k)
        except ValueError as err:
            if k <= 1:
                return
            if modarith.euclidean_alg(x % k, k) != 1:
                return
            return modarith.mod_inv, (x, k), None, err, "not mutually prime"
        if k <= 1:
            return modarith.mod_inv, (x, k), result, None, "expected ValueError, because k <= 1"
        if (result * x) % k != 1:
            return modarith.mod_inv, (x, k), result, None, "multiplication does not result in 1"

    @staticmethod
    def test_div(x: int, y: int, k: int):
        try:
            result = modarith.mod_div(x, y, k)
        except ValueError as err:
            if k <= 1:
                return
            if modarith.euclidean_alg(y % k, k) != 1:
                return
            return modarith.mod_div, (x, y, k), None, err, ""
        if k <= 1:
            return modarith.mod_div, (x, y, k), result, None, "expected ValueError, because k <= 1"
        if (result * y) % k != x % k:
            return modarith.mod_div, (x, y, k), result, None, "result * y mod k was not x mod k"

    # noinspection PyUnusedLocal
    @staticmethod
    def test_euclidean(x: int, y: int, k: int):
        try:
            result = modarith.euclidean_alg(x, y)
        except ValueError as err:
            if x < 0 or y < 0:
                return
            return modarith.euclidean_alg, (x, y), None, err, "ValueError despite both x and y >= 0"
        if x < 0 or y < 0:
            return modarith.euclidean_alg, (x, y), result, None, "expected ValueError, because x or y < 0"
        real_result = math.gcd(x, y)
        if real_result != result:
            return modarith.euclidean_alg, (x, y), result, None, f"was not gcd. {real_result} is greater common divisor"

    # noinspection PyUnusedLocal
    @staticmethod
    def test_extended_euclidean(x: int, y: int, k: int):
        try:
            result = modarith.extended_euclidean_alg(x, y)
        except ValueError as err:
            if x < 0 or y < 0:
                return
            return modarith.extended_euclidean_alg, (x, y), None, err, "ValueError despite both x and y >= 0"
        if x < 0 or y < 0:
            return modarith.extended_euclidean_alg, (x, y), result, None, "expected ValueError, because x or y < 0"
        if not isinstance(result, tuple) or len(result) != 3:
            return modarith.extended_euclidean_alg, (x, y), result, None, "result must be a tuple of length 3"
        d, s, t = result
        if d != s * x + t * y:
            return modarith.extended_euclidean_alg, (x, y), result, None, "result must satisfy the equation d == s * " \
                                                                          "x + t * y "

    # noinspection PyUnusedLocal
    @staticmethod
    def test_mod(x: int, y: int, k: int):
        try:
            result = modarith.mod(x, k)
        except ZeroDivisionError as err:
            if k == 0:
                return
            else:
                return modarith.mod, (x, k), None, err, "ZeroDivisionError despite k != 0"
        if result != x % k:
            return modarith.mod, (x, k), result, None, ""

    @staticmethod
    def test_pow(x: int, y: int, k: int):
        try:
            result = modarith.mod_pow(x, y, k)
        except ValueError as err:
            if k <= 1 or x < 0 or y < 0:
                return
            else:
                return modarith.mod_pow, (x, y, k), None, err, "ValueError despite k > 1, x >= 0 and y >= 0"
        if x < 0 or y < 0:
            return modarith.mod_pow, (x, y, k), result, None, "expected ValueError, because x or y < 0"
        if k <= 1:
            return modarith.mod_pow, (x, y, k), result, None, "expected ValueError, because k <= 1"
        real_result = pow(x, y, k)
        if result != real_result:
            return modarith.mod_pow, (x, y, k), result, None, f"instead of {real_result}"


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("min_rand", type=int, help="the smallest possible random value")
    parser.add_argument("max_rand", type=int, help="the biggest possible random value")
    parser.add_argument("n", type=int, help="the amount of test runs [>= 100]")
    args = parser.parse_args()
    n: int = int(args.n)
    if n < 100:
        raise ValueError(f"n musst be at least 100, given {n}")
    min_rand: int = int(args.min_rand)
    max_rand: int = int(args.max_rand)
    if min_rand >= max_rand:
        raise ValueError(f"min_rand (given {min_rand}) must be smaller than max_rand (given {max_rand})")
    tester = FuzzingTester(min_rand, max_rand, n)
    tester.run()
