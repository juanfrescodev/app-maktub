# Proyecto de Análisis de Datos con Python - Dataset "Advertising Budget and Sales"

## 1. Título del Proyecto
# Analisis de ventas y marketing con publicidad en distintos medios

## 2. Objetivo del análisis
# Analizar cómo impacta la inversión publicitaria en distintos medios (TV, radio y diarios)
#sobre las ventas, mediante limpieza de datos, segmentación y visualización de resultados.

#3 importar librerias
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#Cargar el dataset
def cargar_datos(ruta_csv):
    df = pd.read_csv(ruta_csv)
    return df


#4 limpiar datos
def preprocesar_datos(df):
# eliminar espacios en blanco en los nombres de las columnas
  df.columns = df.columns.str.strip()
  df = df.drop(columns=["Unnamed: 0"])
  return df

#5 agrupar datos
def agrupar(df):
  #crear columna para cada tipo de publicidad y especificar cuanto presupuesto se uso en esa categoria
  df["Categoria TV"] = pd.cut(df["TV Ad Budget ($)"], bins=[0, 100, 200, df["TV Ad Budget ($)"].max()],
                              labels=["Bajo", "Medio", "Alto"])
  df["Categoria radio"] = pd.cut(df["Radio Ad Budget ($)"], bins=[0, 15, 30, df["Radio Ad Budget ($)"].max()],
                              labels=["Bajo", "Medio", "Alto"])
  df["Categoria diario"] = pd.cut(df["Newspaper Ad Budget ($)"], bins=[0, 30, 60, df["Newspaper Ad Budget ($)"].max()],
                              labels=["Bajo", "Medio", "Alto"])
  #5.1 analisis de datos

  # 5.3DataFrames agrupados para graficar:
  df_tv_agrupado = df.groupby("Categoria TV")["Sales ($)"].mean().reset_index()
  df_radio_agrupado = df.groupby("Categoria radio")["Sales ($)"].mean().reset_index()
  df_diario_agrupado = df.groupby("Categoria diario")["Sales ($)"].mean().reset_index()

  #5.4 definir si una campaña fue exitosa
  df["ventas_exitosas"] = df["Sales ($)"] > 10
  #5.5 dataframes agrupados para graficar
  df_tv_exitosas = df.groupby("Categoria TV")["ventas_exitosas"].mean().reset_index()
  df_radio_exitosas = df.groupby("Categoria radio")["ventas_exitosas"].mean().reset_index()
  df_diario_exitosas = df.groupby("Categoria diario")["ventas_exitosas"].mean().reset_index()
  return df, df_tv_agrupado, df_tv_exitosas, df_radio_agrupado, df_radio_exitosas, df_diario_agrupado, df_diario_exitosas


## 6. Visualización de datos

def graficar_ventas(df_tv_agrupado, df_tv_exitosas,
                    df_radio_agrupado,
                     df_diario_agrupado,
                    df, guardar=False):

  # Gráfico de barras: ventas por presupuesto TV
  plt.figure(figsize=(8, 5))
  sns.barplot(x="Categoria TV", y="Sales ($)", data=df_tv_agrupado, palette="viridis")
  plt.title("ventas por cantidad de presupuesto aplicado en TV")
  plt.xlabel("cantidad de presupuesto")
  plt.ylabel("promedio de ventas")
  plt.xticks(rotation=45)
  plt.tight_layout()
  if guardar:
        plt.savefig("ventas_por_presupuesto_tv.png")
  plt.show()

  # Gráfico de barras: ventas por presupuesto radio
  plt.figure(figsize=(8, 5))
  sns.barplot(x="Categoria radio", y="Sales ($)", data=df_radio_agrupado, palette="viridis")
  plt.title("ventas por cantidad de presupuesto aplicado en radio")
  plt.xlabel("cantidad de presupuesto")
  plt.ylabel("promedio de ventas")
  plt.xticks(rotation=45)
  plt.tight_layout()
  if guardar:
        plt.savefig("ventas_por_presupuesto_radio.png")
  plt.show()

    # Gráfico de barras: ventas por presupuesto diario
  plt.figure(figsize=(8, 5))
  sns.barplot(x="Categoria diario", y="Sales ($)", data=df_diario_agrupado, palette="viridis")
  plt.title("ventas por cantidad de presupuesto aplicado en diarios")
  plt.xlabel("cantidad de presupuesto")
  plt.ylabel("promedio de ventas")
  plt.xticks(rotation=45)
  plt.tight_layout()
  if guardar:
        plt.savefig("ventas_por_presupuesto_diario.png")
  plt.show()

    # Gráfico de dispersion: ventas por presupuesto en tv
  plt.figure(figsize=(7, 5))
  sns.scatterplot(data=df, x="TV Ad Budget ($)", y="Sales ($)", hue="Categoria TV", palette="Set2")
  plt.title("Relación entre presupuesto en TV y ventas")
  plt.xlabel("Presupuesto en TV ($)")
  plt.ylabel("Ventas ($)")
  if guardar:
    plt.savefig("dispersion_por_presupuesto_tv.png")
  plt.show()

      # Gráfico de dispersion: ventas por presupuesto en radio
  plt.figure(figsize=(7, 5))
  sns.scatterplot(data=df, x="Radio Ad Budget ($)", y="Sales ($)", hue="Categoria radio", palette="Set3")
  plt.title("Relación entre presupuesto en radio y ventas")
  plt.xlabel("Presupuesto en radio ($)")
  plt.ylabel("Ventas ($)")
  if guardar:
    plt.savefig("dispersion_por_presupuesto_radio.png")
  plt.show()

      # Gráfico de dispersion: ventas por presupuesto en diarios
  plt.figure(figsize=(7, 5))
  sns.scatterplot(data=df, x="Newspaper Ad Budget ($)", y="Sales ($)", hue="Categoria diario", palette="Set1")
  plt.title("Relación entre presupuesto en diarios y ventas")
  plt.xlabel("Presupuesto en diarios ($)")
  plt.ylabel("Ventas ($)")
  if guardar:
    plt.savefig("dispersion_por_presupuesto_diarios.png")
  plt.show()

  # Heatmap de correlación
  plt.figure(figsize=(8, 6))
  numeric_df = df.select_dtypes(include=['number'])
  sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
  plt.title("Mapa de calor de correlación entre variables")
  if guardar:
    plt.savefig("mapa_de_calor.png")
  plt.show()

  #cantidad de ventas exitosas segun presupuesto en TV
  sns.boxplot(x='ventas_exitosas', y='TV Ad Budget ($)', data=df, palette='Set3')
  plt.title('Inversión en TV según éxito de la venta')
  plt.xlabel('¿Venta Exitosa?')
  plt.ylabel('TV Ad Budget ($)')
  if guardar:
    plt.savefig("ventas_exitosas_tv.png")
  plt.show()

  #cantidad de ventas exitosas segun presupuesto en radio
  sns.boxplot(x='ventas_exitosas', y='Radio Ad Budget ($)', data=df, palette='Set3')
  plt.title('Inversión en radio según éxito de la venta')
  plt.xlabel('¿Venta Exitosa?')
  plt.ylabel('Radio Ad Budget ($)')
  if guardar:
    plt.savefig("ventas_exitosas_radio.png")
  plt.show()

    #cantidad de ventas exitosas segun presupuesto en diarios
  sns.boxplot(x='ventas_exitosas', y='Newspaper Ad Budget ($)', data=df, palette='Set3')
  plt.title('Inversión en diarios según éxito de la venta')
  plt.xlabel('¿Venta Exitosa?')
  plt.ylabel('Newspaper Ad Budget ($)')
  if guardar:
    plt.savefig("ventas_exitosas_diarios.png")
  plt.show()
 
  #cantidad de ventas exitosas segun segmento de inversion en TV
  sns.barplot(x="Categoria TV", y='ventas_exitosas', data=df_tv_exitosas, palette='viridis')
  plt.title('% de Ventas Exitosas por Segmento de Inversión en TV')
  plt.ylabel('% Ventas Exitosas')
  plt.xticks(rotation=45)
  if guardar:
    plt.savefig("exitosas_inversion_tv.png")
  plt.show()
  #cantidad de ventas exitosas segun segmento de inversion en radio
  sns.barplot(x="Categoria radio", y='ventas_exitosas', data=df_radio_exitosas, palette='viridis')
  plt.title('% de Ventas Exitosas por Segmento de Inversión en Radio')
  plt.ylabel('% Ventas Exitosas')
  plt.xticks(rotation=45)
  if guardar:
    plt.savefig("exitosas_inversion_radio.png")
  plt.show()
  #cantidad de ventas exitosas segun segmento de inversion en diarios
  sns.barplot(x="Categoria diario", y='ventas_exitosas', data=df_diario_exitosas, palette='viridis')
  plt.title('% de Ventas Exitosas por Segmento de Inversión en Diarios')
  plt.ylabel('% Ventas Exitosas')
  plt.xticks(rotation=45)
  if guardar:
    plt.savefig("exitosas_inversion_diarios.png")
  plt.show()


# 7 llamada al flujo completo
# ---- FLUJO PRINCIPAL ----
if __name__ == "__main__":
  df = cargar_datos("Advertising Budget and Sales.csv")
  df = preprocesar_datos(df)
  df, df_tv_agrupado, df_tv_exitosas, df_radio_agrupado, df_radio_exitosas, df_diario_agrupado, df_diario_exitosas = agrupar(df)
  guardar = input("¿Desea guardar las gráficas? (si/no): ").lower() == "si"

graficar_ventas(df_tv_agrupado, df_tv_exitosas,
                    df_radio_agrupado,
                    df_diario_agrupado,
                    df, guardar=False)

def generar_comentarios(df_tv_agrupado, df_tv_exitosas,
                        df_radio_agrupado, df_radio_exitosas,
                        df_diario_agrupado, df_diario_exitosas,
                        df):

    ventas_totales = df["Sales ($)"].sum()
    presupuesto_promedio_tv = df["TV Ad Budget ($)"].mean()
    presupuesto_promedio_radio = df["Radio Ad Budget ($)"].mean()
    presupuesto_promedio_diario = df["Newspaper Ad Budget ($)"].mean()
    presupuesto_promedio_total = (presupuesto_promedio_tv + presupuesto_promedio_radio + presupuesto_promedio_diario) / 3
    promedio_tv = round(presupuesto_promedio_tv,2)
    promedio_radio = round(presupuesto_promedio_radio,2)
    promedio_diario = round(presupuesto_promedio_diario,2)
    promedio_total = round(presupuesto_promedio_total,2)

    # Crear el texto HTML
    comentarios = f"""
    <h3> Este dataset simula el comportamiento de campañas de marketing en una empresa de ventas en línea.</h3>
    <ul>
    <li>Las ventas totales son: {ventas_totales}.</li>
    <li>El presupuesto promedio gastado en tv es: {promedio_tv}.</li>
    <li>El presupuesto promedio gastado en radio es: {promedio_radio}.</li>
    <li>El presupuesto promedio gastado en diarios es: {promedio_diario}.</li>
    <li>El presupuesto promedio gastado en total es: {promedio_total}.</li>
    </ul>
    """
    if df_tv_exitosas["ventas_exitosas"].max() > 2:
      comentarios += "<li>Las campañas de TV con alto presupuesto tienen un alto porcentaje de éxito.</li>"

    if df_radio_exitosas["ventas_exitosas"].max() > 2:
      comentarios += "<li>Las campañas de radio con alto presupuesto tienen un alto porcentaje de éxito.</li>"

    if df_diario_exitosas["ventas_exitosas"].max() > 2:
      comentarios += "<li>Las campañas de diarios con alto presupuesto tienen un alto porcentaje de éxito.</li>"

    return comentarios

import base64
from io import BytesIO

conclusiones_html = """
<h2>Conclusiones</h2>
<ul>
  <li>Las campañas con mayor presupuesto no siempre generaron más ventas.</li>
  <li>La TV mostró una relación más fuerte entre presupuesto y ventas.</li>
  <li>El análisis sugiere que una mejor distribución del presupuesto puede mejorar el ROI.</li>
  <li>La combinación de canales y una planificación basada en datos puede optimizar resultados futuros.</li>
</ul>
"""

def guardar_dashboard_html(df_tv_agrupado, df_tv_exitosas,
                          df_radio_agrupado, df_radio_exitosas,
                          df_diario_agrupado, df_diario_exitosas,
                          df, comentarios, nombre_archivo="dashboard.html"):

    # Crear imágenes de los gráficos y guardarlas como base64
    def fig_to_base64(fig):
        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        return base64.b64encode(buf.read()).decode("utf-8")

    # Crear y capturar cada gráfico
    figs = []

    # Gráfico de barras: Ventas por presupuesto en TV:
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    sns.barplot(x="Categoria TV", y="Sales ($)", data=df_tv_agrupado, palette="viridis", ax=ax1)
    ax1.set_title("Ventas por cantidad de presupuesto aplicado a tv:")
    ax1.set_xlabel("Cantidad de presupuesto")
    ax1.set_ylabel("Promedio de ventas")
    ax1.tick_params(axis='x', rotation=45)
    figs.append(fig_to_base64(fig1))
    plt.close(fig1)

    # Gráfico de barras: Ventas por presupuesto en radio
    fig2, ax2 = plt.subplots(figsize=(7, 5))
    sns.barplot(x="Categoria radio", y="Sales ($)", data=df_radio_agrupado, palette="crest", ax=ax2)
    ax2.set_title("Ventas por cantidad de presupuesto aplicado a radio:")
    ax2.set_xlabel("Presupuesto")
    ax2.set_ylabel("Promedio de ventas")
    figs.append(fig_to_base64(fig2))
    plt.close(fig2)

    # Gráfico de barras: ventas por presupuesto diarios
    fig3, ax3 = plt.subplots(figsize=(7, 5))
    sns.barplot(x="Categoria diario", y="Sales ($)", data=df_diario_agrupado, palette="mako", ax=ax3)
    ax3.set_title("Ventas por cantidad de presupuesto aplicado a diarios:")
    ax3.set_xlabel("Presupuesto")
    ax3.set_ylabel("Promedio de ventas")
    ax3.tick_params(axis='x', rotation=45)
    figs.append(fig_to_base64(fig3))
    plt.close(fig3)

    #Grafico de dispersion: ventas por presupuesto en TV
    fig4, ax4 = plt.subplots(figsize=(7, 5))
    sns.scatterplot(data=df, x="TV Ad Budget ($)", y="Sales ($)", hue="Categoria TV", palette="Set2", ax=ax4)
    plt.title("Relación entre presupuesto en TV y ventas:")
    plt.xlabel("Presupuesto en TV ($)")
    plt.ylabel("Ventas ($)")
    figs.append(fig_to_base64(fig4))
    plt.close(fig4)

    #grafico de dispersion: ventas por presupuesto en radio
    fig5, ax5 = plt.subplots(figsize=(7, 5))
    sns.scatterplot(data=df, x="Radio Ad Budget ($)", y="Sales ($)", hue="Categoria radio", palette="Set3", ax=ax5)
    plt.title("Relación entre presupuesto en radio y ventas:")
    plt.xlabel("Presupuesto en radio ($)")
    plt.ylabel("Ventas ($)")
    figs.append(fig_to_base64(fig5))
    plt.close(fig5)

    #grafico de dispersion: ventas por presupuesto en diarios
    fig6, ax6 = plt.subplots(figsize=(7, 5))
    sns.scatterplot(data=df, x="Newspaper Ad Budget ($)", y="Sales ($)", hue="Categoria diario", palette="Set1", ax=ax6)
    plt.title("Relación entre presupuesto en diarios y ventas:")
    plt.xlabel("Presupuesto en diarios ($)")
    plt.ylabel("Ventas ($)")
    figs.append(fig_to_base64(fig6))
    plt.close(fig6)

    #cantidad de ventas exitosas segun presupuesto en TV
    sns.boxplot(x='ventas_exitosas', y='TV Ad Budget ($)', data=df, palette='Set3')
    plt.title('Inversión en TV según éxito de la venta:')
    plt.xlabel('¿Venta Exitosa?')
    plt.ylabel('TV Ad Budget ($)')
    plt.show()

    #heatmap de correlacion
    fig7, ax7 = plt.subplots(figsize=(8, 6))
    plt.figure(figsize=(8, 6))
    numeric_df = df.select_dtypes(include=['number'])
    sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax7)
    plt.title("Mapa de calor de correlación entre variables:")
    figs.append(fig_to_base64(fig7))
    plt.close(fig7)

    #cantidad de ventas exitosas segun el presupuesto en TV
    fig8, ax8 = plt.subplots(figsize=(7, 5))
    sns.boxplot(x='ventas_exitosas', y='TV Ad Budget ($)', data=df, palette='Set3', ax=ax8)
    plt.title('Inversión en TV según éxito de la venta:')
    plt.xlabel('¿Venta Exitosa?')
    plt.ylabel('TV Ad Budget ($)')
    figs.append(fig_to_base64(fig8))
    plt.close(fig8)

    #cantidad de ventas exitosas segun el presupuesto en radio
    fig9, ax9 = plt.subplots(figsize=(7, 5))
    sns.boxplot(x='ventas_exitosas', y='Radio Ad Budget ($)', data=df, palette='Set3', ax=ax9)
    plt.title('Inversión en radio según éxito de la venta:')
    plt.xlabel('¿Venta Exitosa?')
    plt.ylabel('Radio Ad Budget ($)')
    figs.append(fig_to_base64(fig9))
    plt.close(fig9)

    #cantidad de ventas exitosas segun el presupuesto en diarios
    fig10, ax10 = plt.subplots(figsize=(7, 5))
    sns.boxplot(x='ventas_exitosas', y='Newspaper Ad Budget ($)', data=df, palette='Set3', ax=ax10)
    plt.title('Inversión en diarios según éxito de la venta:')
    plt.xlabel('¿Venta Exitosa?')
    plt.ylabel('Newspaper Ad Budget ($)')
    figs.append(fig_to_base64(fig10))


    #cantidad de ventas exitosas segun segmento de inversion TV
    fig11, ax11 = plt.subplots(figsize=(7, 5))
    sns.barplot(x="Categoria TV", y='ventas_exitosas', data=df_tv_exitosas, palette='viridis', ax=ax11)
    plt.title('% de Ventas Exitosas por Segmento de Inversión en TV:')
    plt.ylabel('% Ventas Exitosas')
    plt.xticks(rotation=45)
    figs.append(fig_to_base64(fig11))

    #cantidad de ventas exitosas segun segmento de inversion TV
    fig12, ax12 = plt.subplots(figsize=(7, 5))
    sns.barplot(x="Categoria radio", y='ventas_exitosas', data=df_radio_exitosas, palette='viridis', ax=ax12)
    plt.title('% de Ventas Exitosas por Segmento de Inversión en Radio:')
    plt.ylabel('% Ventas Exitosas')
    plt.xticks(rotation=45)
    figs.append(fig_to_base64(fig12))

    #cantidad de ventas exitosas segun segmento de inversion diaris
    fig13, ax13 = plt.subplots(figsize=(7, 5))
    sns.barplot(x="Categoria diario", y='ventas_exitosas', data=df_diario_exitosas, palette='viridis', ax=ax13)
    plt.title('% de Ventas Exitosas por Segmento de Inversión en Diarios:')
    plt.ylabel('% Ventas Exitosas')
    plt.xticks(rotation=45)
    figs.append(fig_to_base64(fig13))

    # Crear HTML final
    html = f"""
    <html>
    <head>
        <title>Ventas y publicidades</title>
    </head>
    <body>
        <h1>Dashboard de Ventas en relación al marketing</h1>
        {comentarios}
        <h2>Gráficos</h2>
        
        <h3>Ventas por presupuesto en TV:</h3>
        <img src="data:image/png;base64,{figs[0]}" />
        <h3>Ventas por presupuesto en radio: </h3>
        <img src="data:image/png;base64,{figs[1]}" />
        <h3>Ventas por presupuesto en diarios</h3>
        <img src="data:image/png;base64,{figs[2]}" />
        <h3>Gráfico de dispersión: ventas por presupuesto en TV:</h3>
        <img src="data:image/png;base64,{figs[3]}" />
        <h3>Gráfico de dispersión: ventas por presupuesto en radio:</h3>
        <img src="data:image/png;base64,{figs[4]}" />
        <h3>Gráfico de dispersión: ventas por presupuesto en diarios:</h3>
        <img src="data:image/png;base64,{figs[5]}" />
        <h3>Heatmap de correlacion entre variables:</h3>
        <img src="data:image/png;base64,{figs[6]}" />
        <h3>Cantidad de ventas exitosas segun presupuesto en TV</h3>
        <img src="data:image/png;base64,{figs[7]}" />
        <h3>Cantidad de ventas exitosas segun presupuesto en radio</h3>
        <img src="data:image/png;base64,{figs[8]}" />
        <h3>Cantidad de ventas exitosas segun presupuesto en diarios</h3>
        <img src="data:image/png;base64,{figs[9]}" />
        <h3>Cantidad de ventas exitosas segun segmento de inversión TV</h3>
        <img src="data:image/png;base64,{figs[10]}" />
        <h3>Cantidad de ventas exitosas segun segmento de inversión radio</h3>
        <img src="data:image/png;base64,{figs[11]}" />
        <h3>Cantidad de ventas exitosas segun segmento de inversión diarios</h3>
        <img src="data:image/png;base64,{figs[12]}" />

        {conclusiones_html}

    </body>
    </html>
    """

    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Dashboard guardado como {nombre_archivo}")

comentarios = generar_comentarios(df_tv_agrupado, df_tv_exitosas,
                                  df_radio_agrupado, df_radio_exitosas,
                                  df_diario_agrupado, df_diario_exitosas,
                                  df)
guardar_dashboard_html(df_tv_agrupado, df_tv_exitosas,
                                  df_radio_agrupado, df_radio_exitosas,
                                  df_diario_agrupado, df_diario_exitosas,
                                  df, comentarios)

