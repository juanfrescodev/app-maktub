import streamlit as st
import os
import pandas as pd
import plotly.express as px

# Rutas
base_dir = os.path.dirname(__file__)
alumnas_file = os.path.join(base_dir, 'alumnas_procesadas.csv')
alquileres_file = os.path.join(base_dir, 'alquileres.csv')

# Cargar alumnas
if os.path.exists(alumnas_file):
    df = pd.read_csv(alumnas_file)
else:
    df = pd.DataFrame(columns=['Nombre', 'Grupo', 'Cuota'])

# Cargar o crear alquileres
if os.path.exists(alquileres_file):
    alquileres = pd.read_csv(alquileres_file, index_col='Lugar')['Alquiler'].to_dict()
else:
    alquileres = {'Mitre': 99000, 'Alma Latina': 160000, 'Campichuelo': 92000}

# Menú
menu = st.sidebar.selectbox(
    'Menú principal',
    [
        'Inicio', 'Resumen general', 'Cantidad por grupo', 'Alumnas que pagaron',
        'Alumnas que no pagaron', 'Agregar nueva alumna', 'Modificar estado de pago',
        'Eliminar alumna', 'Suma total de pagos', 'Total pagado por grupo',
        'Gráficos', 'Valor de alquileres', 'Modificar alquileres'
    ]
)

# Inicio
if menu == 'Inicio':
    st.write('Hola mi amorcito esta es tu app ❤️❤️❤️')

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

# Cantidad por grupo
elif menu == 'Cantidad por grupo':
    st.write('Cantidad de alumnas por grupo:')
    st.write(df['Grupo'].value_counts())

# Alumnas que pagaron
elif menu == 'Alumnas que pagaron':
    st.write('Alumnas que pagaron:')
    st.write(df[df['Cuota'].notna()][['Nombre', 'Grupo']])

# Alumnas que no pagaron
elif menu == 'Alumnas que no pagaron':
    st.write('Alumnas que NO pagaron:')
    st.write(df[df['Cuota'].isna()][['Nombre', 'Grupo']])

# Agregar nueva alumna
elif menu == 'Agregar nueva alumna':
    st.write('Agregar nueva alumna:')
    nombre = st.text_input('Nombre')
    grupo = st.text_input('Grupo')
    cuota = st.number_input('Cuota pagada (dejar en 0 si no pagó)', min_value=0)
    if st.button('Agregar'):
        nueva_fila = {'Nombre': nombre, 'Grupo': grupo, 'Cuota': cuota if cuota > 0 else None}
        df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
        df.to_csv(alumnas_file, index=False)
        st.success(f'Alumna {nombre} agregada.')

# Modificar estado de pago
elif menu == 'Modificar estado de pago':
    st.write('Modificar estado de pago:')
    seleccion = st.selectbox('Seleccionar alumna', df['Nombre'])
    nuevo_pago = st.number_input('Nuevo valor de cuota (0 para eliminar pago)', min_value=0)
    if st.button('Actualizar'):
        df.loc[df['Nombre'] == seleccion, 'Cuota'] = nuevo_pago if nuevo_pago > 0 else None
        df.to_csv(alumnas_file, index=False)
        st.success('Pago actualizado.')

# Eliminar alumna
elif menu == 'Eliminar alumna':
    st.write('Eliminar alumna:')
    seleccion = st.selectbox('Seleccionar alumna para eliminar', df['Nombre'])
    if st.button('Eliminar'):
        df = df[df['Nombre'] != seleccion]
        df.to_csv(alumnas_file, index=False)
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
        pd.DataFrame({'Lugar': alquileres.keys(), 'Alquiler': alquileres.values()}).to_csv(alquileres_file, index=False)
        st.success('Alquileres actualizados.')
