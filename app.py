import streamlit as st
import yfinance as yf
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Consulta de Precios y Volumen", layout="centered")
st.title("📊 Consulta de precios históricos y volúmenes")
st.markdown("Consulta el precio de cierre y volumen negociado de cualquier acción, fondo, ETF o criptomoneda.")

# Input del usuario
ticker = st.text_input("🔍 Ingresa el ticker (clave de pizarra):", "AAPL")

# Frecuencia
frecuencia = st.selectbox("🕒 Frecuencia:", ["Diaria", "Semanal", "Mensual"])
intervalos = {"Diaria": "1d", "Semanal": "1wk", "Mensual": "1mo"}

# Plazo
plazo = st.selectbox("📅 Plazo:", ["1 día", "1 mes", "3 meses", "6 meses", "12 meses", "5 años"])
plazos = {"1 día": "1d", "1 mes": "1mo", "3 meses": "3mo", "6 meses": "6mo", "12 meses": "1y", "5 años": "5y"}

# Botón para obtener datos
if st.button("🔽 Obtener datos"):
    try:
        data = yf.Ticker(ticker).history(period=plazos[plazo], interval=intervalos[frecuencia])
        if data.empty:
            st.warning("⚠️ No se encontraron datos para los criterios seleccionados.")
        else:
            precios_volumen = data[['Close', 'Volume']].rename(columns={
                'Close': 'Precio de Cierre',
                'Volume': 'Volumen'
            })

            st.success(f"✅ Datos obtenidos para {ticker}")
            st.subheader("📈 Precio de Cierre")
            st.line_chart(precios_volumen['Precio de Cierre'])

            st.subheader("📊 Volumen Negociado")
            st.bar_chart(precios_volumen['Volumen'])

            # Preparar Excel para descarga
            precios_volumen.index = precios_volumen.index.tz_localize(None)
            excel_file = f"{ticker}_{intervalos[frecuencia]}_{plazos[plazo]}.xlsx"
            precios_volumen.to_excel(excel_file)

            with open(excel_file, "rb") as f:
                st.download_button(
                    "📥 Descargar Excel con precios y volumen",
                    f,
                    file_name=excel_file,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    except Exception as e:
        st.error(f"❌ Ocurrió un error: {e}")

