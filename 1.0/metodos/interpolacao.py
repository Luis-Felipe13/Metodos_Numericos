import numpy as np


# ----------------------------------------------------
# 5.1.2 INTERPOLAÇÃO DE LAGRANGE
# ----------------------------------------------------

def interpolacao_lagrange(x_pontos, y_pontos, x_interpolar):
    n = len(x_pontos)
    if n != len(y_pontos):
        raise ValueError("O número de pontos x e y deve ser o mesmo.")

    x_pontos = np.array(x_pontos, dtype=float)
    y_pontos = np.array(y_pontos, dtype=float)
    x_interpolar = float(x_interpolar)

    P_x = 0

    for i in range(n):
        # Calcula o polinômio base de Lagrange L_i(x)
        L_i_x = 1
        for j in range(n):
            if i != j:
                L_i_x *= (x_interpolar - x_pontos[j]) / (x_pontos[i] - x_pontos[j])

        P_x += y_pontos[i] * L_i_x

    return P_x


# ----------------------------------------------------
# 5.2.1 TABELA DE DIFERENÇAS DIVIDIDAS FINITAS (NEWTON)
# Esta função apenas constrói a tabela, a interpolação é complexa para um único módulo
# Vamos focar na interpolação em si, que é o resultado final.
# ----------------------------------------------------

def interpolacao_newton_diferencas_divididas(x_pontos, y_pontos, x_interpolar):
    n = len(x_pontos)
    if n != len(y_pontos):
        raise ValueError("O número de pontos x e y deve ser o mesmo.")

    x = np.array(x_pontos, dtype=float)
    y = np.array(y_pontos, dtype=float)

    # Inicializa a tabela de diferenças
    diff = np.zeros((n, n))
    diff[:, 0] = y

    # Preenche a tabela
    for j in range(1, n):
        for i in range(n - j):
            diff[i, j] = (diff[i + 1, j - 1] - diff[i, j - 1]) / (x[i + j] - x[i])

    # Polinômio de Newton-Gregory (usa apenas a primeira linha da tabela)
    P_x = diff[0, 0]  # f[x0]

    for j in range(1, n):
        termo = diff[0, j]
        for i in range(j):
            termo *= (x_interpolar - x[i])
        P_x += termo

    # Retornamos o valor interpolado e a tabela (para visualização no Streamlit)
    tabela_df = {}
    for j in range(n):
        # Apenas as linhas relevantes são mantidas para a coluna
        coluna = [f"{diff[i, j]:.6f}" if i < n - j else "" for i in range(n)]
        tabela_df[f'f[x...](ordem {j})'] = coluna

    return P_x, tabela_df