import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Cargar credenciales de Streamlit Secrets
creds_info = st.secrets["gcp_service_account"]

# Crear credenciales usando google-auth directamente
creds = Credentials.from_service_account_info(dict(creds_info))

# Probar conexión a una hoja de prueba
gc = gspread.authorize(creds)

# Si no falla, lista hojas de prueba (CAMBIA por tu URL si querés)
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/154ueaF5pT7lDqk8ECO9I8r_6ZNOhXFWLodYaeZNjP00")
worksheet = sh.get_worksheet(0)
st.write(worksheet.get_all_records())
