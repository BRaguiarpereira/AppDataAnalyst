import streamlit as st # responsavel por pegar o dados e exibilos na interface web
import pandas as pd # prepara para ler dados
import matplotlib.pyplot as plt # criar graficos gerar parte visual

st.title("Análise de Vendas")

# 1. Coleta de Dados (simulando upload ou leitura direta)
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("Arquivo carregado com sucesso!")

    # 2. Pré-processamento (ex: converter Data para datetime)
    df['Data'] = pd.to_datetime(df['Data'])

    st.subheader("Dados Brutos (Primeiras 5 linhas)")
    st.write(df.head())

    # 3. Análise Exploratória e Visualização
    st.subheader("Métricas de Vendas")
    total_vendas = df['Vendas'].sum()
    st.metric("Total de Vendas", f"R$ {total_vendas:,.2f}")

    vendas_por_produto = df.groupby('Produto')['Vendas'].sum().sort_values(ascending=False)
    st.subheader("Vendas por Produto")
    st.bar_chart(vendas_por_produto)

    vendas_por_regiao = df.groupby('Regiao')['Vendas'].sum().sort_values(ascending=False)
    st.subheader("Vendas por Região")
    st.bar_chart(vendas_por_regiao)

    # Gráfico de Vendas ao longo do tempo
    st.subheader("Vendas ao Longo do Tempo")
    vendas_diarias = df.groupby('Data')['Vendas'].sum()
    fig, ax = plt.subplots()
    ax.plot(vendas_diarias.index, vendas_diarias.values)
    ax.set_xlabel("Data")
    ax.set_ylabel("Vendas")
    ax.set_title("Vendas Diárias")
    st.pyplot(fig)

    # Insights Adicionais (ex: Top 3 produtos)
    st.subheader("Insights")
    st.write(f"O produto mais vendido é: **{vendas_por_produto.index[0]}**")
    st.write(f"A região com maior volume de vendas é: **{vendas_por_regiao.index[0]}**")

else:
    st.info("Por favor, carregue um arquivo CSV para começar a análise.")