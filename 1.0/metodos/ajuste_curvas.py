import numpy as np


# ----------------------------------------------------
# 6.1 MÍNIMOS QUADRADOS (Reta e Parábola)
# ----------------------------------------------------

def ajuste_minimos_quadrados(x_pontos, y_pontos, grau):
    n = len(x_pontos)
    x = np.array(x_pontos, dtype=float)
    y = np.array(y_pontos, dtype=float)

    if n < grau + 1:
        raise ValueError(f"São necessários pelo menos {grau + 1} pontos para um ajuste de grau {grau}.")

    # Monta a matriz do sistema normal [A][C] = [B]
    A = np.zeros((grau + 1, grau + 1))
    B = np.zeros(grau + 1)

    for i in range(grau + 1):
        for j in range(grau + 1):
            A[i, j] = np.sum(x ** (i + j))
        B[i] = np.sum(y * x ** i)

    # Resolve o sistema linear A * Coeficientes = B
    try:
        coeficientes = np.linalg.solve(A, B)
    except np.linalg.LinAlgError:
        raise Exception("O sistema de equações normais é singular ou mal condicionado.")

    # Formatação da função resultante para exibição
    polinomio_str = " + ".join(
        [f"{c:.4f}x^{i}" if i > 1 else f"{c:.4f}x" if i == 1 else f"{c:.4f}"
         for i, c in enumerate(coeficientes)]
    )
    polinomio_str = polinomio_str.replace("x^1", "x").replace("x^0", "")

    return coeficientes, polinomio_str