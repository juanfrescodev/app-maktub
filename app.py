import streamlit as st

st.write("Email de cuenta de servicio:")
st.write(st.secrets["gcp_service_account"]["client_email"])

st.write("Inicio de clave:")
st.write(st.secrets["gcp_service_account"]["private_key"][:50])
