import streamlit as st

# configuracion de la pagina
st.set_page_config(page_title="Calculadora de Precios Unique", page_icon="💰")

st.title("Calculadora de Precios Unique")
st.markdown("---")

# barra lateral
st.sidebar.header("Configuración de Costos")

tasa_cambio = st.sidebar.number_input("Tasa de Cambio (USD a MXN)", value=18.5, step=0.1)
costo_envio = st.sidebar.number_input("Costo Fijo de Envío (MXN)", value=80.0, step=10.0)
margen_ganancia = st.sidebar.number_input("Margen de Ganancia (Multiplicador)", value=1.6, step=0.1)
porcentaje_descuento = st.sidebar.number_input("Descuento Aplicado (Porcentaje %)",
value = 10.0, step=0.1)

# area principal
st.subheader("Entrada de Producto")
precio_dolares = st.number_input("Precio del producto en Dólares (USD):", min_value=0.0, step=1.0)

# calculos
if precio_dolares > 0:
    precio_pesos = precio_dolares * tasa_cambio
    precio_con_envio = precio_pesos + costo_envio
    precio_base_con_margen = precio_con_envio * margen_ganancia
    
    monto_descuento = precio_base_con_margen * (porcentaje_descuento / 100)
    precio_final = round(precio_base_con_margen - monto_descuento, 2)
    

    # Mmostrar resultados
    st.markdown("### Resultado del Cálculo")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Precio Final Sugerido", value=f"${precio_final} MXN")
    with col2:
        ganancia_estimada = round(precio_final - precio_con_envio, 2)
        st.metric(label="Ganancia Bruta", value=f"${ganancia_estimada} MXN", delta=f"{int((margen_ganancia-1)*100)}%")
    with col3:
        st.metric(label = "Ahorro del Cliente", value=f'-${round(monto_descuento, 2)} MXN', delta =f'{porcentaje_descuento}%')

    st.info(f"Costo base: ${precio_pesos:.2f} | Envío: ${costo_envio} | Sin descuento: ${round(precio_base_con_margen, 2)}")
else:
    st.write("Ingresa un precio arriba para ver el cálculo.")

#python3 -m venv .venv
#source .venv/bin/activate
#pip install streamlit

#streamlit run app.py

