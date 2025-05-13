import streamlit as st
import os
import pandas as pd
import plotly.express as px
import gspread
from google.oauth2.service_account import Credentials

# Autenticación con Google Sheets
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
credentials = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
client = gspread.authorize(credentials)

# Abrir la hoja de cálculo
spreadsheet = client.open("Alumnas_maktub")  

# Obtener las hojas de trabajo
hoja_alumnas = spreadsheet.worksheet("Alumnas")
hoja_alquileres = spreadsheet.worksheet("Alquileres")

# Cargar datos de alumnas
def cargar_alumnas():
    data = hoja_alumnas.get_all_records()
    return pd.DataFrame(data)

# Guardar datos de alumnas
def guardar_alumnas(df):
    hoja_alumnas.clear()
    hoja_alumnas.update([df.columns.values.tolist()] + df.values.tolist())

# Cargar datos de alquileres
def cargar_alquileres():
    data = hoja_alquileres.get_all_records()
    return pd.DataFrame(data)

# Guardar datos de alquileres
def guardar_alquileres(df):
    hoja_alquileres.clear()
    hoja_alquileres.update([df.columns.values.tolist()] + df.values.tolist())

# Inicializar datos
df_alumnas = cargar_alumnas()
df_alquileres = cargar_alquileres()



st.write(df_alquileres.columns)
