import pytest

from src.mimatmul import mimatmul


def test_multiplicacion_2x2():
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    esperado = [[19, 22], [43, 50]]
    assert mimatmul(A, B) == esperado


def test_multiplicacion_rectangular():
    A = [[1, 2, 3], [4, 5, 6]]
    B = [[7, 8], [9, 10], [11, 12]]
    esperado = [[58, 64], [139, 154]]
    assert mimatmul(A, B) == esperado


def test_multiplicacion_identidad():
    A = [[1, 2], [3, 4]]
    I = [[1, 0], [0, 1]]
    assert mimatmul(A, I) == A
    assert mimatmul(I, A) == A


def test_dimensiones_incompatibles():
    A = [[1, 2], [3, 4]]
    B = [[1, 2, 3]]
    with pytest.raises(ValueError):
        mimatmul(A, B)
