import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Meu Aplicativo de Análise de Dados")

# 1. Carregar e manipular dados (com Pandas)
# Geralmente, você teria um arquivo de dados aqui.
# Para este exemplo, vamos criar um DataFrame fictício.
data = {'Cidade': ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Salvador'],
        'População': [12396372, 6772775, 2530701, 2928680],
        'Área_km2': [1521, 1200, 331, 693]}
df = pd.DataFrame(data)

st.header("Dados das Cidades")
st.dataframe(df) # Exibe o DataFrame no Streamlit

# 2. Criar um gráfico (com Matplotlib, usando dados do Pandas)
st.header("Gráfico de População por Cidade")

fig, ax = plt.subplots() # Cria uma figura e um eixo para o gráfico
ax.bar(df['Cidade'], df['População']) # Cria um gráfico de barras
ax.set_xlabel("Cidade")
ax.set_ylabel("População")
ax.set_title("População das Principais Cidades Brasileiras")
plt.xticks(rotation=45, ha='right') # Rotaciona os rótulos do eixo X para melhor leitura
plt.tight_layout() # Ajusta o layout para evitar sobreposição

# 3. Exibir o gráfico no Streamlit
st.pyplot(fig) # Exibe a figura Matplotlib no aplicativo Streamlit

st.write("Este é um aplicativo de exemplo usando Streamlit, Pandas e Matplotlib.")