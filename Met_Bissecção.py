import math
import numpy as np

func = input("Digite o f(x) na seguinte formatação: x**(n-1)n +- x**(n-1) +- C**(n-2)")

pi = int(input("Digite o ponto inicial:"))
pf = int(input("DIgite o ponto final:"))

f = eval(f"lambda x: {func}", {"math": math})
cont = pi
find_sqrt = False
while cont < pf:
    fpi = f(cont)
    fpi2 = f(cont+1)
    cont+=1
    if fpi * fpi2 < 0:
        find_sqrt = True
        print('Raiz encontrada em:')
        print(cont-1, fpi, fpi2)
        break

if not find_sqrt:
    print('Essa função está incorreta.')