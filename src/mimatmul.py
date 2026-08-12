def mimatmul(A, B):
    # Aqui se revisa que las matrices no esten vacias.
    if not A or not B or not A[0] or not B[0]:
        raise ValueError("Las matrices no pueden estar vacias")

    # Aqui se guardan las dimensiones de ambas matrices.
    filas_a = len(A)
    columnas_a = len(A[0])
    filas_b = len(B)
    columnas_b = len(B[0])

    # Aqui se revisa que las filas de cada matriz tengan el mismo largo.
    if any(len(fila) != columnas_a for fila in A) or any(
        len(fila) != columnas_b for fila in B
    ):
        raise ValueError("Todas las filas de cada matriz deben tener el mismo largo")

    # Aqui se revisa que las dimensiones permitan multiplicar A por B.
    if columnas_a != filas_b:
        raise ValueError(
            "Dimensiones incompatibles: "
            f"A es {filas_a}x{columnas_a} y B es {filas_b}x{columnas_b}"
        )

    # Aqui se calcula cada elemento del resultado con tres ciclos for.
    resultado = []
    for i in range(filas_a):
        fila = []
        for j in range(columnas_b):
            total = 0
            for k in range(columnas_a):
                total += A[i][k] * B[k][j]
            fila.append(total)
        resultado.append(fila)
    # Aqui se devuelve la matriz final multiplicada.
    return resultado
