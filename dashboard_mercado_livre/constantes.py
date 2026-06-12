"""Constantes do projeto: caminhos, chaves de colunas e parâmetros."""

from pathlib import Path

# Diretórios e arquivos
RAIZ_PROJETO = Path(__file__).resolve().parents[1]
CAMINHO_DADOS = RAIZ_PROJETO / "dados" / "vendas_mercado_livre_2023.csv"
CAMINHO_LOGO = RAIZ_PROJETO / "imagens" / "mercado-livre-logo-8.png"

# Colunas do dataset
COLUNAS_DATAS = [
    "Data da venda",
    "Data a caminho completa",
    "Data de entrega completa",
]
COLUNAS_INTEIRO = ["Unidades", "Reclamação encerrada"]
COLUNAS_STRING = ["N.º de venda"]
COLUNAS_ABSOLUTAS = [
    "Tarifa de venda e impostos",
    "Tarifas de envio",
    "Cancelamentos e reembolsos (BRL)",
]

COLUNA_RECEITA = "Receita por produtos (BRL)"
COLUNA_PUBLICIDADE = "Venda por publicidade"
COLUNA_ESTADO = "Estado"
COLUNA_PRODUTO = "Título do anúncio"
COLUNA_VARIACAO = "Variação"
COLUNA_NUMERO_VENDA = "N.º de venda"

# Colunas temporais derivadas
COLUNAS_TEMPORAIS_STR = [
    "Ano_Mes", "Ano", "Mes", "Dia", "Hora", "Minuto",
    "Dia_Semana", "Trimestre", "Dia_Nome", "Mes_Nome",
]

# Locale
LOCALE_BR = "pt_BR.UTF-8"

# Tamanho dos rankings
TOP_N = 10

# Valores da coluna de publicidade
VALOR_ADS = "Sim"
VALOR_ORGANICO = "Não"
