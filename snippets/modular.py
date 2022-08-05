import math


def print_list(strings: list):
    for i in strings:
        print(i)


def count_bits(x: int):
    i = 0
    while x != 0:
        x = x >> 1
        i += 1
    return i


def square_and_multiply(base: int, exponent: int, mod: int, output=0):
    if exponent < 1 or mod < 2:
        print("Faulty use of SaM. (base exponent mod) = (", base, exponent, mod, ").")
        return 0
    e = exponent
    binary = []
    while e > 0:
        binary.append(e & 1)
        e = e >> 1
    result = 1
    if output != 0:
        squares = len(binary) - 1
        multiplications = binary.count(1) - 1
        sequence = [0]
        result_sequence = []
        for i in range(len(binary)).__reversed__():
            result = (result * result) % mod
            sequence.append(sequence[len(sequence) - 1] * 2)
            result_sequence.append(result)
            if binary[i] == 1:
                sequence.append(sequence[len(sequence) - 1] + 1)
                result = base * result % mod
                result_sequence.append(result)
        strings = ["Square and multiply algorithm: (base, exponent, mod) = ({0}, {1}. {2})".format(base, exponent, mod),
                   "Exponent binary (reversed): {0}".format(binary),
                   "(squares, multiplications) = ({0}, {1})".format(squares, multiplications),
                   "Computation sequence (exponents): {0}".format(sequence),
                   "Result sequence: {0}".format(result_sequence),
                   "Result = {0}".format(result),
                   "Check = {0}".format(result == pow(base, exponent, mod))]
        print_list(strings)
    else:
        for i in range(len(binary)).__reversed__():
            result = (result * result) % mod
            if binary[i] == 1:
                result = base * result % mod

    return result


def euclid_extended(a: int, b: int, output=0):
    a_start = a
    b_start = b
    if a < 0:
        a = -a
    if b < 0:
        b = -b
    if a == 0 or b == 0:
        return [max(a, b), 1, 1]
    if a == 1:
        return [1, 1, 0]
    if b == 1:
        return [1, 0, 1]

    r = [a, b]
    q = [0, 0]
    s = [1, 0]
    t = [0, 1]

    def ts(t_2, t_1, q_0):
        return t_2 - q_0 * t_1

    i = 1
    while r[i] != 0:
        q.append(r[i - 1] // r[i])
        r.append(r[i - 1] % r[i])
        s.append(ts(s[i - 1], s[i], q[i + 1]))
        t.append(ts(t[i - 1], t[i], q[i + 1]))
        i += 1

    if output != 0:
        strings = ["Euclid's Extended Algorithm: (a, b) = ({0},{1})".format(a_start, b_start),
                   #  "r list: {0}".format(r),
                   #  "q list: {0}".format(q),
                   #  "s list: {0}".format(s),
                   #  "t list: {0}".format(t),
                   "\\begin{table}[h!]\n\t\\begin{tabular}{ccccc}",
                   "\t\t$i$ & $r_i$ & $q_i$ & $s_i$ & $t_i$ \\\\ \\hline"]
        for j in range(i):
            strings.append("\t\t{0}\t&\t{1}\t&\t{2}\t&\t{3}\t&\t{4}\t\\\\".format(j, r[j], q[j], s[j], t[j])),
        strings.append("\t\t{0}\t&\t{1}\t&\t{2}\t&\t{3}\t&\t{4}".format(i, r[i], q[i], s[i], t[i])),
        strings.append("\t\\end{tabular}\n\\end{table}")
        strings.append("\\\\\n${0} = {1} \\cdot {2} + {3} \\cdot {4}$".format(r[i - 1], s[i - 1], r[0], t[i - 1], r[1]))
        print_list(strings)

    return [r[i - 1], s[i - 1], t[i - 1]]


def inverse_mod(a, mod):
    result = euclid_extended(a, mod, 0)
    if len(result) != 3:
        print("No inverse to", a, "mod", mod)
        return 0
    elif result[0] != 1:
        print("No inverse to", a, "mod", mod)
        return 0
    return result[1] % mod


def gen_primes():
    d = {}
    q = 2

    while True:
        if q not in d:
            yield q
            d[q * q] = [q]
        else:
            for p in d[q]:
                d.setdefault(p + q, []).append(p)
            del d[q]

        q += 1


def prime_factor_naive(n: int):
    factors = []
    if n < 1:
        return 0
    i = 0
    while n != 1 and i < n:
        i = i + 1
        for prime in gen_primes():
            if n % prime == 0:
                factors.append(prime)
                n = n // prime
                break
    return factors


def unique_factors(prime_list: list):
    result = []
    i = 0
    while i < len(prime_list):
        result.append(prime_list[i])
        i += prime_list.count(prime_list[i])
    return result


def collect_factors(prime_list: list):
    result = []
    i = 0
    prime_list.sort()
    while i < len(prime_list):
        count = prime_list.count(prime_list[i])
        val = 1
        for j in range(count):
            val *= prime_list[i]
        result.append(val)
        i += count
    return result


def c_string(n: int):
    result = ""
    for i in range(n):
        result += "c"
    return result


def separate_string(values: list, delimiter=""):
    if len(values) == 0:
        return ""
    result = ""
    for i in range(len(values) - 1):
        result += "{0} {1} ".format(values[i], delimiter)
    result += "{0}".format(values[len(values) - 1])
    return result


def crt_x(a_list, mod_list, output=0):
    if len(a_list) != len(mod_list):
        print("You did fucky wucky!")
        return 0
    m = 1
    for i in mod_list:
        m = m * i
    m_i = []
    y = []
    for i in range(len(mod_list)):
        m_i.append(m // mod_list[i])
        y.append(inverse_mod(m_i[i], mod_list[i]))
    x = 0
    for i in range(len(mod_list)):
        x += (a_list[i] * m_i[i] * y[i]) % m

    if output != 0:
        strings = ["$M = {0} = {1}$".format(separate_string(mod_list, "\\cdot"), m),
                   "\\begin{table}[h!]\n\t\\begin{tabular}" + "{" + "{0}".format(c_string(len(mod_list) + 1)) + "}"]
        i_list = []
        for i in range(len(a_list)):
            i_list.append(i + 1)
        strings.append("\t\t$i$\t&\t" + separate_string(i_list, "\t&\t") + "\\\\ \\hline")
        strings.append("\t\t$a_i$\t&\t" + separate_string(a_list, "\t&\t") + "\\\\")
        strings.append("\t\t$m_i$\t&\t" + separate_string(mod_list, "\t&\t") + "\\\\")
        strings.append("\t\t$M_i$\t&\t" + separate_string(m_i, "\t&\t") + "\\\\")
        strings.append("\t\t$y_i$\t&\t" + separate_string(y, "\t&\t"))
        strings.append("\t\\end{tabular}\n\\end{table}")
        print_list(strings)
    return x


def crt_as(x, mod, output=0):
    mod_list = collect_factors(prime_factor_naive(mod))
    a = []
    for i in mod_list:
        a.append(x % i)
    if output != 0:
        strings = ["Solutions $x_i\\mod m_i$:\n\\begin{align*}"]
        lines = []
        for n, m in zip(a, mod_list):
            lines.append("\t{0}&\\equiv{1}\\mod{2}".format(x, n, m))
        strings.append(separate_string(lines, "\\\\\n"))
        strings.append("\\end{align*}")
        print_list(strings)
    return [a, mod_list]


def euler_phi(n: int, output=0):
    if n < 2:
        print("You did fucky wucky.")
        return 0
    primes = prime_factor_naive(n)
    unique_primes = unique_factors(primes)
    exponents = []
    for p in unique_primes:
        exponents.append(primes.count(p))
    result = 1

    for p, e in zip(unique_primes, exponents):
        result *= (pow(p, e) - pow(p, e - 1))

    if output != 0:
        product = []
        i = 0
        while i < len(primes):
            product.append("{0}^{1}".format(primes[i], primes.count(primes[i])))
            i += primes.count(primes[i])
        strings = ["$n$ factors into $n={0}$ which gives us $k={1}$ coprime factors.".format(
            separate_string(product, "\\cdot"), len(unique_primes)),
                   "\\begin{align*}\n\t\\phi(n) &= \\prod_{i=1}^k\\left(p_i^{e_i}-p_i^{e_i-1}\\right)\\\\"]
        product = "\t&="
        for p, e in zip(unique_primes, exponents):
            product += "\\left({0}^{1}-{0}^{2}\\right)".format(p, e, e - 1)
        strings.append(product + "\\\\")
        factors = []
        for p, e in zip(unique_primes, exponents):
            factors.append(pow(p, e) - pow(p, e - 1))
        product = "\t&=" + separate_string(factors, "\\cdot")
        strings.append(product + "\\\\")
        strings.append("\t&={0}\n".format(result) + "\\end{align*}")
        print_list(strings)
    return result


def gcd(a: int, b: int, output=0):
    result = euclid_extended(a, b)[0]
    if output != 0:
        print("$\\gcd({0},{1})={2}$".format(a, b, result))
    return result


def lcm(a: int, b: int, output=0):
    result = (a * b) // gcd(a, b)
    if output != 0:
        print("$\\text{lcm}" + "({0},{1})={2}$".format(a, b, result))
    return result


def sqrt_mod_p(a: int, p: int):
    while True:
        if math.isqrt(a) * math.isqrt(a) == a:
            break
        a = a + p
    return math.isqrt(a)


def roots_mod_p(a: int, b: int, c: int, p: int):  # Assumes d = b^2 - 4ac is a square in the integers
    a, b, c = a % p, b % p, c % p
    d = (b * b - 4 * a * c) % p
    d = sqrt_mod_p(d, p)
    div = inverse_mod(2 * a, p)
    return (-b + d) * div % p, (-b - d) * div % p


def roots_mod_n(a: int, b: int, c: int, n: int):  # Assumes n = pq, for p,q prime.
    crt_moduli = collect_factors(prime_factor_naive(n))
    solutions_mod = []
    for m in crt_moduli:
        i, j = roots_mod_p(a, b, c, m)
        solutions_mod.append([i, j, m])
    print(solutions_mod)
    solutions_n = []
    for i in range(len(solutions_mod)):
        for j in range(len(solutions_mod)):
            solutions_n.append(crt_x([solutions_mod[0][i], solutions_mod[1][j]],
                                     [solutions_mod[0][2], solutions_mod[1][2]]) % n)
    return solutions_n


def wrap_negative(x: int):
    if x < 0:
        return "\\left(" + x.__str__() + "\\right)"
    return x.__str__()
