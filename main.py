import math
import random

from snippets import modular as md
from snippets import primes


def otp_enc(m: int, k: int):
    return m ^ k


def otp_dec(c: int, k: int):
    return c ^ k


def std_s_box(m, bits=16):
    result = 0
    for i in range(bits):
        result += (m & 1) * pow(2, (i // 4 + 4 * (i % 4)))
        m = m >> 1
    return result


def sb_enc(m: int, k: int, n: int, s_box, bits=16):
    keys = []
    for i in range(n):
        keys.append(k % pow(2, bits))
        k = k >> bits
    m = m % pow(2, bits)
    for i in range(n - 1):
        m = s_box(m ^ keys[i])
    return m ^ keys[n - 1]


def sb_dec(c: int, k: int, n: int, s_box, bits=16):
    keys = []
    for i in range(n):
        keys.append(k % pow(2, bits))
        k = k >> bits
    c = c % pow(2, bits)
    for i in range(n - 1):
        c = s_box(c ^ keys[n - 1 - i])
    return c ^ keys[0]


def rsa_enc(m: int, e: int, n: int):
    return md.square_and_multiply(m, e, n)


def rsa_dec(c: int, d: int, n: int):
    return md.square_and_multiply(c, d, n)


def generate_rsa(min_bytes=32):
    p = primes.generate_prime(min_bytes)
    q = primes.generate_prime(min_bytes * 2)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    while True:
        e = random.randrange(3, 101, 2)
        if md.gcd(e, phi_n) == 1:
            break
    d = md.inverse_mod(e, phi_n)
    return (n, e), (p, q, d)


def rsa_sign(x: int, n: int, d: int):
    return pow(x, d, n)


def rsa_verify(x: int, s: int, e: int, n: int):
    return x % n == pow(s, e, n)


def generate_eg(min_bytes=32):
    while True:
        p = 2 * primes.generate_prime(min_bytes) + 1
        if primes.miller_rabin(p, 50):
            break
    a_lower = math.isqrt(p)
    while True:
        a = random.randrange(a_lower, a_lower * 2, 1)
        if primes.test_primitive(a, p, [2]):
            break
    exp = random.randint(1, p - 1)
    b = pow(a, exp, p)
    return exp, p, a, b


def enc_eg(m, a, b, p):
    k = random.randint(1, p - 1)
    y_1 = pow(a, k, p)
    y_2 = m * pow(b, k, p)
    return y_1, y_2


def dec_eg(exp, y_1, y_2, p):
    y = md.inverse_mod(pow(y_1, exp, p), p)
    y = (y_2 * y) % p
    return y


def merkle_damgaard(x: int, m: int, n_cap: int, n: int):
    i = md.count_bits(m) + 1
    l_m = pow(2, i) - 1
    v = md.count_bits(x)
    x = 2 * x + 1

    s = n_cap - n - ((v + 1 + l_m) % (n_cap - n))
    x = x << s
    v_1 = v
    i = 0
    v_binary = []
    while v_1 != 0:
        v_binary.append(v_1 & 1)
        v_1 = v_1 >> 1
        i += 1
    extra_bits = l_m - len(v_binary)
    x = x << extra_bits
    for i in range(len(v_binary)).__reversed__():
        x = (x << 1) + v_binary[i]
    return x


def shamir_gen(t: int, w: int, k: int):
    p = primes.generate_prime()
    c = []
    for i in range(t - 1):
        c.append(random.randint(1, p - 1))

    def f(x_i: int):
        y_i = k
        for j in range(len(c)):
            y_i = (y_i + c[j] * pow(x_i, j + 1, p)) % p
        return y_i

    x = []
    i = 0
    while i < w:
        cand = random.randint(1, p - 1)
        if x.count(cand) == 0 and md.inverse_mod(cand, p) != 0:
            x.append(cand)
            i += 1

    y = []
    for i in x:
        y.append(f(i))

    return x, y, p, zip(x, y)


def shamir_retrieve(x: list, y: list, p: int, output=0):
    t = len(y)
    k = 0
    calc_i = []
    formula_expand_i = []
    formula_expand_i_2 = []
    reduction_i = []
    result_i = []
    strings = []
    final_reduction = []
    if output != 0:
        intro = "Retrieving key $k$ in a $(t,w)$-threshold scheme.\n$t={0}$ shares are given as ".format(t)
        point_strings = []
        for i in range(t):
            point_strings.append("$({0},{1})$".format(x[i], y[i]))
        intro = intro + md.separate_string(point_strings, ", ") + " with $p={0}$.\n".format(p)
        intro = intro + "\\begin{align*}\n\tk =& \\sum_{i=1}^{" + t.__str__() + "} y_i \\left(\\prod_{1\\leq j\\leq"
        intro = intro + t.__str__() + ", j\\neq i} \\frac{x_j}{x_j-x_i}\\right)\\mod" + p.__str__() + "\\\\"
        strings.append(intro)
    for i in range(t):
        k_i = 1
        mid_product = 1
        mid_inverse = 1
        formula_expand_j_num = []
        formula_expand_j_denom = []
        nums = []
        inverses = []
        for j in range(t):
            if i == j:
                continue
            k_i *= x[j] * md.inverse_mod((x[j] - x[i]) % p, p)
            if output != 0:
                formula_expand_j_num.append("x_{" + "{}".format(j + 1) + "}")
                formula_expand_j_denom.append("\\left(x_{" + "{}".format(j + 1) + "}" + "-" + "x_{" + "{}".format(i + 1)
                                              + "}" + "\\right)")
                nums.append("{}".format(x[j]))
                inverses.append("\\left(" + md.wrap_negative(x[j]) + "-" + md.wrap_negative(x[i]) + "\\right)")
                mid_product *= x[j]
                mid_inverse *= x[j] - x[i]
        k += k_i * y[i] % p
        if output != 0:
            formula_expand_i.append("y_{" + "{}".format(i + 1) + "}\\cdot" + "\\left(\\prod_{1\\leq j\\leq"
                                    + "{}".format(t) + ", j\\neq" + "{}".format(i + 1) + "} \\frac{x_j}{x_j-x_{"
                                    + "{}".format(i + 1) + "}}\\right)")
            formula_expand_i_2.append("y_{" + "{}".format(i) + "} \\cdot "
                                      + md.separate_string(formula_expand_j_num, " \\cdot ") + "\\cdot \\left("
                                      + md.separate_string(formula_expand_j_denom, "") + "\\right)^{-1}")
            calc_i.append("{0} \\cdot {1} \\cdot \\left( {2} \\right)".format(y[i], md.separate_string(nums, "\\cdot"),
                                                                              md.separate_string(inverses))
                          + "^{-1}")
            mid_product *= y[i]
            reduction_i.append("{}\\cdot ".format(mid_product) + md.wrap_negative(mid_inverse) + "^{-1}")
            final_reduction.append("{0}\\cdot {1}".format(mid_product % p, md.inverse_mod(mid_inverse % p, p)))
            result_i.append((k_i * y[i] % p).__str__())
    if output != 0:
        strings.append("\t=&" + md.separate_string(formula_expand_i, "\\\\\n\t&+") + "\\\\")
        strings.append("\t=&" + md.separate_string(formula_expand_i_2, "\\\\\n\t&+") + "\\\\")
        strings.append("\t=&" + md.separate_string(calc_i, "\\\\\n\t&+") + "\\\\")
        strings.append("\t=&" + md.separate_string(reduction_i, "+") + "\\\\")
        strings.append("\t=&" + md.separate_string(final_reduction, "+") + "\\\\")
        strings.append("\t=&" + md.separate_string(result_i, "+") + "\\\\")
        strings.append("\t=&" + (k % p).__str__() + "\\mod {0}".format(p) + "\n\\end{align*}")
        md.print_list(strings)
    return k % p


def main(output: int):
    x, y, p, zipped = shamir_gen(5, 8, 31)
    shamir_retrieve(x, y, p, 1)



if __name__ == '__main__':
    main(1)
