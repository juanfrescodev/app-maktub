import streamlit as st

# Muestra el comienzo de la clave
st.write(st.secrets["gcp_service_account"]["private_key"][:50])
