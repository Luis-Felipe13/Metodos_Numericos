import numpy as np


# ----------------------------------------------------
# 7.2 REGRA DO TRAPÉZIO
# ----------------------------------------------------

def regra_trapezio(f, a, b, n):
    """Regra do Trapézio (composta)"""
    h = (b - a) / n
    soma = 0.5 * (f(a) + f(b))

    for i in range(1, n):
        soma += f(a + i * h)

    integral = h * soma
    return integral


# ----------------------------------------------------
# 7.3 1/3 DE SIMPSON (Quadratura Gaussiana)
# ----------------------------------------------------

def regra_simpson_1_3(f, a, b, n):
    """Regra de Simpson 1/3 (composta). n deve ser PAR."""
    if n % 2 != 0:
        raise ValueError("O número de subintervalos (n) deve ser PAR para a regra de Simpson 1/3.")

    h = (b - a) / n
    soma = f(a) + f(b)  # f(x0) + f(xn)

    for i in range(1, n):
        x_i = a + i * h
        if i % 2 == 0:
            soma += 2 * f(x_i)  # Coeficiente 2 para índices pares
        else:
            soma += 4 * f(x_i)  # Coeficiente 4 para índices ímpares

    integral = (h / 3) * soma
    return integral