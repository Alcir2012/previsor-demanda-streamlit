from utils.previsoes import media_movel,suavizacao_exponencial,regressao_linear

def calcular_mae(valores_reais, previsoes):

    erros = []

    for real, previsto in zip(valores_reais, previsoes):
        erros.append(abs(real - previsto))

    return sum(erros) / len(erros)

def calcular_mae_metodo(dados, metodo):

    previsoes = []

    valores_reais = []

    for i in range(4, len(dados)):

        historico = dados[:i]

        if metodo == "Média Móvel":
            previsto = media_movel(historico, 1)[0]

        elif metodo == "Suavização Exponencial":
            previsto = suavizacao_exponencial(historico, 1)[0]

        elif metodo == "Regressão Linear":
            previsto = regressao_linear(historico, 1)[0]

        previsoes.append(previsto)

        valores_reais.append(dados[i])

    return calcular_mae(valores_reais, previsoes)
