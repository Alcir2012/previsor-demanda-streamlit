import streamlit as st
import pandas as pd
from utils.previsoes import media_movel,suavizacao_exponencial,regressao_linear
from utils.graficos import grafico_comparativo
from utils.metricas import calcular_mae_metodo

# ==========================================
# Configuração da página
# ==========================================

st.set_page_config(
    page_title="Previsor de Demanda",
    page_icon="📈",
    layout="wide"
)

# ==========================================
# Título
# ==========================================

st.title("📈 Previsor de Demanda Semanal")

st.write(
    "Auxiliador de planejamento da produção utilizando métodos de previsão de demanda."
)

st.divider()

# ==========================================
# Entrada de dados
# ==========================================

produto = st.text_input(
    "Nome do Produto",
    placeholder="Ex.: Arroz 5kg"
)

st.subheader("Histórico de vendas")

dados = []

col1, col2 = st.columns(2)

with col1:
    for i in range(1, 5):
        valor = st.number_input(
            f"Semana {i} - Unidades vendidas",
            min_value=0,
            value=0,
            key=f"semana_{i}"
        )
        dados.append(valor)

with col2:
    for i in range(5, 9):
        valor = st.number_input(
            f"Semana {i} - Unidades vendidas",
            min_value=0,
            value=0,
            key=f"semana_{i}"
        )
        dados.append(valor)

with col1:

    metodos = st.selectbox(
        "Métodos de previsão",
        [
            "Média Móvel",
            "Suavização Exponencial",
            "Regressão Linear"
        ],
        index=0
    )

with col2:

    semanas = st.number_input(
        "Quantidade de semanas futuras",
        min_value=1,
        max_value=4,
        value=4
    )

st.divider()

# ==========================================
# Botão
# ==========================================

if st.button("Calcular Previsão"):

    # Validações
    if not produto.strip():
        st.error("Informe o nome do produto.")
        st.stop()

    if any(valor <= 0 for valor in dados):
        st.error("Informe as vendas das quatro semanas.")
        st.stop()

    # Calcula todos os métodos
    previsao_media = media_movel(dados, semanas)

    previsao_suavizacao = suavizacao_exponencial(dados, semanas)

    previsao_regressao = regressao_linear(dados, semanas)

    # Escolhe qual mostrar na tabela
    if metodos == "Média Móvel":
        previsoes = previsao_media

    elif metodos == "Suavização Exponencial":
        previsoes = previsao_suavizacao

    else:
        previsoes = previsao_regressao

    # ===============================
    # Tabela
    # ===============================

    st.write("Método selecionado:",metodos)
    df = pd.DataFrame({
        "Semana": list(range(5, 5 + semanas)),
        "Previsão de vendas": previsoes
    })

    df["Previsão de vendas"] = df["Previsão de vendas"].round(2)

    st.dataframe(df)

    # ===============================
    # Gráfico
    # ===============================

    st.subheader("Comparativo entre os Métodos de Previsão")

    fig = grafico_comparativo(
    dados,
    previsao_media,
    previsao_suavizacao,
    previsao_regressao
)
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "O gráfico apresenta o histórico de vendas informado pelo usuário e as previsões geradas pelos métodos de Média Móvel, Suavização Exponencial e Regressão Linear."
    )
    st.divider()

    st.subheader("Comparação dos Métodos")


    mae_media = calcular_mae_metodo(dados, "Média Móvel")
    mae_suavizacao = calcular_mae_metodo(dados, "Suavização Exponencial")
    mae_regressao = calcular_mae_metodo(dados, "Regressão Linear")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Média Móvel", f"{mae_media:.2f}")

    with col2:
        st.metric("Suavização", f"{mae_suavizacao:.2f}")

    with col3:
        st.metric("Regressão", f"{mae_regressao:.2f}")

        maes = {
    "Média Móvel": mae_media,
    "Suavização Exponencial": mae_suavizacao,
    "Regressão Linear": mae_regressao
}

    melhor_metodo = min(maes, key=maes.get)

    st.success(
        f"O método recomendado é **{melhor_metodo}**, "
        f"pois apresentou o menor Erro Médio Absoluto (MAE): **{maes[melhor_metodo]:.2f}**."
    )

    st.divider()

    st.subheader("Análise Gerencial")
    ultima_venda = dados[-1]
    proxima_previsao = previsoes[0]
    variacao = proxima_previsao - ultima_venda

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Método utilizado",
            metodos
        )

    with col2:
        st.metric(
            "Última venda",
            f"{ultima_venda:.0f} unidades"
        )

    with col3:
        st.metric(
            "Próxima previsão",
            f"{proxima_previsao:.2f} unidades",
            delta=f"{variacao:.2f}"
        )

    if variacao > 10:

        st.success(
            "A previsão indica crescimento da demanda. Recomenda-se aumentar o estoque e planejar maior produção."
        )

    elif variacao < -10:

        st.warning(
            "A previsão indica redução da demanda. Recomenda-se revisar o planejamento para evitar excesso de estoque."
        )

    else:

        st.info(
            "A demanda apresenta estabilidade. Recomenda-se manter o planejamento atual."
        )
    percentual = (variacao / ultima_venda) * 100

    st.write(
        f"**Variação prevista:** {percentual:.2f}% em relação à última semana."
    )