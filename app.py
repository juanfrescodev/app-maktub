import streamlit as st
import os
import pandas as pd
import plotly.express as px
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime


# Autenticación con Google Sheets
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
credentials = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
client = gspread.authorize(credentials)

# Abrir la hoja de cálculo
spreadsheet = client.open("Alumnas_maktub")

# Obtener las hojas de trabajo
hoja_alumnas = spreadsheet.worksheet("Alumnas")
hoja_alquileres = spreadsheet.worksheet("Alquileres")
hoja_historial = spreadsheet.worksheet('Historial')

# Cargar datos de alumnas
def cargar_alumnas():
    data = hoja_alumnas.get_all_records()
    return pd.DataFrame(data)

# Guardar datos de alumnas con validación segura
def guardar_alumnas(df):
    df_safe = df.fillna('').astype(str)
    hoja_alumnas.clear()
    hoja_alumnas.update([df_safe.columns.values.tolist()] + df_safe.values.tolist())

# Cargar datos de alquileres
def cargar_alquileres():
    data = hoja_alquileres.get_all_records()
    return pd.DataFrame(data)

# Guardar datos de alquileres
def guardar_alquileres(df):
    hoja_alquileres.clear()
    hoja_alquileres.update([df.columns.values.tolist()] + df.values.tolist())

# Inicializar datos
df = cargar_alumnas()
df['Cuota'] = pd.to_numeric(df['Cuota'], errors='coerce')
df_alquileres = cargar_alquileres()
alquileres = dict(zip(df_alquileres['Lugar'], df_alquileres['Alquiler']))

def registrar_pago_historial(nombre_alumna, grupo, cuota_pagada):
    # Intentar cargar la hoja 'Historial'
    try:
        historial_values = hoja_historial.get_all_values()
        if len(historial_values) > 1:
            historial_df = pd.DataFrame(historial_values[1:], columns=historial_values[0])
        else:
            # Si no hay datos, crear DataFrame vacío con las columnas deseadas
            historial_df = pd.DataFrame(columns=['Nombre', 'Grupo', 'Fecha de pago', 'Cuota pagada'])
    except Exception as e:
        st.error(f"Error al leer la hoja 'Historial': {e}")
        return

    # Generar nuevo registro
    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    nuevo_registro = pd.DataFrame([{
        'Nombre': nombre_alumna,
        'Grupo': grupo,
        'Fecha de pago': fecha_hora,
        'Cuota pagada': cuota_pagada
    }])

    # Concatenar el nuevo registro al DataFrame existente
    historial_df = pd.concat([historial_df, nuevo_registro], ignore_index=True)

    # Actualizar la hoja 'Historial'
    try:
        hoja_historial.update([historial_df.columns.values.tolist()] + historial_df.values.tolist())
    except Exception as e:
        st.error(f"Error al actualizar la hoja 'Historial': {e}")

# Función para modificar el estado de pago y actualizar fecha
def modificar_estado_pago(df, nombre_alumna, nuevo_estado, cuota_pagada=None):
    index = df[df['Nombre'] == nombre_alumna].index
    if not index.empty:
        df.at[index[0], 'Pago'] = nuevo_estado
        if nuevo_estado == 'TRUE':
            df.at[index[0], 'Fecha de pago'] = datetime.now().strftime('%Y-%m-%d')
            df.at[index[0], 'Cuota'] = cuota_pagada
        else:
            df.at[index[0], 'Fecha de pago'] = None
            df.at[index[0], 'Cuota'] = 0
        guardar_alumnas(df)
        return df
    else:
        st.error('Alumna no encontrada.')
        return df

# Lógica de renovación de pagos
def renovar_pagos(df):
    mes_actual = datetime.now().strftime('%Y-%m')
    df['Historial Pagos'] = df.apply(lambda row: f"{row['Historial Pagos']} | {row['Cuota']} ({mes_actual})" if row['Cuota'] > 0 else row['Historial Pagos'], axis=1)
    df['Cuota'] = 0
    df['Pago'] = 'FALSE'
    df['Fecha de pago'] = None
    guardar_alumnas(df)
    return df

# Verificar si es inicio de mes para realizar renovación
if datetime.now().day == 1:
    df = renovar_pagos(df)
    st.success('Renovación de pagos realizada para el mes actual.')

# Menú de la aplicación
menu = st.sidebar.radio(
    'Menú principal',
    ['Inicio', 'Resumen general', 'Listado de alumnas', 'Consultar alumna', 'Cantidad por grupo', 
     'Alumnas que pagaron', 'Alumnas que no pagaron', 'Agregar nueva alumna', 'Modificar estado de pago',
     'Eliminar alumna', 'Suma total de pagos', 'Total pagado por grupo', 'Gráficos', 'Valor de alquileres', 'Modificar alquileres']
)

# Inicio
if menu == 'Inicio':
    st.write('Gestión de alumnas y cuotas, escuela Maktub')

# Resumen general
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

# Mostrar historial de pagos por alumna
elif menu == 'Consultar alumna':
    if df.empty:
        st.info('No hay alumnas cargadas.')
    else:
        seleccion = st.selectbox('Seleccionar alumna para consultar:', df['Nombre'].unique())
        
        # Filtramos la fila completa de la alumna
        datos_alumna = df[df['Nombre'] == seleccion]

        # Mostramos todos los datos actuales
        st.write('📋 Datos actuales de la alumna:')
        st.dataframe(datos_alumna)

        # Ahora vamos a buscar el historial en la hoja 'Historial'
        try:
            # Buscar registros de la alumna en la hoja Historial
            historial_values = hoja_historial.get_all_values()
            historial_df = pd.DataFrame(historial_values[1:], columns=historial_values[0])

            # Filtramos por el nombre de la alumna
            historial_alumna = historial_df[historial_df['Nombre'] == seleccion]

            if not historial_alumna.empty:
                st.write('📜 Historial de pagos:')
                for _, row in historial_alumna.iterrows():
                    # Mostramos cada registro del historial
                    st.write(f"💸 {row['Cuota pagada']} | Fecha: {row['Fecha de pago']}")
            else:
                st.info('Esta alumna no tiene historial de pagos registrado.')
        except Exception as e:
            st.error(f"Error al cargar el historial de pagos: {e}")

# Cantidad por grupo
elif menu == 'Cantidad por grupo':
    st.write('Cantidad de alumnas por grupo:')
    st.write(df['Grupo'].value_counts())

# Alumnas que pagaron
elif menu == 'Alumnas que pagaron':
    st.write('Alumnas que pagaron:')
    st.write(df[df['Pago'] == 'TRUE'][['Nombre', 'Grupo']])

# Alumnas que no pagaron
elif menu == 'Alumnas que no pagaron':
    st.write('Alumnas que NO pagaron:')
    st.write(df[df['Pago'] == 'FALSE'][['Nombre', 'Grupo']])

#agregar nueva alumna
elif menu == 'Agregar nueva alumna':
    st.write('Agregar nueva alumna:')
    nombre = st.text_input('Nombre')
    grupo = st.text_input('Grupo')
    cuota = st.number_input('Cuota pagada (dejar en 0 si no pagó)', min_value=0)
    if st.button('Agregar'):
        nueva_fila = {
            'Nombre': nombre,
            'Grupo': grupo,
            'Cuota': cuota if cuota > 0 else '',  # 👈 Ahora usamos string vacío en lugar de None
            'Pago': 'TRUE' if cuota > 0 else 'FALSE'
        }
        df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
        guardar_alumnas(df)
        st.success(f'Alumna {nombre} agregada.')

#modificar estado de pago
if menu == 'Modificar estado de pago':
    st.write('Modificar estado de pago:')
    if df.empty:
        st.info('No hay alumnas cargadas.')
    else:
        alumna_seleccionada = st.selectbox('Seleccionar alumna:', df['Nombre'].unique())
        estado_pago = st.radio('Nuevo estado de pago:', ['TRUE', 'FALSE'])
        cuota_pagada = None
        if estado_pago == 'TRUE':
            cuota_pagada = st.number_input('Ingrese el valor de la cuota pagada:', min_value=0)

        if st.button('Actualizar Estado'):
            if estado_pago == 'TRUE' and (cuota_pagada is None or cuota_pagada == 0):
                st.error('Debe ingresar el valor de la cuota pagada.')
            else:
                df = modificar_estado_pago(df, alumna_seleccionada, estado_pago, cuota_pagada)
                guardar_alumnas(df)

                # 🔥 REGISTRAR EN HOJA HISTORIAL (solo si es TRUE y cuota_pagada)
                grupo_alumna = df.loc[df['Nombre'] == alumna_seleccionada, 'Grupo'].values[0]
                registrar_pago_historial(alumna_seleccionada, grupo_alumna, cuota_pagada)
                
                st.success('Estado, historial y registro externo actualizados correctamente.')


# Eliminar alumna
elif menu == 'Eliminar alumna':
    st.write('Eliminar alumna:')
    seleccion = st.selectbox('Seleccionar alumna para eliminar', df['Nombre'])
    if st.button('Eliminar'):
        df = df[df['Nombre'] != seleccion]
        guardar_alumnas(df)
        st.success(f'Alumna {seleccion} eliminada.')

# Suma total de pagos
elif menu == 'Suma total de pagos':
    suma_pagos = df['Cuota'].sum()
    st.write(f"Suma total de pagos realizados: ${suma_pagos:,.0f}")

# Total pagado por grupo
elif menu == 'Total pagado por grupo':
    st.write('Total recaudado por grupo:')
    st.write(df.groupby('Grupo')['Cuota'].sum().sort_values(ascending=False))

# Gráficos
elif menu == 'Gráficos':

    st.write('Gráficos interactivos:')


    st.plotly_chart(px.bar(df.groupby('Grupo')['Cuota'].sum().reset_index(), x='Grupo', y='Cuota', title='Recaudación por Grupo'))
    st.plotly_chart(px.pie(df, names='Grupo', values='Cuota', title='Distribución de pagos por grupo'))

    # Gráfico 2: Pagaron vs No pagaron
    st.write("📊 Porcentaje de alumnas que pagaron vs no pagaron")
    pagaron = df['Cuota'].notna().sum()
    no_pagaron = df['Cuota'].isna().sum()
    datos_pago = pd.DataFrame({
        'Estado': ['Pagaron', 'No pagaron'],
        'Cantidad': [pagaron, no_pagaron]
    })
    fig2 = px.pie(datos_pago, names='Estado', values='Cantidad', color='Estado',
                title='Distribución de pagos')
    fig2.update_traces(textinfo='percent+label')
    st.plotly_chart(fig2)
    
    # Cantidad de alumnas por grupo
    cantidad_por_grupo = df['Grupo'].value_counts().reset_index()
    cantidad_por_grupo.columns = ['Grupo', 'Cantidad']
    fig_cant = px.bar(cantidad_por_grupo, x='Grupo', y='Cantidad', title='Cantidad de Alumnas por Grupo', text_auto=True)
    st.plotly_chart(fig_cant)

# Valor de alquileres y ganancia
elif menu == 'Valor de alquileres':
    st.write('Valores de alquileres y ganancia:')
    for lugar, valor in alquileres.items():
        st.write(f"{lugar}: ${valor:,.0f}")
    alquiler_total = sum(alquileres.values())
    ganancia = df['Cuota'].sum() - alquiler_total
    st.write(f"Total alquiler: ${alquiler_total:,.0f}")
    st.write(f"Ganancia neta: ${ganancia:,.0f}")

# Modificar alquileres
elif menu == 'Modificar alquileres':
    st.write('Modificar valores de alquiler:')
    for lugar in alquileres.keys():
        nuevo_valor = st.number_input(f'{lugar}', value=alquileres[lugar], step=1000)
        alquileres[lugar] = nuevo_valor
    if st.button('Guardar alquileres'):
        # Actualizamos los valores de alquileres en el dataframe
        df_alquileres_actualizado = pd.DataFrame({
            'Lugar': alquileres.keys(),
            'Alquiler': alquileres.values()
        })
        guardar_alquileres(df_alquileres_actualizado)  # Guardamos la nueva tabla de alquileres en Google Sheets
        st.success('Alquileres actualizados correctamente.')

# Footer con información de contacto o logo
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
