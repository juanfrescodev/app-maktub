import streamlit as st
import os
import pandas as pd
import plotly.express as px
import gspread
from google.oauth2.service_account import Credentials
import datetime 

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

# Guardar datos de alumnas con validación segura
def guardar_alumnas(df):
    # Convertir todo a string y reemplazar None o NaN por ''
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

# Añadimos columnas para el historial y la fecha del pago
def inicializar_columna_historial(df):
    # Agregar columnas si no existen
    if 'Historial Pagos' not in df.columns:
        df['Historial Pagos'] = ''
    if 'Fecha de pago' not in df.columns:
        df['Fecha de pago'] = None
    return df

# Aplicamos la inicialización si es necesario
df = inicializar_columna_historial(df)

def renovar_pagos(df):
    # Resetea los pagos y almacena el historial
    mes_actual = datetime.datetime.now().strftime('%Y-%m')
    
    # Guardar el historial de pagos
    df['Historial Pagos'] = df.apply(lambda row: f"{row['Historial Pagos']} | {row['Cuota']} ({mes_actual})" if row['Cuota'] > 0 else row['Historial Pagos'], axis=1)
    
    # Resetear las cuotas a 0
    df['Cuota'] = 0
    df['Pago'] = 'FALSE'
    df['Fecha de pago'] = None  # Limpiar la fecha de pago si es necesario
    guardar_alumnas(df)  # Guardar los cambios en la hoja de Google Sheets

    return df

# Verificar si es inicio de mes para realizar renovación
if datetime.datetime.now().day == 1:
    df = renovar_pagos(df)
    st.success('Renovación de pagos realizada para el mes actual.')


# Función para modificar estado de pago y actualizar fecha
def modificar_estado_pago(df, nombre_alumna, nuevo_estado, cuota_pagada=None):
    index = df[df['Nombre'] == nombre_alumna].index
    if not index.empty:
        df.at[index[0], 'Pago'] = nuevo_estado
        if nuevo_estado == 'TRUE':
            df.at[index[0], 'Fecha de pago'] = datetime.datetime.now().strftime('%Y-%m-%d')
            df.at[index[0], 'Cuota'] = cuota_pagada  # Registra la cuota ingresada
        else:
            df.at[index[0], 'Fecha de pago'] = None  # Limpia la fecha si no pagó
            df.at[index[0], 'Cuota'] = 0  # Limpia el valor de cuota si no pagó
        guardar_alumnas(df)
        return df
    else:
        st.error('Alumna no encontrada.')
        return df



# Título de la app con fondo y estilo
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


# Menú
menu = st.sidebar.radio(
    'Menú principal',
    [
        'Inicio', 'Resumen general', 'Listado de alumnas', 'Consultar alumna', 'Cantidad por grupo', 'Alumnas que pagaron',
        'Alumnas que no pagaron', 'Agregar nueva alumna', 'Modificar estado de pago',
        'Eliminar alumna', 'Suma total de pagos', 'Total pagado por grupo',
        'Gráficos', 'Valor de alquileres', 'Modificar alquileres'
    ]
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

        # Mostramos historial si la columna 'Historial Pagos' existe y tiene datos
        if 'Historial Pagos' in datos_alumna.columns:
            historial = datos_alumna['Historial Pagos'].values[0]
            if historial and isinstance(historial, list):
                st.write('📜 Historial de pagos:')
                for item in historial:
                    st.write(f"- {item}")
            else:
                st.info('Esta alumna no tiene historial cargado.')
        else:
            st.warning('La columna Historial Pagos no existe.')


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
elif menu == 'Modificar estado de pago':
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

                if estado_pago == 'TRUE':
                    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
                    historial_actual = df.loc[df['Nombre'] == alumna_seleccionada, 'Historial Pagos'].values[0]
                    if pd.isna(historial_actual) or historial_actual == '':
                        historial_actual = []
                    else:
                        historial_actual = ast.literal_eval(historial_actual)

                    nuevo_registro = f"{fecha_actual}: Pagado - {cuota_pagada}"
                    historial_actual.append(nuevo_registro)

                    df.loc[df['Nombre'] == alumna_seleccionada, 'Historial Pagos'] = str(historial_actual)
                    guardar_alumnas(df)
                    st.success(f'✅ Pago marcado como realizado el {fecha_actual} por ${cuota_pagada}')
                else:
                    st.info('ℹ️ Estado marcado como no pagado, fecha y cuota limpiadas.')

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
