import streamlit as st
import sqlite3
import pandas as pd


# Función para conectar a la base de datos
def get_data():
    conn = sqlite3.connect('scraped_data.db')
    query = "SELECT * FROM scraped_items"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# Configuración de la página
st.set_page_config(page_title="Web Scraping XYZ", layout="wide")

# Título
st.title("Web Scraping XYZ")

# Cargar datos
data = get_data()

# Mostrar estadísticas generales
st.header("Estadísticas Generales")
st.write(f"total de citas: {len(data)}")
st.write(f"Número de autores únicos: {data['author'].nunique()}")

# Mostrar los datos en una tabla
st.header("Datos Recabados")
st.dataframe(data)

# Gráfico de barras para los autores más citados
st.header("Autores más citados")
author_counts = data['author'].value_counts().head(10)
st.bar_chart(author_counts)

# Nube de palabras de las etiquetas
st.header("Nube de Etiquetas")
from wordcloud import WordCloud
import matplotlib.pyplot as plt


all_tags = ' '.join(data['tags'].str.split(', ').sum())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_tags)


fig, ax = plt.subplots()
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig)


# Búsqueda de citas
st.header("Buscar Citas")
search_term =st.text_input("Introduce un término de búsqueda:")
if search_term:
    filtered_data = data[data['about'].str.contains(search_term, case=False)]
    st.write(f"Resultador encontrados: {len(filtered_data)}")
    st.dataframe(filtered_data)