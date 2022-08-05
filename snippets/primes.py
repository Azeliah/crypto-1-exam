import math
import random

import numpy as np
from snippets import modular as md


def prime_test_mr(y: int, s: int, m: int):
    for i in range(s):
        if y == m - 1:
            return True
        else:
            y = md.square_and_multiply(y, 2, m)  # Result of SaM is always mod m here.
    return False


def miller_rabin(num: int, iterations: int):
    if iterations > num - 2:
        print("Too many iterations. m: ", num, " iterations: ", iterations)
        return False

    odd_remainder = num - 1
    exponent = 0
    while odd_remainder % 2 == 0:
        exponent += 1
        odd_remainder = odd_remainder // 2

    for i in range(iterations):
        b = random.randint(2, num)
        y = md.square_and_multiply(b, odd_remainder, num)
        if y != 1:
            if not prime_test_mr(y, exponent, num):
                return False
    return True


def prime_estimate(num: int):
    return num / np.log(num)


def prime_test(num: int):
    if num < 2:
        return 0
    if num == 2:
        return 1
    upper_bound = math.isqrt(num) + 1
    odds = np.arange(start=3, stop=upper_bound, step=2)
    for i in odds:
        if num % i == 0:
            return 0
    return 1


def generate_prime(min_bytes=32):
    p_lower_bound = pow(256, min_bytes)
    prime_found = False
    num = 0
    while not prime_found:
        num = random.randrange(p_lower_bound + 1, p_lower_bound * 2 - 1, 2)
        prime_found = miller_rabin(num, 50)
        if prime_found:
            num_2 = (num - 1) // 2
            if miller_rabin(num_2, 50):
                prime_found = False
    return num


def test_primitive(a: int, p: int, factors=None, output=0):
    if factors is None:
        factors = []
    if len(factors) == 0:
        factors = md.unique_factors(md.prime_factor_naive(p - 1))
    for i in factors:
        if pow(a, (p - 1) // i, p) == 1:
            if output != 0:
                print("{0} is not a primitive modulo {1}, since ${0}^{2} = 1$, where ${2}\\neq{3}$".format(a, p,
                                                                                                           (p - 1) // i,
                                                                                                           p - 1))
            return False
    return True
