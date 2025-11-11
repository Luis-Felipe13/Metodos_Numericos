# Não precisamos importar math/numpy aqui, pois 'f' é uma função lambda já criada

def isolamento_raiz(f, pi, pf, passo=1.0):
    """Realiza a busca incremental no intervalo [pi, pf]."""
    #Passo 1:
    a = pi
    #Passo 1.1:
    f_a_inicial = f(a)

    #Passo 2:
    while a < pf:
        #Passo 2.1:
        cont_prox = min(a + passo, pf)

        #Questão de segurança, para não entrar em loop infinito
        if a == cont_prox:
            break
            
        #Passo 1.1 (Novamente)
        f_cont_prox = f(cont_prox)

        #Passo 3:
        if f_a_inicial * f_cont_prox <= 0:
            return a, cont_prox
        #Passo 4:
        a = cont_prox
        f_a_inicial = f_cont_prox

    return None, None


# ----------------------------------------------------
# 3.1 MÉTODO DA BISSECÇÃO
# ----------------------------------------------------

def metodo_bisseccao(f, a_inicial, b_inicial, tol, max_iter=50):
    a = a_inicial
    b = b_inicial
    fa = f(a)

    #Verificação de segurança
    if fa * f(b) > 0:
        raise ValueError("f(a) e f(b) devem ter sinais opostos.")
    
    iteracoes = []
    iteracao_cont = 0

    #Passo 1:
    while (b - a) > tol and iteracao_cont < max_iter:
        iteracao_cont += 1
        
        #Passo 2:
        m = (a + b) / 2
        
        #Passo 3:
        f_m = f(m)

        iteracoes.append({
            'Iteração': iteracao_cont,
            'a': f"{a:.6f}",
            'b': f"{b:.6f}",
            'm': f"{m:.6f}",
            'f(m)': f"{f_m:.6f}",
            '|b-a|': f"{abs(b - a):.6f}"
        })
        #Verificação de segurança (Se atendida, quebra loop)
        if abs(f_m) < 1e-10:
            break

        #Passo 3.1:
        if fa * f_m < 0:
            b = m
        else:
            a = m
            fa = f_m
        #Volta ao loop

    #Final da iteração
    r_a = (a + b) / 2
    return r_a, iteracoes


# ----------------------------------------------------
# 3.2 MÉTODO DA POSIÇÃO FALSA (Regra Falsa)
# ----------------------------------------------------

def metodo_posicao_falsa(f, a_inicial, b_inicial, tol, max_iter=50):
    a = a_inicial
    b = b_inicial
    fa = f(a)
    fb = f(b)

    if fa * fb > 0:
        raise ValueError("f(a) e f(b) devem ter sinais opostos.")

    iteracoes = []
    iteracao_cont = 0

    while (b - a) > tol and iteracao_cont < max_iter:
        iteracao_cont += 1

        m = (a * fb - b * fa) / (fb - fa)
        f_m = f(m)

        iteracoes.append({
            'Iteração': iteracao_cont,
            'a': f"{a:.6f}",
            'b': f"{b:.6f}",
            'm': f"{m:.6f}",
            'f(m)': f"{f_m:.6f}",
            '|b-a|': f"{abs(b - a):.6f}"
        })

        if abs(f_m) < 1e-10:
            break

        if fa * f_m < 0:
            b = m
            fb = f_m
        else:
            a = m
            fa = f_m

    r_a = (a * fb - b * fa) / (fb - fa)
    return r_a, iteracoes
