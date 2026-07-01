import numpy as np

def media_movel(dados, semanas):

    historico = dados.copy()

    previsoes = []

    for _ in range(semanas):

        media = sum(historico[-4:]) / 4

        previsoes.append(media)

        historico.append(media)

    return previsoes

def suavizacao_exponencial(dados, semanas, alpha=0.3):
    previsoes = []
    previsao = dados[0]

    for i in range(semanas):
        previsao = alpha * dados[-1] + (1 - alpha) * previsao
        previsoes.append(previsao)

    return previsoes

def regressao_linear(dados, semanas):

    x = np.arange(1, len(dados) + 1)

    y = np.array(dados)

    coef_angular, coef_linear = np.polyfit(x, y, 1)

    futuras = np.arange(
        len(dados) + 1,
        len(dados) + semanas + 1
    )

    previsoes = coef_angular * futuras + coef_linear

    return previsoes.tolist()