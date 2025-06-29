import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Título de la app
st.title("Análisis de Actitudes según Variables Socio-Demográficas")

# Subir archivo CSV
archivo = st.file_uploader("Sube tu archivo CSV con los datos de actitudes", type=["csv"])

if archivo:
    try:
        df = pd.read_csv(archivo)
    except UnicodeDecodeError:
        df = pd.read_csv(archivo, encoding="ISO-8859-1")

    # Calcular promedio de actitud
    df['Promedio_Actitud'] = df[[f'R{i}' for i in range(1, 26)]].mean(axis=1)

    # Mapas de etiquetas
    mapas = {
        'Sexo': {1: 'Mujer', 2: 'Hombre'},
        'Escolaridad': {
            1: 'Primaria', 2: 'Secundaria', 3: 'Técnico',
            4: 'Preparatoria', 5: 'Licenciatura', 6: 'Maestría', 7: 'Doctorado'
        },
        'Estado civil': {
            1: 'Soltero', 2: 'Noviazgo', 3: 'Casado', 4: 'Unión libre'
        },
        'Religión': {
            1: 'Católica', 2: 'Cristiana', 3: 'Testigo de Jehová', 4: 'No tengo'
        }
    }

    # Reemplazar valores codificados
    for col, mapa in mapas.items():
        df[col] = df[col].map(mapa)

    # Mostrar primeros datos
    with st.expander("📄 Ver datos cargados"):
        st.dataframe(df.head())

    # Selector de grupo de análisis
    grupo = st.selectbox("Selecciona una variable socio-demográfica para analizar", 
                         ["Sexo", "Escolaridad", "Estado civil", "Religión"])

    # Gráfico de barras
    st.subheader(f"Promedio de actitud por {grupo}")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=df, x=grupo, y="Promedio_Actitud", ax=ax)
    ax.set_ylabel("Promedio de actitud")
    ax.set_xlabel(grupo)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Tabla resumen
    with st.expander("📊 Ver tabla resumen"):
        resumen = df.groupby(grupo)['Promedio_Actitud'].mean().reset_index()
        st.dataframe(resumen)

else:
    st.info("📌 Esperando que subas un archivo CSV con los datos.")
