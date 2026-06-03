import math
import pytest

from elgamal import (
    extended_euclid,
    fast_modular,
    string_to_int,
    int_to_string,
    gen_prime,
    key,
)


# ----------------------------
# extended_euclid tests
# ----------------------------

def test_extended_euclid_gives_correct_hcf():
    hcf, i, j = extended_euclid(30, 12)

    assert hcf == 6


def test_extended_euclid_linear_combination():
    a = 240
    b = 46

    hcf, i, j = extended_euclid(a, b)

    # extended Euclid should return i and j such that:
    # a*i + b*j == gcd(a, b)
    assert hcf == math.gcd(a, b)
    assert a * i + b * j == hcf


def test_extended_euclid_when_one_number_is_zero():
    hcf, i, j = extended_euclid(10, 0)

    assert hcf == 10
    assert 10 * i + 0 * j == hcf


# ----------------------------
# fast_modular tests
# ----------------------------

def test_fast_modular_small_example():
    assert fast_modular(2, 10, 1000) == 24


def test_fast_modular_matches_python_pow():
    base = 123456
    exp = 789
    p = 1000000007

    # Python's built-in pow(base, exp, p) is the reference answer
    assert fast_modular(base, exp, p) == pow(base, exp, p)


def test_fast_modular_exp_zero():
    assert fast_modular(999, 0, 17) == 1


@pytest.mark.parametrize("base, exp, p", [
    (2, 5, 13),
    (7, 3, 11),
    (10, 100, 17),
    (123, 456, 789),
    (999999, 12345, 1000003),
])
def test_fast_modular_parametrised(base, exp, p):
    assert fast_modular(base, exp, p) == pow(base, exp, p)


# ----------------------------
# string/int conversion tests
# ----------------------------

def test_string_to_int_and_back():
    message = "hello"

    value = string_to_int(message)
    result = int_to_string(value)

    assert result == message


def test_empty_string_to_int_and_back():
    message = ""

    value = string_to_int(message)
    result = int_to_string(value)

    assert result == message


def test_string_with_symbols_to_int_and_back():
    message = "ElGamal 123!"

    value = string_to_int(message)
    result = int_to_string(value)

    assert result == message


# ----------------------------
# gen_prime tests
# ----------------------------

def test_gen_prime_returns_number_with_correct_bit_length():
    p = gen_prime(bits=8, k=5)

    # This checks that the number is not accidentally tiny
    assert p.bit_length() <= 8


def test_gen_prime_rejects_too_few_bits():
    with pytest.raises(ValueError):
        gen_prime(bits=2)


# ----------------------------
# ElGamal encryption/decryption tests
# ----------------------------

def test_encrypt_decrypt_small_message():
    # This is a toy key, not secure.
    # p must be bigger than the integer encoding of the message.
    p = 1000003
    g = 2
    x = 123

    private_key = key(x, g, p)

    a, b = key.encrypt(private_key, "hi")
    decrypted = private_key.decrypt(a, b)

    assert decrypted == "hi"


def test_encrypt_rejects_message_too_large_for_p():
    p = 101
    g = 2
    x = 5

    private_key = key(x, g, p)

    # "hello" as an integer is much bigger than 101
    with pytest.raises(ValueError):
        key.encrypt(private_key, "hello")

def test_debug_fast_modular():
    from elgamal import fast_modular

    print(fast_modular)
    print(fast_modular(2, 10, 1000))

    assert fast_modular(2, 10, 1000) == 24