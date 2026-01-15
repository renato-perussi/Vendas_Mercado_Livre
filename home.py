import streamlit as st
import pandas as pd
import datetime as dt
import plotly.express as px
import locale

# Functions

def alterando_tipo(df, colunas, tipo):

        if tipo == 'datetime':
            for coluna in colunas:
                df[coluna] = pd.to_datetime(df[coluna])

        elif tipo == 'str':
            for coluna in colunas:
                df[coluna] = df[coluna].astype(str)

        elif tipo == 'int':
            for coluna in colunas:
                df[coluna] = df[coluna].astype(int)

        elif tipo == 'float':
            for coluna in colunas:
                df[coluna] = df[coluna].astype(float)


def numeros_absolutos(df, colunas):
    for coluna in colunas:
        df[coluna] = df[coluna].abs()


def alterando_moeda_local(value):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    return locale.currency(value, grouping=True)
    

@st.cache_data
def etl(caminho_arquivo):

    df = pd.read_csv(caminho_arquivo)

    # Colunas para alteração de Tipo.

    colunas_datas = ['Data da venda', 'Data a caminho completa', 'Data de entrega completa']
    colunas_int = ['Unidades', 'Reclamação encerrada']
    colunas_strings = ['N.º de venda']
    alterando_tipo(df, colunas_datas, tipo='datetime')
    alterando_tipo(df, colunas_strings, tipo='str')
    alterando_tipo(df, colunas_int, tipo='int')


    # Convertendo valores negativos em absolutos.

    colunas_absolutas = ['Tarifa de venda e impostos', 'Tarifas de envio', 'Cancelamentos e reembolsos (BRL)']
    numeros_absolutos(df, colunas_absolutas)


    # Criando colunas temporais para análise

    data_base = df['Data da venda']
    df['Ano_Mes'] = data_base.dt.to_period('M')
    df['Ano'] = data_base.dt.year
    df['Mes'] = data_base.dt.month
    df['Dia'] = data_base.dt.day
    df['Hora'] = data_base.dt.hour
    df['Minuto'] = data_base.dt.minute
    df['Dia_Semana'] = data_base.dt.weekday
    df['Trimestre'] = data_base.dt.to_period('Q').astype(str).apply(lambda x: x[-2:])
    df['Dia_Nome'] = data_base.dt.day_name()
    df['Mes_Nome'] = data_base.dt.month_name()
    df['Time_Delta_Caminho'] = df['Data a caminho completa'] - df['Data da venda']
    df['Time_Delta_Entrega'] = df['Data de entrega completa'] - df['Data a caminho completa']
    df['Time_Delta_Total'] = df['Data de entrega completa'] - df['Data da venda']
    df['Dias_Delta_Caminho'] = df['Time_Delta_Caminho'].dt.days
    df['Horas_Delta_Caminho'] = df['Time_Delta_Caminho'].dt.seconds // 3600
    df['Minutos_Delta_Caminho'] = (df['Time_Delta_Caminho'].dt.seconds % 3600) // 60
    df['Dias_Delta_Entrega'] = df['Time_Delta_Entrega'].dt.days
    df['Horas_Delta_Entrega'] = df['Time_Delta_Entrega'].dt.seconds // 3600
    df['Minutos_Delta_Entrega'] = (df['Time_Delta_Entrega'].dt.seconds % 3600) // 60
    df['Dias_Delta_Total'] = df['Time_Delta_Total'].dt.days
    df['Horas_Delta_Total'] = df['Time_Delta_Total'].dt.seconds // 3600
    df['Minutos_Delta_Total'] = (df['Time_Delta_Total'].dt.seconds % 3600) // 60

    df['Data da venda'] = df['Data da venda'].dt.date   # Convertendo a coluna Data de datetime para date


    # Convertendo colunas temporais para Strings

    colunas_strings = 'Ano_Mes Ano Mes Dia Hora Minuto Dia_Semana Trimestre Dia_Nome Mes_Nome'.split()
    alterando_tipo(df, colunas=colunas_strings, tipo='str') # Alterando o Tipo para String.


    # Ordenando o DF pela coluna 'Data da Venda'

    df = df.sort_values('Data da venda').reset_index(drop=True)

    return df


# Main

if __name__ == '__main__':

    # ETL

    caminho_arquivo = 'datasets/vendas_mercado_livre_2023.csv'
    df = etl(caminho_arquivo)


    # Streamlit

    # Page config

    st.set_page_config(
        page_title='Dashboard_Mercado_Livre',
        layout='wide'
    )


    # Sidebar

    st.sidebar.title('Dashboard - Vendas Mercado Livre')

    st.sidebar.header('Filtros:')

    data_min = df['Data da venda'].min()
    data_max = df['Data da venda'].max()
    data_inicial = st.sidebar.date_input('Data Inicial:', data_min)
    data_final = st.sidebar.date_input('Data Final:', data_max)

    ads = df['Venda por publicidade'].unique().tolist()
    ads_selecionados = st.sidebar.multiselect('Venda por publicidade:', ads, default=ads)

    estados = df['Estado'].unique().tolist()
    estados_selecionados = st.sidebar.multiselect('Estados:', estados, default=estados)

    produtos = df['Título do anúncio'].unique().tolist()
    produtos_selecionados = st.sidebar.multiselect('Produtos:', produtos, default=produtos)

    sabor = df['Variação'].unique().tolist()
    sabor_selecionados = st.sidebar.multiselect('Sabores:', sabor, default=sabor)
    
    st.sidebar.divider()

    st.sidebar.markdown('Developed by Renato Perussi')

    # Data Frame filtrado

    df = df[(df['Data da venda'] >= data_inicial) & (df['Data da venda'] <= data_final) & (df['Estado'].isin(estados_selecionados)) & (df['Título do anúncio'].isin(produtos_selecionados)) & (df['Variação'].isin(sabor_selecionados)) & (df['Venda por publicidade'].isin(ads_selecionados))]


    # Pagina principal

    st.image(image='images/mercado-livre-logo-8.png', width=250)

    st.write('')
    st.write('')

    # Métricas principais
    
    col1, col2, col3, col4, col5 = st.columns(5, gap='small', vertical_alignment='top')

    with col1:
        receita_total = df['Receita por produtos (BRL)'].sum().round(2)
        st.metric('Receita Total:', value = f'{alterando_moeda_local(receita_total)}')

    with col2:
        pedido_total = df['N.º de venda'].nunique()
        st.metric('Pedidos:', value = f'{pedido_total}')

    with col3:
        ticket_medio = round(receita_total / pedido_total, 2)
        st.metric('Ticket Médio:', value = f'{alterando_moeda_local(ticket_medio)}')
    with col4:
        receita_ads = df[df['Venda por publicidade'] == 'Sim']['Receita por produtos (BRL)'].sum().round(2)
        st.metric('Receita Ads:', value = f'{alterando_moeda_local(receita_ads)}')

    with col5:
        receita_organico = df[df['Venda por publicidade'] == 'Não']['Receita por produtos (BRL)'].sum().round(2)
        st.metric('Receita Orgânico:', value = f'{alterando_moeda_local(receita_organico)}')


    st.divider()


    # Gráficos e Análises

    receita = df.groupby('Ano_Mes')['Receita por produtos (BRL)'].sum().round(2).reset_index()

    st.markdown('### Evolução das Vendas')

    fig = px.line(data_frame = receita, x = 'Ano_Mes', y = 'Receita por produtos (BRL)', title= 'Evolução da Receita Mensal', markers = 'o', labels={'Ano_Mes': 'Ano e Mês', 'Receita por produtos (BRL)': 'Vendas (R$)'})

    st.plotly_chart(fig)


    st.markdown('### Sazonalidade')

    col1, col2 = st.columns(2)

    with col1:
        receita_dia = df.groupby('Dia_Semana')['Receita por produtos (BRL)'].sum().round(2).reset_index()
        fig = px.bar(data_frame = receita_dia, x = 'Dia_Semana', y = 'Receita por produtos (BRL)', title='Receita por Dia da Semana', subtitle='A Semana começa na Segunda-Feira = 0', labels={'Dia_Semana': 'Dia da Semana', 'Receita por produtos (BRL)': 'Vendas (R$)'})
        st.plotly_chart(fig)

    with col2:
        receita_hora = df.groupby('Hora')['Receita por produtos (BRL)'].sum().round(2).reset_index()
        fig = px.bar(data_frame = receita_hora, x = 'Hora', y = 'Receita por produtos (BRL)', title = 'Receita por Hora do Dia', labels={'Hora': 'Hora do Dia', 'Receita por produtos (BRL)': 'Vendas (R$)'})
        st.plotly_chart(fig)


    # Tabelas

    st.markdown('### Vendas por Produto')

    produtos_ranking = df.groupby('Título do anúncio')['Receita por produtos (BRL)'].sum().round(2).sort_values(ascending = False).head(10)
    produto_min = produtos_ranking.min()
    produto_max = produtos_ranking.max()

    sabores_ranking = df.groupby('Variação')['Receita por produtos (BRL)'].sum().round(2).sort_values(ascending = False).head(10)
    sabor_min = sabores_ranking.min()
    sabor_max = sabores_ranking.max()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('###### Receita por Produto')
        st.dataframe(
            produtos_ranking,
            column_config={
                'Receita por produtos (BRL)': st.column_config.ProgressColumn('Receita por produtos (BRL)', min_value = produto_min, max_value = produto_max, format = 'R$ %f', color = 'blue')
            }
        )

    with col2:
        st.markdown('###### Receita por Sabor')
        st.dataframe(
            sabores_ranking,
            column_config={
                'Receita por produtos (BRL)': st.column_config.ProgressColumn('Receita por produtos (BRL)', min_value = sabor_min, max_value = sabor_max, format = 'R$ %f', color = 'blue')
            }
        )

    
    # Análises por estado

    st.markdown('### Vendas por Localidade')

    col1, col2 = st.columns(2)

    with col1:
        receita_estados = df.groupby('Estado')['Receita por produtos (BRL)'].sum().round(2).reset_index().sort_values('Receita por produtos (BRL)')
        fig = px.bar(data_frame = receita_estados, x = 'Receita por produtos (BRL)', y = 'Estado', title = 'Receita por Estado', labels={'Receita por produtos (BRL)': 'Vendas (R$)', 'Estado': 'Estado'})
        st.plotly_chart(fig)

    with col2:
        fig = px.pie(data_frame = receita_estados, values = 'Receita por produtos (BRL)', hole = 0.4, title = 'Proporção da Receita por Estado (%)',names = 'Estado')
        st.plotly_chart(fig)


    st.markdown('### Dataset Completo')
    st.dataframe(df)