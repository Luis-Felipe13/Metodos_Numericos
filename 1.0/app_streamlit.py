import streamlit as st
import pandas as pd
import numpy as np
import json  # Para lidar com as entradas de listas

# Importa todas as funções dos módulos
from metodos.utils import criar_funcao
from metodos.fechados import isolamento_raiz, metodo_bisseccao, metodo_posicao_falsa
from metodos.abertos import metodo_newton_raphson, metodo_secante, metodo_ponto_fixo
from metodos.lineares import metodo_eliminacao_gauss
from metodos.interpolacao import interpolacao_lagrange, interpolacao_newton_diferencas_divididas
from metodos.ajuste_curvas import ajuste_minimos_quadrados
from metodos.integracao import regra_trapezio, regra_simpson_1_3


# =========================================================================
# FUNÇÃO AUXILIAR PARA ENTRADA DE DADOS (Lista de pontos ou Matrizes)
# =========================================================================

def parse_input_list(input_str, default_value):
    """Tenta converter a string de entrada do usuário em uma lista/array Python."""
    if not input_str:
        return default_value
    try:
        # Usa json.loads para converter strings de listas ([1, 2, 3]) em listas Python
        return json.loads(input_str)
    except json.JSONDecodeError:
        st.error("Formato inválido. Use a sintaxe Python para listas (ex: [1, 2, 3]).")
        st.stop()
    except Exception:
        st.error("Erro ao processar a entrada.")
        st.stop()


# =========================================================================
# CONFIGURAÇÃO DA INTERFACE
# =========================================================================

st.title("Calculadora de Métodos Numéricos")
st.markdown("---")

# --- SELETOR DE MÉTODOS ---
METODOS = {
    "Raízes de Equações": [
        "1. Bissecção", "2. Posição Falsa", "3. Newton-Raphson",
        "4. Secante", "5. Ponto Fixo (Extra)"
    ],
    "Sistemas Lineares": [
        "6. Eliminação de Gauss",
        # "7. Gauss-Jacobi (A ser implementado)",
        # "8. Gauss-Seidel (A ser implementado)"
    ],
    "Interpolação": [
        "9. Lagrange", "10. Diferenças Divididas (Newton)"
    ],
    "Ajuste de Curvas": [
        "11. Mínimos Quadrados (Reta)", "12. Mínimos Quadrados (Parábola)"
    ],
    "Integração Numérica": [
        "13. Regra do Trapézio", "14. 1/3 de Simpson"
    ]
}

# Cria o seletor na barra lateral
grupo_selecionado = st.sidebar.selectbox("Escolha a Seção:", list(METODOS.keys()))
metodo_selecionado = st.sidebar.selectbox("Escolha o Método:", METODOS[grupo_selecionado])

st.header(f"Método: {metodo_selecionado}")
st.markdown("---")

# =========================================================================
# ENTRADA DE DADOS GERAL (Para Raízes, Interpolação e Integração)
# =========================================================================

if grupo_selecionado not in ["Sistemas Lineares", "Ajuste de Curvas"]:
    col_func, col_tol = st.columns([3, 1])
    with col_func:
        func_str = st.text_input("Função f(x) (Ex: np.cos(x) - x)", value="np.cos(x) - x")
    with col_tol:
        tol = st.number_input("Tolerância/Erro (tol)", value=0.0001, format="%.6f", step=0.00001)

# Validação da Função (Para métodos que usam f(x))
if grupo_selecionado in ["Raízes de Equações", "Integração Numérica"]:
    f_num = criar_funcao(func_str)
    if f_num is None:
        st.error("Erro: A função digitada é inválida. Use 'np.' para funções trigonométricas/exponenciais.")
        st.stop()

# =========================================================================
# LÓGICA DE EXECUÇÃO POR MÉTODO
# =========================================================================


# --- 1. RAÍZES DE EQUAÇÕES (Fechados) ---

if metodo_selecionado in ["1. Bissecção", "2. Posição Falsa"]:

    st.subheader("Configuração do Intervalo")
    col_pi, col_pf = st.columns(2)
    with col_pi:
        pi = st.number_input("Ponto Inicial (pi)", value=0.0, step=0.1, key="pi_f")
    with col_pf:
        pf = st.number_input("Ponto Final (pf)", value=10.0, step=0.1, key="pf_f")

    if st.button(f"Executar {metodo_selecionado}"):

        a_isolado, b_isolado = isolamento_raiz(f_num, pi, pf)

        if a_isolado is None:
            st.warning(f"Não foi possível isolar a raiz no intervalo [{pi}, {pf}].")
        else:
            st.success(f"Raiz isolada no intervalo: **[{a_isolado:.6f}, {b_isolado:.6f}]**")

            try:
                if metodo_selecionado == "1. Bissecção":
                    raiz, iteracoes = metodo_bisseccao(f_num, a_isolado, b_isolado, tol)
                else:
                    raiz, iteracoes = metodo_posicao_falsa(f_num, a_isolado, b_isolado, tol)

                st.subheader("Resultados")
                st.success(f"**Raiz Aproximada:** `{raiz:.6f}` em {len(iteracoes)} iterações.")
                st.dataframe(pd.DataFrame(iteracoes))

            except Exception as e:
                st.error(f"Erro durante o cálculo: {e}")


# --- 2. RAÍZES DE EQUAÇÕES (Abertos: Newton) ---
elif metodo_selecionado == "3. Newton-Raphson":

    x0 = st.number_input("Chute Inicial (x0)", value=1.0, step=0.1, key="x0_n")

    if st.button("Executar Newton-Raphson"):
        try:
            raiz, iteracoes = metodo_newton_raphson(func_str, x0, tol)

            st.subheader("Resultados")
            st.success(f"**Raiz Aproximada:** `{raiz:.6f}` em {len(iteracoes)} iterações.")
            st.dataframe(pd.DataFrame(iteracoes))

        except Exception as e:
            st.error(f"Erro durante o cálculo de Newton-Raphson: {e}")


# --- 3. RAÍZES DE EQUAÇÕES (Abertos: Secante) ---
elif metodo_selecionado == "4. Secante":

    col_x_ant, col_x_i = st.columns(2)
    with col_x_ant:
        x_ant = st.number_input("Chute Inicial 1 (x_ant)", value=0.0, step=0.1, key="x_ant_s")
    with col_x_i:
        x_i = st.number_input("Chute Inicial 2 (x_i)", value=1.0, step=0.1, key="x_i_s")

    if st.button("Executar Secante"):
        try:
            raiz, iteracoes = metodo_secante(f_num, x_ant, x_i, tol)

            st.subheader("Resultados")
            st.success(f"**Raiz Aproximada:** `{raiz:.6f}` em {len(iteracoes)} iterações.")
            st.dataframe(pd.DataFrame(iteracoes))

        except Exception as e:
            st.error(f"Erro durante o cálculo da Secante: {e}")


# --- 4. RAÍZES DE EQUAÇÕES (Abertos: Ponto Fixo) ---
elif metodo_selecionado == "5. Ponto Fixo (Extra)":

    col_g, col_x0 = st.columns([3, 1])
    with col_g:
        g_str = st.text_input("Função de Iteração g(x) (Ex: np.cos(x))", key="g_str_pf", value="np.cos(x)")
    with col_x0:
        x0 = st.number_input("Chute Inicial (x0)", value=0.5, step=0.1, key="x0_pf")

    if st.button("Executar Ponto Fixo"):
        try:
            raiz, iteracoes = metodo_ponto_fixo(g_str, x0, tol)

            st.subheader("Resultados")
            st.success(f"**Raiz Aproximada:** `{raiz:.6f}` em {len(iteracoes)} iterações.")
            st.dataframe(pd.DataFrame(iteracoes))

        except Exception as e:
            st.error(f"Erro durante o cálculo de Ponto Fixo: {e}")


# --- 5. ELIMINAÇÃO DE GAUSS ---
elif metodo_selecionado == "6. Eliminação de Gauss":
    st.warning("Insira as matrizes como strings de listas JSON (Ex: [[2, 1], [1, 3]])")

    col_a, col_b = st.columns(2)
    with col_a:
        A_str = st.text_area("Matriz A (Ex: [[3, 2], [1, 2]])", value="[[3.0, 2.0], [1.0, 2.0]]")
    with col_b:
        b_str = st.text_input("Vetor b (Ex: [7, 5])", value="[7.0, 5.0]")

    if st.button("Executar Eliminação de Gauss"):
        A = parse_input_list(A_str, None)
        b = parse_input_list(b_str, None)

        try:
            solucao, M_final = metodo_eliminacao_gauss(A, b)

            st.subheader("Resultados")
            st.success(f"Vetor Solução X: `{solucao.round(6)}`")
            st.info("Matriz Aumentada [A | b] após o escalonamento:")
            st.dataframe(pd.DataFrame(M_final).round(6))

        except Exception as e:
            st.error(f"Erro durante o cálculo de Gauss: {e}")


# --- 6. INTERPOLAÇÃO (Lagrange e Newton) ---
elif metodo_selecionado in ["9. Lagrange", "10. Diferenças Divididas (Newton)"]:
    st.warning("Insira os pontos x e y como strings de listas JSON (Ex: [1, 2, 3])")

    col_x, col_y = st.columns(2)
    with col_x:
        x_str = st.text_input("Pontos X (Ex: [0, 1, 2])", value="[0.0, 1.0, 2.0]")
    with col_y:
        y_str = st.text_input("Pontos Y (Ex: [1, 2.718, 7.389])", value="[1.0, 2.718, 7.389]")

    x_interpolar = st.number_input("Valor de X para Interpolar:", value=0.5, step=0.1)

    if st.button(f"Executar {metodo_selecionado}"):
        x_pontos = parse_input_list(x_str, None)
        y_pontos = parse_input_list(y_str, None)

        if len(x_pontos) != len(y_pontos):
            st.error("As listas de pontos X e Y devem ter o mesmo número de elementos.")
            st.stop()

        try:
            if metodo_selecionado == "9. Lagrange":
                resultado = interpolacao_lagrange(x_pontos, y_pontos, x_interpolar)
                st.success(f"P({x_interpolar}) ≈ `{resultado:.6f}`")
            else:  # Diferenças Divididas (Newton)
                resultado, tabela = interpolacao_newton_diferencas_divididas(x_pontos, y_pontos, x_interpolar)
                st.success(f"P({x_interpolar}) ≈ `{resultado:.6f}`")
                st.subheader("Tabela de Diferenças")
                st.dataframe(pd.DataFrame(tabela))

        except Exception as e:
            st.error(f"Erro na Interpolação: {e}")


# --- 7. AJUSTE DE CURVAS (Mínimos Quadrados) ---
elif metodo_selecionado in ["11. Mínimos Quadrados (Reta)", "12. Mínimos Quadrados (Parábola)"]:
    st.warning("Insira os pontos x e y como strings de listas JSON (Ex: [1, 2, 3])")

    grau = 1 if "Reta" in metodo_selecionado else 2

    col_x, col_y = st.columns(2)
    with col_x:
        x_str = st.text_input("Pontos X (Ex: [1, 2, 3, 4])", value="[1.0, 2.0, 3.0, 4.0]")
    with col_y:
        y_str = st.text_input("Pontos Y (Ex: [1.5, 3.0, 4.0, 5.0])", value="[1.5, 3.0, 4.0, 5.0]")

    if st.button(f"Executar Ajuste de {metodo_selecionado}"):
        x_pontos = parse_input_list(x_str, None)
        y_pontos = parse_input_list(y_str, None)

        try:
            coeficientes, polinomio_str = ajuste_minimos_quadrados(x_pontos, y_pontos, grau)

            st.subheader("Resultado do Ajuste")
            st.success(f"Polinômio: **f(x) ≈ {polinomio_str}**")
            st.info(f"Coeficientes (c0, c1, ...): `{coeficientes.round(6)}`")

        except Exception as e:
            st.error(f"Erro no Ajuste de Curvas: {e}")


# --- 8. INTEGRAÇÃO NUMÉRICA (Trapézio e Simpson) ---
elif metodo_selecionado in ["13. Regra do Trapézio", "14. 1/3 de Simpson"]:

    col_a, col_b, col_n = st.columns(3)
    with col_a:
        a = st.number_input("Limite Inferior (a)", value=0.0, step=0.1)
    with col_b:
        b = st.number_input("Limite Superior (b)", value=1.0, step=0.1)
    with col_n:
        n = st.number_input("Subintervalos (n)", value=10, min_value=2, step=2)

    if st.button(f"Executar {metodo_selecionado}"):

        try:
            if metodo_selecionado == "13. Regra do Trapézio":
                integral = regra_trapezio(f_num, a, b, n)
            else:  # 1/3 de Simpson
                integral = regra_simpson_1_3(f_num, a, b, n)

            st.subheader("Resultado")
            st.success(f"Valor da Integral ≈ `{integral:.6f}`")

        except ValueError as ve:
            st.error(f"Erro de Validação: {ve}")
        except Exception as e:
            st.error(f"Erro durante a Integração Numérica: {e}")