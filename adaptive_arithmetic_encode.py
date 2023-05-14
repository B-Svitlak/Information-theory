from functools import reduce
import math
from decimal import Decimal, getcontext


def adaptive_arithmetic_encode(text):
    sorted_prob = ''.join(sorted(set(text)))
    symbol_weight = [1] * len(sorted_prob)
    s, q, p = 0, 0, 0
    cb, ce, z = 0, 1, 1
    for char in msg:
        index_char = sorted_prob.index(char)
        s = sum(symbol_weight)
        q = sum(symbol_weight[:index_char])
        p = sum(symbol_weight[:index_char + 1])
        symbol_weight[index_char] += 1
        cb, ce = cb * s + q * (ce - cb), cb * s + p * (ce - cb)
        z = z * s

    common_divisor = gcd(cb, ce, z)
    cb //= common_divisor
    ce //= common_divisor
    z //= common_divisor
    code = round(ce * next_power_of_two(z) / z)
    return bin(code), sorted_prob

# ????
# def adaptive_arithmetic_decode(binary_text, prob, length):
#     decimal_num = Decimal(int(str(binary_text), 2) / (2 ** (len(binary_text) - 1)))
#     print(decimal_num)
#     symbol_weight = [1] * len(prob)
#     decode_text = ''
#     for i in range(length):
#         interval = {}
#
#         for index, char in enumerate(prob):
#             s = sum(symbol_weight)
#             q = sum(symbol_weight[:index])
#             p = sum(symbol_weight[:index + 1])
#             print(f"{char} = {q}/{s}, {p}/{s}")
#             interval[char] = [Decimal(q / s), Decimal(p / s)]
#             if interval[char][0] <= decimal_num <= interval[char][1]:
#                 decode_text += char
#                 symbol_weight[index] += 1
#                 decimal_num = (decimal_num - interval[char][0]) / (interval[char][1] - interval[char][0])
#                 print(decimal_num)
#                 break
#     return decode_text


def next_power_of_two(n):
    return 2 ** math.ceil(math.log2(n))


def gcd(*args):
    def _gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    # Використовуємо reduce() для знаходження НСД для всіх введених чисел.
    return reduce(_gcd, args)


if __name__ == '__main__':
    msg = "sszzzuyzuu" + "o"
    encode, sorted_prob = adaptive_arithmetic_encode(msg)
    print(encode)

    # getcontext().prec = 45
    # decode = adaptive_arithmetic_decode(encode, sorted_prob, len(msg))
    # print(decode)
