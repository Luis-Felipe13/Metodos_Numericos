import sympy
from metodos.utils import criar_funcao_simbolica, criar_funcao


# ----------------------------------------------------
# 3.4 MÉTODO DE NEWTON-RAPHSON
# ----------------------------------------------------

def metodo_newton_raphson(func_str, x0, tol, max_iter=50):
    f_expr, x_sym = criar_funcao_simbolica(func_str)

    if f_expr is None:
        raise ValueError("Função simbólica inválida. Verifique a sintaxe.")

    df_expr = sympy.diff(f_expr, x_sym)
    f = sympy.lambdify(x_sym, f_expr, 'numpy')
    df = sympy.lambdify(x_sym, df_expr, 'numpy')

    x_i = float(x0)
    iteracoes = []
    iteracao_cont = 0

    while iteracao_cont < max_iter:
        iteracao_cont += 1

        fx_i = f(x_i)
        dfx_i = df(x_i)

        if abs(dfx_i) < 1e-10:
            raise Exception("Derivada zero (f'(x) ≈ 0). O método falhou.")

        x_novo = x_i - (fx_i / dfx_i)
        erro = abs(x_novo - x_i)

        iteracoes.append({
            'Iteração': iteracao_cont,
            'x_i': f"{x_i:.6f}",
            'f(x_i)': f"{fx_i:.6f}",
            "f'(x_i)": f"{dfx_i:.6f}",
            'x_i+1': f"{x_novo:.6f}",
            '|x_i+1 - x_i|': f"{erro:.6f}"
        })

        if erro < tol:
            break

        x_i = x_novo

    return x_i, iteracoes


# ----------------------------------------------------
# 3.5 MÉTODO DA SECANTE
# ----------------------------------------------------

def metodo_secante(f, x_ant, x_i, tol, max_iter=50):
    x_ant = float(x_ant)
    x_i = float(x_i)

    iteracoes = []
    iteracao_cont = 0

    while iteracao_cont < max_iter:
        iteracao_cont += 1

        fx_ant = f(x_ant)
        fx_i = f(x_i)

        if abs(fx_i - fx_ant) < 1e-10:
            raise Exception("Divisão por zero (f(x_i) ≈ f(x_ant)). O método falhou.")

        x_novo = x_i - fx_i * (x_i - x_ant) / (fx_i - fx_ant)
        erro = abs(x_novo - x_i)

        iteracoes.append({
            'Iteração': iteracao_cont,
            'x_ant': f"{x_ant:.6f}",
            'x_i': f"{x_i:.6f}",
            'f(x_i)': f"{fx_i:.6f}",
            'x_i+1': f"{x_novo:.6f}",
            '|x_i+1 - x_i|': f"{erro:.6f}"
        })

        if erro < tol:
            break

        x_ant = x_i
        x_i = x_novo

    return x_i, iteracoes


# ----------------------------------------------------
# EXTRA: PONTO FIXO (Iteração)
# ----------------------------------------------------

def metodo_ponto_fixo(g_str, x0, tol, max_iter=50):
    g = criar_funcao(g_str)

    if g is None:
        raise ValueError("Função de iteração g(x) inválida.")

    x_i = float(x0)
    iteracoes = []
    iteracao_cont = 0

    while iteracao_cont < max_iter:
        iteracao_cont += 1

        try:
            x_novo = g(x_i)
        except Exception as e:
            raise Exception(f"Erro ao calcular g(x): {e}")

        erro = abs(x_novo - x_i)

        iteracoes.append({
            'Iteração': iteracao_cont,
            'x_i': f"{x_i:.6f}",
            'g(x_i)': f"{x_novo:.6f}",
            'x_i+1': f"{x_novo:.6f}",
            '|x_i+1 - x_i|': f"{erro:.6f}"
        })

        if erro < tol:
            break

        x_i = x_novo

    if iteracao_cont == max_iter:
        raise Exception(f"O método não convergiu após {max_iter} iterações. Verifique o critério |g'(x)| < 1.")

    return x_i, iteracoes