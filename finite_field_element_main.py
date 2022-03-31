import time
from mod_arith.modarith import *

if __name__ == '__main__':
    start = time.time_ns()
    a = mod_mul(781324681235646123, 187326455132453124, 103)
    print(time.time_ns()-start)
    start = time.time_ns()
    b = 13252457612345234 * 2345123542345764256 % 103
    print(time.time_ns() - start)
