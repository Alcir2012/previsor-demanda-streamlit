import pandas as pd
import plotly.express as px

def grafico_comparativo(
    historico,
    previsao_media,
    previsao_suavizacao,
    previsao_regressao
):

    semanas_hist = list(range(1, len(historico) + 1))
    semanas_prev = list(range(len(historico) + 1,
                              len(historico) + 5))

    df = pd.DataFrame()

    # Histórico
    df_hist = pd.DataFrame({
        "Semana": semanas_hist,
        "Vendas": historico,
        "Tipo": "Histórico"
    })

    # Média móvel
    df_media = pd.DataFrame({
        "Semana": semanas_prev,
        "Vendas": previsao_media,
        "Tipo": "Média Móvel"
    })

    # Suavização
    df_suav = pd.DataFrame({
        "Semana": semanas_prev,
        "Vendas": previsao_suavizacao,
        "Tipo": "Suavização"
    })

    # Regressão
    df_reg = pd.DataFrame({
        "Semana": semanas_prev,
        "Vendas": previsao_regressao,
        "Tipo": "Regressão"
    })

    df = pd.concat([
        df_hist,
        df_media,
        df_suav,
        df_reg
    ])

    fig = px.line(
        df,
        x="Semana",
        y="Vendas",
        color="Tipo",
        markers=True
    )

    return fig