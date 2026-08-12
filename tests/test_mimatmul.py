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


def test_consistencia_con_numpy_cuadradas():
    np = pytest.importorskip("numpy")
    rng = np.random.default_rng(7)
    for n in range(2, 6):
        A = rng.integers(0, 10, size=(n, n)).tolist()
        B = rng.integers(0, 10, size=(n, n)).tolist()
        esperado = (np.array(A) @ np.array(B)).tolist()
        assert mimatmul(A, B) == esperado


def test_consistencia_con_numpy_rectangulares():
    np = pytest.importorskip("numpy")
    rng = np.random.default_rng(11)
    for filas_a, col_a, col_b in [(3, 4, 2), (4, 2, 5), (1, 3, 1)]:
        A = rng.integers(0, 10, size=(filas_a, col_a)).tolist()
        B = rng.integers(0, 10, size=(col_a, col_b)).tolist()
        esperado = (np.array(A) @ np.array(B)).tolist()
        assert mimatmul(A, B) == esperado
