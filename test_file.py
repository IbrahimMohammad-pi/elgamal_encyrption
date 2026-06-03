import pytest

import elgamal


def test_extended_euclid_basic():
    gcd, x, y = elgamal.extended_euclid(240, 46)
    assert gcd == 2
    assert 240 * x + 46 * y == gcd


def test_fast_modular_small_exponents():
    assert elgamal.fast_modular(2, 0, 13) == 1
    assert elgamal.fast_modular(2, 3, 13) == 8
    assert elgamal.fast_modular(7, 5, 19) == pow(7, 5, 19)


def test_string_conversion_roundtrip():
    message = "hi"
    encoded = elgamal.string_to_int(message)
    decoded = elgamal.int_to_string(encoded)
    assert decoded == message


def test_key_encrypt_decrypt_roundtrip():
    p = 65537
    g = 3
    x = 13
    private_key = elgamal.key(x, g, p)
    assert private_key.A == elgamal.fast_modular(g, x, p)

    plaintext = "hi"
    a, b = elgamal.key.encrypt(private_key, plaintext)
    assert isinstance(a, int)
    assert isinstance(b, int)

    recovered = private_key.decrypt(a, b)
    assert recovered == plaintext


def test_encrypt_rejects_large_message():
    p = 17
    g = 3
    x = 5
    private_key = elgamal.key(x, g, p)
    with pytest.raises(ValueError):
        elgamal.key.encrypt(private_key, "too large for p")
