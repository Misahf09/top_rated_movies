import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuración de la página
st.set_page_config(page_title="Análisis de Películas", page_icon="🎬", layout="wide")

# Título de la aplicación
st.title("Análisis de Películas Mejor Calificadas")

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

# Crear la figura con subplots
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Agregar la gráfica de línea para el promedio de votos
fig.add_trace(
    go.Scatter(x=avg_votes_by_year['year'], y=avg_votes_by_year['vote_average'], name="Promedio de votos"),
    secondary_y=False,
)

# Agregar la gráfica de barras para la cantidad de películas
fig.add_trace(
    go.Bar(x=movies_count_by_year['year'], y=movies_count_by_year['count'], name="Cantidad de películas"),
    secondary_y=True,
)

# Configurar los ejes
fig.update_layout(
    title_text="Promedio de votos y cantidad de películas por año",
    xaxis_title="Año",
)

fig.update_yaxes(title_text="Promedio de votos", secondary_y=False)
fig.update_yaxes(title_text="Cantidad de películas", secondary_y=True)

# Mostrar la gráfica en Streamlit
st.plotly_chart(fig, use_container_width=True)

# Mostrar los datos en una tabla
st.subheader("Datos")
st.dataframe(df)