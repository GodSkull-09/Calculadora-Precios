import streamlit as st

# configuracion de la pagina
st.set_page_config(page_title="Calculadora de Precios Unique", page_icon="💰")

st.title("Calculadora de Precios Unique")
st.markdown("---")

# barra lateral
st.sidebar.header("Configuración de Costos")

tasa_cambio = st.sidebar.number_input("Tasa de Cambio (USD a MXN)", value=18.5, step=0.1)
porcentaje_descuento = st.sidebar.number_input("Descuento Aplicado (Porcentaje %)",
value = 10.0, step=0.1)
costo_envio = st.sidebar.number_input("Costo Fijo de Envío (MXN)", value=80.0, step=10.0)
margen_ganancia = st.sidebar.number_input("Margen de Ganancia (Multiplicador)", value=1.6, step=0.1)


# area principal
st.subheader("Entrada de Producto")
precio_dolares = st.number_input("Precio del producto en Dólares (USD):", min_value=0.0, step=1.0)

# calculos
if precio_dolares > 0:
    monto_descuento_usd = precio_dolares * (porcentaje_descuento / 100)
    precio_usd_con_descuento = precio_dolares - monto_descuento_usd
    precio_pesos = precio_usd_con_descuento * tasa_cambio
    precio_con_envio = precio_pesos + costo_envio
    precio_final = round(precio_con_envio * margen_ganancia, 2)
    
    precio_sin_descuento_total = ((precio_dolares * tasa_cambio) + costo_envio) * margen_ganancia
    ahorro_total_mxn = round(precio_sin_descuento_total - precio_final, 2)
    
    # mostrar resultados
    st.markdown("### Resultado del Cálculo")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Precio Final Sugerido", value=f"${precio_final} MXN")
    with col2:
        ganancia_estimada = round(precio_final - precio_con_envio, 2)
        st.metric(label="Ganancia Bruta", value=f"${ganancia_estimada} MXN", delta=f"{int((margen_ganancia-1)*100)}%")
    with col3:
        st.metric(label="Ahorro Total", value=f"-${ahorro_total_mxn} MXN", delta=f"{porcentaje_descuento}% USD")

    st.info(f"Costo base USD: ${precio_usd_con_descuento:.2f} (Ahorraste ${monto_descuento_usd:.2f} USD)")
else:
    st.write("Ingresa un precio arriba para ver el cálculo.")

#python3 -m venv .venv
#source .venv/bin/activate
#pip install streamlit

#streamlit run app.py

