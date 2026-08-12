def mimatmul(A, B):
    if not A or not B or not A[0] or not B[0]:
        raise ValueError("Las matrices no pueden estar vacias")

    filas_a = len(A)
    columnas_a = len(A[0])
    filas_b = len(B)
    columnas_b = len(B[0])

    if any(len(fila) != columnas_a for fila in A) or any(
        len(fila) != columnas_b for fila in B
    ):
        raise ValueError("Todas las filas de cada matriz deben tener el mismo largo")

    if columnas_a != filas_b:
        raise ValueError(
            "Dimensiones incompatibles: "
            f"A es {filas_a}x{columnas_a} y B es {filas_b}x{columnas_b}"
        )

    resultado = []
    for i in range(filas_a):
        fila = []
        for j in range(columnas_b):
            total = 0
            for k in range(columnas_a):
                total += A[i][k] * B[k][j]
            fila.append(total)
        resultado.append(fila)
    return resultado
