import numpy as np
import pandas as pd
import plotly.express as px
import requests
import streamlit as st

st.set_page_config(
    page_title="Ibanasca - Defensa Planetaria de Dr. Z Academy",
    page_icon="🌍",
    layout="wide",
)


@st.cache_data
def cargar_datos():
    url = "https://ssd-api.jpl.nasa.gov/sbdb_query.api"
    campos = "full_name,H,albedo,diameter,moid,e,a,i,class,neo,pha"
    params = {
        "fields": campos,
        "sb-kind": "a",
        "sb-group": "neo",
    }
    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()  # por si algo falla

    df = pd.DataFrame(r.json()["data"], columns=r.json()["fields"])

    for col in ["H", "albedo", "diameter", "moid", "e", "a", "i"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["nombre"] = df["full_name"].str.strip()
    return df


# st spinner muestra un mensaje mientras espera la descarga

with st.spinner("Descargando catálogo del JPL..."):
    df = cargar_datos()

st.title("Ibanasca - Defensa Planetaria de Dr.Z Academy")
st.caption(f"Catálogo JPL - {len(df):,} asteroides NEA")

## Parte 2

st.sidebar.header("Filtros")

clases = ["Todas"] + sorted(df["class"].dropna().unique().tolist())
clase_sel = st.sidebar.selectbox("Clase orbital", clases)

solo_pha = st.sidebar.checkbox("Solo PHAs")

h_min, h_max = st.sidebar.slider(
    "Rango de magnitud H",
    min_value=float(df["H"].min()),
    max_value=float(df["H"].max()),
    value=(float(df["H"].min()), 25.0),
)

df_filtrado = df.copy()

if clase_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado["class"] == clase_sel]

if solo_pha:
    df_filtrado = df_filtrado[df_filtrado["pha"] == "Y"]

df_filtrado = df_filtrado[(df_filtrado["H"] >= h_min) & (df_filtrado["H"] <= h_max)]

st.sidebar.markdown(f"**{len(df_filtrado):,} asteroides** con estos filtros")


# parte 3
#


tab1, tab2, tab3 = st.tabs(
    [
        "📚 Catálogo",
        "🗺️ Mapas",
        "🪐 Ficha",
    ]
)

with tab1:
    st.write(type(df))
    st.write(type(df_filtrado))
    st.write(type(df_filtrado[columnas]))

    st.subheader("Catálogo de Asteroides NEA")
    columnas = ["nombre", "H", "albedo", "diameter", "moid", "class", "pha"]
    st.dataframe(
        df_filtrado[columnas].rename(
            columns={
                "nombre": "Nombre",
                "H": "Mag. H",
                "albedo": "Albedo",
                "diameter": "Diametro (km)",
                "moid": "MOID (UA)",
                "class": "Clase",
                "pha": "PHA",
            }
        ),
        use_container_width=True,
        height=500,
    )
