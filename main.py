import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Análisis de Películas", page_icon="🎬", layout="wide")

# Título de la aplicación
st.title("Análisis de Películas Mejor Calificadas ")

# Cargar los datos
@st.cache_data
def load_data():
    return pd.read_csv("https://raw.githubusercontent.com/Misahf09/top_rated_movies/refs/heads/main/Top_Rated_Movies.csv")

df = load_data()

# Preprocesamiento de datos
df['year'] = pd.to_datetime(df['release_date']).dt.year

# Cálculo de estadísticas
avg_votes_by_year = df.groupby('year')['vote_average'].mean().reset_index()
movies_count_by_year = df['year'].value_counts().sort_index().reset_index()
movies_count_by_year.columns = ['year', 'count']

# Crear la figura con dos ejes Y
fig, ax1 = plt.subplots(figsize=(12, 6))

# Gráfica de línea para el promedio de votos
color = 'tab:blue'
ax1.set_xlabel('Año')
ax1.set_ylabel('Promedio de votos', color=color)
ax1.plot(avg_votes_by_year['year'], avg_votes_by_year['vote_average'], color=color)
ax1.tick_params(axis='y', labelcolor=color)

# Crear un segundo eje Y
ax2 = ax1.twinx()

# Gráfica de barras para la cantidad de películas
color = 'tab:orange'
ax2.set_ylabel('Cantidad de películas', color=color)
ax2.bar(movies_count_by_year['year'], movies_count_by_year['count'], alpha=0.3, color=color)
ax2.tick_params(axis='y', labelcolor=color)

# Título de la gráfica
plt.title("Promedio de votos y cantidad de películas por año")

# Ajustar el diseño
fig.tight_layout()

# Mostrar la gráfica en Streamlit
st.pyplot(fig)

# Mostrar los datos en una tabla
st.subheader("Datos")
st.dataframe(df)
