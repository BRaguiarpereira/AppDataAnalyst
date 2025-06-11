import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import kagglehub
import os

st.set_page_config(layout="wide")

st.title("Explorador de Dados de E-commerce Brasileiro")

# Download da versão mais recente do dataset
with st.spinner("Baixando o dataset do Kaggle... Isso pode levar um momento."):
    try:
        path = kagglehub.dataset_download("olistbr/brazilian-ecommerce")
        st.success(f"Dataset baixado para: {path}")
    except Exception as e:
        st.error(f"Erro ao baixar o dataset do Kaggle: {e}")
        st.stop() # Interrompe o app se o download falhar

# Função para carregar dados
@st.cache_data
def load_data(file_name):
    file_path = os.path.join(path, file_name)
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        st.error(f"Arquivo não encontrado: {file_path}")
        return pd.DataFrame() # Retorna um DataFrame vazio em caso de erro

# Carregar datasets
st.subheader("Carregando DataFrames")
try:
    customers_df = load_data("olist_customers_dataset.csv")
    orders_df = load_data("olist_orders_dataset.csv")
    order_items_df = load_data("olist_order_items_dataset.csv")
    products_df = load_data("olist_products_dataset.csv")
    sellers_df = load_data("olist_sellers_dataset.csv")
    product_category_name_translation_df = load_data("product_category_name_translation.csv")
    geolocation_df = load_data("olist_geolocation_dataset.csv")
    order_payments_df = load_data("olist_order_payments_dataset.csv")
    order_reviews_df = load_data("olist_order_reviews_dataset.csv")

    st.success("Todos os datasets carregados com sucesso!")

except Exception as e:
    st.error(f"Erro ao carregar um ou mais datasets: {e}")
    st.stop()




## Visão Geral dos Dados

#Selecione um dataset para ver seu cabeçalho e formato:
selected_dataset = st.selectbox(
    "Escolha um dataset:",
    ["customers_df", "orders_df", "order_items_df", "products_df",
     "sellers_df", "product_category_name_translation_df",
     "geolocation_df", "order_payments_df", "order_reviews_df"]
)

if selected_dataset == "customers_df":
    df_to_display = customers_df
elif selected_dataset == "orders_df":
    df_to_display = orders_df
elif selected_dataset == "order_items_df":
    df_to_display = order_items_df
elif selected_dataset == "products_df":
    df_to_display = products_df
elif selected_dataset == "sellers_df":
    df_to_display = sellers_df
elif selected_dataset == "product_category_name_translation_df":
    df_to_display = product_category_name_translation_df
elif selected_dataset == "geolocation_df":
    df_to_display = geolocation_df
elif selected_dataset == "order_payments_df":
    df_to_display = order_payments_df
elif selected_dataset == "order_reviews_df":
    df_to_display = order_reviews_df

if not df_to_display.empty:
    st.write(f"### Cabeçalho de {selected_dataset}")
    st.dataframe(df_to_display.head())
    st.write(f"### Formato de {selected_dataset}")
    st.write(df_to_display.shape)
else:
    st.warning("O DataFrame selecionado está vazio ou não pôde ser carregado.")




## Visualizações Básicas

### Distribuição do Status do Pedido
if not orders_df.empty:
    fig1, ax1 = plt.subplots()
    orders_df['order_status'].value_counts().plot(kind='bar', ax=ax1)
    ax1.set_title('Distribuição do Status do Pedido')
    ax1.set_xlabel('Status do Pedido')
    ax1.set_ylabel('Número de Pedidos')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig1)
else:
    st.info("O DataFrame de Pedidos está vazio, não é possível exibir a distribuição do status do pedido.")

### Top 10 Categorias de Produtos (Traduzidas)
if not order_items_df.empty and not products_df.empty and not product_category_name_translation_df.empty:
    # Mescla os dataframes necessários para obter as categorias de produtos traduzidas
    merged_products = pd.merge(products_df, product_category_name_translation_df,
                               left_on='product_category_name',
                               right_on='product_category_name',
                               how='left')
    merged_order_items = pd.merge(order_items_df, merged_products,
                                  on='product_id',
                                  how='left')

    top_categories = merged_order_items['product_category_name_english'].value_counts().head(10)

    fig2, ax2 = plt.subplots()
    top_categories.plot(kind='barh', ax=ax2)
    ax2.set_title('Top 10 Categorias de Produtos')
    ax2.set_xlabel('Número de Itens Vendidos')
    ax2.set_ylabel('Categoria do Produto (Inglês)')
    plt.tight_layout()
    st.pyplot(fig2)
else:
    st.info("Os DataFrames de Produtos, Itens de Pedido ou Tradução de Categoria de Produto estão vazios, não é possível exibir as principais categorias.")

### Distribuição do Tipo de Pagamento
if not order_payments_df.empty:
    fig3, ax3 = plt.subplots()
    order_payments_df['payment_type'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax3)
    ax3.set_title('Distribuição do Tipo de Pagamento')
    ax3.set_ylabel('') # Oculta o rótulo do eixo y para o gráfico de pizza
    st.pyplot(fig3)
else:
    st.info("O DataFrame de Pagamentos de Pedido está vazio, não é possível exibir a distribuição do tipo de pagamento.")

st.sidebar.header("Sobre")
st.sidebar.info(
    "Este aplicativo demonstra como usar o **`kagglehub`** para baixar um dataset, "
    "o **`pandas`** para carregar e manipular dados, e o **`streamlit`** com **`matplotlib`** "
    "para criar visualizações interativas."
)