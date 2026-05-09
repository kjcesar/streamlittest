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
