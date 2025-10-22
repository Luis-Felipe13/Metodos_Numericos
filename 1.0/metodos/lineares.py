import numpy as np
from metodos.utils import validar_sistema_linear  # Requer a função de validação


# ----------------------------------------------------
# 4.1 MÉTODO DA ELIMINAÇÃO DE GAUSS
# ----------------------------------------------------

def metodo_eliminacao_gauss(A_input, b_input):
    A, b, n = validar_sistema_linear(A_input, b_input)

    # Matriz Aumentada [A | b]
    M = np.hstack((A, b.reshape(n, 1)))

    # Etapa 1: Eliminação (Forma Escalonada)
    for i in range(n):

        # Pivoteamento Parcial (encontra o maior elemento na coluna i abaixo da linha i)
        pivot_row = i + np.argmax(np.abs(M[i:, i]))
        if M[pivot_row, i] == 0:
            raise Exception("Matriz Singular ou Mal Condicionada (Divisão por zero no pivô).")

        # Troca as linhas (pivoteamento)
        M[[i, pivot_row]] = M[[pivot_row, i]]

        # Eliminação
        for j in range(i + 1, n):
            fator = M[j, i] / M[i, i]
            M[j, i:] = M[j, i:] - fator * M[i, i:]

    # Etapa 2: Substituição Retroativa
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (M[i, n] - np.dot(M[i, i + 1:n], x[i + 1:n])) / M[i, i]

    return x, M