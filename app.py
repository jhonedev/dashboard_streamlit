import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1 - Importando os dados
data = pd.read_csv('data/Pedidos.csv')
df = pd.DataFrame(data)
# print(df)

def main():
    st.title('Dashboard de vendas :shopping_trolley:')

    # Filtros
    st.sidebar.header('Filtros')
    selected_region = st.sidebar.multiselect(
        'Selecione as regiões',
        data['Regiao'].unique(),
        data['Regiao'].unique()
    )
    filtered_data = data[data['Regiao'].isin(selected_region)]

    aba1, aba2, aba3 = st.tabs(['Dataset', 'Receita', 'Vendedores'])
    with aba1:
        display_dataframe(filtered_data)
    with aba2:
        display_charts(filtered_data)
    with aba3:
        display_metrics(filtered_data)

# Função para exibir o dataframe
def display_dataframe(data):
    st.header('Visualização do dataframe')
    st.write(data)

# Função para exibir os gráficos
def display_charts(data):
    st.header('Visualização de gráficos')
    st.set_option('deprecation.showPyplotGlobalUse', False)

    # Gráfico 1: Desempenho por região
    st.subheader('Desempenho por região')
    plt.figure(figsize=(10, 6))
    sns.countplot(x='Regiao', data=data)
    st.pyplot()

    # Gráfico 2: Itens mais vendidos
    st.subheader('Itens mais vendidos')
    plt.figure(figsize=(10, 6))
    sns.countplot(x='Item', data=data)
    st.pyplot()

    # Gráfico 3: Preço médio por item
    st.subheader('Preço médio por ítem')
    avg_price = data.groupby('Item')['PrecoUnidade'].mean().sort_values(ascending=False)
    formatted_avg_price = avg_price.map(lambda x: f'R$ {x:.2f}')
    st.write(formatted_avg_price)

# Função para exibir métricas
def display_metrics(data):
    st.subheader('Métricas')

    if not data.empty:
        # Métricas simples
        total_sales = data['Unidades'].sum()
        average_price = data['PrecoUnidade'].mean()
        most_productive = data['Vendedor'].value_counts().idxmax()

        coluna1, coluna2, coluna3 = st.columns(3)
        with coluna1:
            st.metric('O vendedor mais produtivo foi:', most_productive)
        with coluna2:
            st.metric('Vendas totais:', total_sales)
        with coluna3:
            st.metric('Preço médio:', f'R$ {average_price:.2f}')
    else:
        st.write('Nenhum dado disponível para exibir métricas!')

# Execuçã do aplicativo
if __name__ == '__main__':
    main()