import math

tol = 0.0001
func = input("Digite o f(x) na seguinte formatação (ex: x**2 + 2*x - 3):")
pi = float(input("Digite o ponto inicial:"))
pf = float(input("DIgite o ponto final:"))

f = eval(f"lambda x: {func}", {"math": math})

cont = pi
find_sqrt = False
a = pi
b = pf
f_a_inicial = f(a)

while cont < pf:

    cont_prox = min(cont + 1.0, pf)
    f_cont_prox = f(cont_prox)

    if f_a_inicial * f_cont_prox <= 0:
        find_sqrt = True
        a = cont
        b = cont_prox
        break

    a = cont_prox
    f_a_inicial = f_cont_prox
    cont += 1.0

if not find_sqrt:
    print('Não há raiz, ou a função está errada')
else:
    iteracao = 0
    fa = f(a)

    while (b - a) > tol:
        iteracao += 1

        m = (a + b) / 2
        f_m = f(m)

        if abs(f_m) < 1e-10:
            a = m
            b = m
            break

        if fa * f_m < 0:
            b = m
        else:
            a = m
            fa = f_m

r_a = (a + b) / 2
print(f"Raiz aproximada: {r_a:.6f}")
print(f"Iterações: {iteracao}")