import math
import numpy as np
import sympy


# =========================================================================
# FUNÇÕES GERAIS E CONVERSÃO
# =========================================================================

def criar_funcao(func_str):
    """Cria e retorna a função lambda (para cálculo numérico) a partir de uma string."""
    ambiente = {"math": math, "np": np}
    try:
        # Permite que o usuário use np.sin, np.exp, etc.
        return eval(f"lambda x: {func_str}", ambiente)
    except:
        return None


def criar_funcao_simbolica(func_str):
    """Cria e retorna a expressão simbólica (para cálculo da derivada) e a variável 'x'."""
    x = sympy.Symbol('x')
    try:
        expr = sympy.sympify(func_str)
        return expr, x
    except Exception:
        return None, None


def validar_sistema_linear(A, b):
    """Valida se o sistema A (matriz) e b (vetor) têm dimensões compatíveis."""
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = A.shape[0]

    if A.shape[1] != n:
        raise ValueError("A matriz A deve ser quadrada (n x n).")
    if b.ndim != 1 or b.size != n:
        raise ValueError("O vetor b deve ter n elementos.")

    return A, b, n