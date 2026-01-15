================================================================================
DASHBOARD DE VENDAS - MERCADO LIVRE
================================================================================

DESCRIÇÃO:
Dashboard interativo desenvolvido em Streamlit para análise de dados de vendas 
do Mercado Livre. Fornece visualizações de receita, desempenho por produto, 
sazonalidade e análise geográfica de vendas.

FUNCIONALIDADES:
- Métricas principais: Receita Total, Pedidos, Ticket Médio, Receita Ads e 
  Receita Orgânica
- Evolução de vendas ao longo do tempo (gráfico de linha)
- Análise de sazonalidade por dia da semana e hora do dia
- Ranking de produtos e sabores por receita
- Análise geográfica de vendas por estado
- Filtros interativos: Data, Publicidade, Estado, Produto e Sabor
- Visualização completa do dataset

REQUISITOS:
- Python 3.8+
- Bibliotecas listadas em requirements.txt

INSTALAÇÃO:
1. Clone ou baixe o projeto
2. Instale as dependências:
   pip install -r requirements.txt

COMO EXECUTAR:
1. Coloque o arquivo de dados (vendas_mercado_livre_2023.csv) na pasta 
   'datasets/'
2. Certifique-se de que o arquivo de logo está em 'images/mercado-livre-logo-8.png'
3. Execute o comando:
   streamlit run home.py

4. A aplicação será aberta no navegador (localhost:8501)

ESTRUTURA DO PROJETO:
- home.py                              : Arquivo principal da aplicação
- requirements.txt                     : Dependências do projeto
- datasets/vendas_mercado_livre_2023.csv : Dados de vendas
- images/mercado-livre-logo-8.png      : Logo da aplicação

DADOS ESPERADOS:
O arquivo CSV deve conter as seguintes colunas:
- Data da venda
- Data a caminho completa
- Data de entrega completa
- Unidades
- Reclamação encerrada
- N.º de venda
- Tarifa de venda e impostos
- Tarifas de envio
- Cancelamentos e reembolsos (BRL)
- Receita por produtos (BRL)
- Venda por publicidade
- Estado
- Título do anúncio
- Variação

DESENVOLVIDO POR:
Renato Perussi

DATA DE CRIAÇÃO:
Janeiro de 2026
================================================================================
