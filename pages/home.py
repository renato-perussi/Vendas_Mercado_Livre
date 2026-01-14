import streamlit as st
import pandas as pd
import datetime as dt
import plotly.express as px

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

@st.cache_data
def etl(caminho_arquivo):

    df = pd.read_csv(caminho_arquivo)

    #Colunas para alteração de Tipo.

    colunas_datas = ['Data da venda', 'Data a caminho completa', 'Data de entrega completa']
    colunas_int = ['Unidades', 'Reclamação encerrada']
    colunas_strings = ['N.º de venda', 'CEP']
    alterando_tipo(df, colunas_datas, tipo='datetime')
    alterando_tipo(df, colunas_strings, tipo='str')
    alterando_tipo(df, colunas_int, tipo='int')


    #Convertendo valores negativos em absolutos.

    colunas_absolutas = ['Tarifa de venda e impostos', 'Tarifas de envio', 'Cancelamentos e reembolsos (BRL)']
    numeros_absolutos(df, colunas_absolutas)


    #Criando colunas temporais para análise

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


    #Convertendo colunas temporais para Strings

    colunas_strings = 'Ano_Mes Ano Mes Dia Hora Minuto Dia_Semana Trimestre Dia_Nome Mes_Nome'.split()
    alterando_tipo(df, colunas=colunas_strings, tipo='str') # Alterando o Tipo para String.


    # Ordenando o DF pela coluna 'Data da Venda'

    df = df.sort_values('Data da venda').reset_index(drop=True)

    return df


def main():

    # ETL

    caminho_arquivo = '../datasets/vendas_mercado_livre_2023.csv'
    df = etl(caminho_arquivo)


    # Streamlit

    # Set page config

    st.set_page_config(
        page_title='Dashboard_Mercado_Livre',
        layout='wide'
    )


    # Start Sidebar

    st.sidebar.header('Filtros:')

    data_min = df['Data da venda'].min()
    data_max = df['Data da venda'].max()
    data_inicial = st.sidebar.date_input('Data Inicial:', data_min)
    data_final = st.sidebar.date_input('Data Final:', data_max)

    st.sidebar.divider()

    check_box = st.sidebar.checkbox('Publicidade / Orgânico')

    # Filtered DataFrame
    df = df[(df['Data da venda'] >= data_inicial) & (df['Data da venda'] <= data_final)]


    # Starts Main Page

    st.image(image='../images/mercado-livre-logo-8.png', width=250)

    st.write('')
    st.write('')

    col1, col2, col3, col4, col5 = st.columns(5, gap='small', vertical_alignment='top')

    with col1:
        receita_total = df['Receita por produtos (BRL)'].sum().round(2)
        st.metric('Receita Total:', value = f'R$ {receita_total}')

    with col2:
        pedido_total = df['N.º de venda'].nunique()
        st.metric('Pedidos:', value = f'{pedido_total}')

    with col3:
        ticket_medio = round(receita_total / pedido_total, 2)
        st.metric('Ticket Médio:', value = f'R$ {ticket_medio}')

    with col4:
        receita_ads = df[df['Venda por publicidade'] == 'Sim']['Receita por produtos (BRL)'].sum().round(2)
        st.metric('Receita Ads:', value = f'R$ {receita_ads}')

    with col5:
        receita_organico = df[df['Venda por publicidade'] == 'Não']['Receita por produtos (BRL)'].sum().round(2)
        st.metric('Receita Orgânico:', value = f'R$ {receita_organico}')


    st.divider()


    receita = df.groupby('Ano_Mes')['Receita por produtos (BRL)'].sum().round(2).reset_index()

    fig = px.line(data_frame = receita, x = 'Ano_Mes', y = 'Receita por produtos (BRL)', title= 'Evolução da Receita Mensal', markers = 'o', hover_name = 'Ano_Mes')
    st.plotly_chart(fig)

    if check_box:
        fig = px.histogram(data_frame = df, x = 'Ano_Mes', y = 'Receita por produtos (BRL)', title = 'Receita Ads/Orgânico ao Mês', color = 'Venda por publicidade', hover_name = 'Ano_Mes', barmode = 'group')
        st.plotly_chart(fig)


    col1, col2 = st.columns(2)

    with col1:
        receita_dia = df.groupby('Dia_Semana')['Receita por produtos (BRL)'].sum().round(2).reset_index()
        fig = px.bar(data_frame = receita_dia, x = 'Dia_Semana', y = 'Receita por produtos (BRL)', title='Receita por Dia da Semana (Sazonalidade)', subtitle='A Semana começa na Segunda-Feira = 0', hover_name='Dia_Semana')
        st.plotly_chart(fig)

    with col2:
        receita_hora = df.groupby('Hora')['Receita por produtos (BRL)'].sum().round(2).reset_index()
        fig = px.bar(data_frame = receita_hora, x = 'Hora', y = 'Receita por produtos (BRL)', title = 'Receita por Hora do Dia (Sazonalidade)', hover_name = 'Hora')
        st.plotly_chart(fig)

    if check_box:
        with col1:
            fig = px.histogram(data_frame = df, x = 'Dia_Semana', y = 'Receita por produtos (BRL)', title='Receita Ads/Orgânico por Dia da Semana', color = 'Venda por publicidade', hover_name='Dia_Semana', barmode='group')
            fig.update_traces(hovertemplate = None)
            fig.update_layout(hovermode = 'x unified')
            st.plotly_chart(fig)
        
        with col2:
            fig = px.histogram(data_frame = df, x = 'Hora', y = 'Receita por produtos (BRL)', title = 'Receita Ads/Orgânico por Hora', color = 'Venda por publicidade', hover_name = 'Hora', barmode = 'group', nbins = 24)
            fig.update_traces(hovertemplate = None)
            fig.update_layout(hovermode = 'x unified')
            st.plotly_chart(fig)


    tempo_medio_pedido = df.groupby('Ano_Mes')['Dias_Delta_Total'].mean().round(2).reset_index()
    fig = px.line(data_frame=tempo_medio_pedido, x = 'Ano_Mes', y = 'Dias_Delta_Total', title='Tempo Médio de Entrega do Pedido (Dias) ao Mês', markers='o', hover_name='Ano_Mes')
    st.plotly_chart(fig)


    st.divider()


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

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        receita_estados = df.groupby('Estado')['Receita por produtos (BRL)'].sum().round(2).reset_index().sort_values('Receita por produtos (BRL)')
        fig = px.bar(data_frame = receita_estados, x = 'Receita por produtos (BRL)', y = 'Estado', title = 'Receita por Estado', hover_name = 'Estado')
        st.plotly_chart(fig)

    with col2:
        fig = px.pie(data_frame = receita_estados, values = 'Receita por produtos (BRL)', hole = 0.4, title = 'Proporção da Receita por Estado (%)', hover_name = 'Estado', names = 'Estado')
        st.plotly_chart(fig)

    if check_box:
        fig = px.histogram(data_frame = df, x = 'Receita por produtos (BRL)', y = 'Estado', color = 'Venda por publicidade', title = 'Receita por Estado Ads/ Orgânico', barmode = 'group')
        fig.update_yaxes(categoryorder = 'total ascending')
        st.plotly_chart(fig, height = 700)

    st.divider()

    st.markdown('#### Tabela de Dados')
    st.dataframe(df)


if __name__ == '__main__':
    main()
