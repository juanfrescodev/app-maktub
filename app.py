import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json

def conectar_a_google_sheets():
    creds_info = st.secrets["gcp_service_account"]  # YA ES UN DICCIONARIO
    credentials = Credentials.from_service_account_info(creds_info)
    client = gspread.authorize(credentials)
    sheet = client.open("Alumnas_maktub").worksheet("lista")
    return sheet

sheet = conectar_a_google_sheets()

def cargar_datos_desde_sheets():
    # Carga todos los registros desde Google Sheets
    records = sheet.get_all_records()
    df = pd.DataFrame(records)
    return df

df = cargar_datos_desde_sheets()

def actualizar_datos_en_sheets(df):
    # Borra todos los registros en Google Sheets antes de escribir los nuevos
    sheet.clear()

    # Escribe los nuevos datos
    sheet.update([df.columns.values.tolist()] + df.values.tolist())

import streamlit as st
import pandas as pd
import plotly.express as px


# --- Interfaz ---
st.markdown("""
    <style>
        .title {
            color: #ff6347;
            font-size: 40px;
            font-family: 'Arial', sans-serif;
            text-align: center;
            padding: 20px;
            background-color: #f0f8ff;
            border-radius: 10px;
        }
    </style>
    <div class="title">📊 Gestión Escuela de Danzas Maktub</div>
""", unsafe_allow_html=True)

menu = st.sidebar.radio(
    'Menú principal',
    [
        'Inicio', 'Resumen general', 'Listado de alumnas', 'Cantidad por grupo', 'Alumnas que pagaron',
        'Alumnas que no pagaron', 'Agregar nueva alumna', 'Modificar estado de pago',
        'Eliminar alumna', 'Suma total de pagos', 'Total pagado por grupo',
        'Gráficos', 'Valor de alquileres', 'Modificar alquileres'
    ]
)

# --- Secciones ---
if menu == 'Inicio':
    st.write('Hola mi amorcito esta es tu app ❤️❤️❤️')

elif menu == 'Resumen general':
    st.write('Resumen total de alumnas y pagos.')
    total = len(df)
    pagaron = df['Cuota'].notna().sum()
    no_pagaron = total - pagaron
    porcentaje = (pagaron / total) * 100 if total > 0 else 0
    st.write(f"👥 Total de alumnas: {total}")
    st.write(f"💰 Alumnas que pagaron: {pagaron} ({porcentaje:.1f}%)")
    st.write(f"🚫 Alumnas que NO pagaron: {no_pagaron} ({100 - porcentaje:.1f}%)")

elif menu == 'Listado de alumnas':
    st.write(df['Nombre'])

elif menu == 'Cantidad por grupo':
    st.write('Cantidad de alumnas por grupo:')
    st.write(df['Grupo'].value_counts())

elif menu == 'Alumnas que pagaron':
    st.write('Alumnas que pagaron:')
    st.write(df[df['Cuota'].notna()][['Nombre', 'Grupo']])

elif menu == 'Alumnas que no pagaron':
    st.write('Alumnas que NO pagaron:')
    st.write(df[df['Cuota'].isna()][['Nombre', 'Grupo']])

elif menu == 'Agregar nueva alumna':
    st.write('Agregar nueva alumna:')
    nombre = st.text_input('Nombre')
    grupo = st.text_input('Grupo')
    cuota = st.number_input('Cuota pagada (dejar en 0 si no pagó)', min_value=0)
    if st.button('Agregar'):
        nueva_fila = {'Nombre': nombre, 'Grupo': grupo, 'Cuota': cuota if cuota > 0 else None}
        df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
        actualizar_datos_en_sheets(df)  # Guarda los cambios en Google Sheets
        st.success(f'Alumna {nombre} agregada.')
        st.experimental_rerun()

elif menu == 'Modificar estado de pago':
    st.write('Modificar estado de pago:')
    seleccion = st.selectbox('Seleccionar alumna', df['Nombre'])
    nuevo_pago = st.number_input('Nuevo valor de cuota (0 para eliminar pago)', min_value=0)
    if st.button('Actualizar'):
        df.loc[df['Nombre'] == seleccion, 'Cuota'] = nuevo_pago if nuevo_pago > 0 else None
        actualizar_datos_en_sheets(df)  # Guarda los cambios en Google Sheets
        st.success('Pago actualizado.')
        st.experimental_rerun()

elif menu == 'Eliminar alumna':
    st.write('Eliminar alumna:')
    seleccion = st.selectbox('Seleccionar alumna para eliminar', df['Nombre'])
    if st.button('Eliminar'):
        df = df[df['Nombre'] != seleccion]
        actualizar_datos_en_sheets(df)  # Guarda los cambios en Google Sheets
        st.success(f'Alumna {seleccion} eliminada.')
        st.experimental_rerun()

elif menu == 'Suma total de pagos':
    suma_pagos = df['Cuota'].sum()
    st.write(f"Suma total de pagos realizados: ${suma_pagos:,.0f}")

elif menu == 'Total pagado por grupo':
    st.write('Total recaudado por grupo:')
    st.write(df.groupby('Grupo')['Cuota'].sum().sort_values(ascending=False))

elif menu == 'Gráficos':
    st.write('Gráficos interactivos:')
    st.plotly_chart(px.bar(df.groupby('Grupo')['Cuota'].sum().reset_index(), x='Grupo', y='Cuota', title='Recaudación por Grupo'))
    st.plotly_chart(px.pie(df, names='Grupo', values='Cuota', title='Distribución de pagos por grupo'))

    st.write("📊 Porcentaje de alumnas que pagaron vs no pagaron")
    pagaron = df['Cuota'].notna().sum()
    no_pagaron = df['Cuota'].isna().sum()
    datos_pago = pd.DataFrame({'Estado': ['Pagaron', 'No pagaron'], 'Cantidad': [pagaron, no_pagaron]})
    fig2 = px.pie(datos_pago, names='Estado', values='Cantidad', color='Estado', title='Distribución de pagos')
    fig2.update_traces(textinfo='percent+label')
    st.plotly_chart(fig2)

    cantidad_por_grupo = df['Grupo'].value_counts().reset_index()
    cantidad_por_grupo.columns = ['Grupo', 'Cantidad']
    fig_cant = px.bar(cantidad_por_grupo, x='Grupo', y='Cantidad', title='Cantidad de Alumnas por Grupo', text_auto=True)
    st.plotly_chart(fig_cant)

elif menu == 'Valor de alquileres':
    st.write('Valores de alquileres y ganancia:')
    for lugar, valor in alquileres.items():
        st.write(f"{lugar}: ${valor:,.0f}")
    alquiler_total = sum(alquileres.values())
    ganancia = df['Cuota'].sum() - alquiler_total
    st.write(f"Total alquiler: ${alquiler_total:,.0f}")
    st.write(f"Ganancia neta: ${ganancia:,.0f}")

elif menu == 'Modificar alquileres':
    st.write('Modificar valores de alquiler:')
    for lugar in list(alquileres.keys()):
        nuevo_valor = st.number_input(f'{lugar}', value=int(alquileres[lugar]), step=1000)
        alquileres[lugar] = nuevo_valor
    if st.button('Guardar alquileres'):
        pd.DataFrame({'Lugar': alquileres.keys(), 'Alquiler': alquileres.values()}).to_csv(ALQUILERES_FILE, index=False)
        st.success('Alquileres actualizados.')
        st.experimental_rerun()

# --- Footer ---
st.markdown("""
    <style>
        .footer {
            text-align: center;
            padding: 10px;
            font-size: 14px;
            color: #555;
            background-color: #f0f8ff;
        }
    </style>
    <div class="footer">
        <p>Creado por Juan Fresco - Desarrollo de apps, data analitycs</p>
    </div>
""", unsafe_allow_html=True)

