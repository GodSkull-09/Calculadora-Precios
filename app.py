import streamlit as st

# configuracion de la pagina
st.set_page_config(page_title="Calculadora de Precios Unique", page_icon="🏷️")

st.title("Calculadora de Precios Unique")
st.markdown("----")

# barra lateral
st.sidebar.header("Configuración de Costos")

porcentaje_descuento = st.sidebar.number_input(
    "Descuento Aplicado (%)",
    value=0.0,
    step=1.0,
    min_value=0.0,
    max_value=100.0
)

impuesto = st.sidebar.number_input(
    "Multiplicador de Impuesto (ej. 1.07, 1.074)",
    value=1.07,
    step=0.001,
    min_value=1.0,
    format="%.3f"
)

tasa_cambio = st.sidebar.number_input(
    "Tasa de Cambio (USD a MXN)",
    value=18.0,
    step=0.5,
    min_value=1.0
)

costo_envio = st.sidebar.number_input(
    "Costo Fijo de Envío (MXN)",
    value=80.0,
    step=10.0,
    min_value=0.0
)

margen_ganancia = st.sidebar.number_input(
    "Margen de Ganancia (Multiplicador)",
    value=1.60,
    step=0.05,
    min_value=1.0,
    format="%.2f"
)

# area principal
st.subheader("Entrada de Producto")
precio_dolares = st.number_input("Precio del producto en Dólares (USD):", min_value=0.0, step=1.0)

# calculos
if precio_dolares > 0:

    # 1. Descuento
    monto_descuento_usd = precio_dolares * (porcentaje_descuento / 100)
    precio_con_descuento = precio_dolares - monto_descuento_usd

    # 2. Impuesto
    precio_con_impuesto = precio_con_descuento * impuesto

    # 3. Conversión a MXN
    precio_pesos = precio_con_impuesto * tasa_cambio

    # 4. Envío
    precio_con_envio = precio_pesos + costo_envio

    # 5. Margen de ganancia
    precio_final = round(precio_con_envio * margen_ganancia, 2)

    # Para mostrar el ahorro (precio sin descuento, mismo flujo)
    precio_sin_descuento = round(precio_dolares * impuesto * tasa_cambio * margen_ganancia + costo_envio * margen_ganancia, 2)
    ahorro_total_mxn = round(precio_sin_descuento - precio_final, 2)
    ganancia_estimada = round(precio_final - precio_con_envio, 2)

    # mostrar paso a paso
    st.markdown("### 🔢 Desglose del Cálculo")

    with st.expander("Ver paso a paso"):
        st.write(f"1. **Precio original:** ${precio_dolares:.2f} USD")
        st.write(f"2. **Descuento ({porcentaje_descuento}%):** -${monto_descuento_usd:.2f} USD → ${precio_con_descuento:.2f} USD")
        st.write(f"3. **Impuesto (×{impuesto}):** ${precio_con_impuesto:.2f} USD")
        st.write(f"4. **Conversión (×{tasa_cambio} MXN):** ${precio_pesos:.2f} MXN")
        st.write(f"5. **Envío (+{costo_envio} MXN):** ${precio_con_envio:.2f} MXN")
        st.write(f"6. **Margen de ganancia (×{margen_ganancia}):** ${precio_final:.2f} MXN")

    # resultados principales
    st.markdown("### Resultado del Cálculo")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Precio Final Sugerido", value=f"${precio_final} MXN")
    with col2:
        st.metric(label="Ganancia Bruta", value=f"${ganancia_estimada} MXN", delta=f"{int((margen_ganancia-1)*100)}%")
    with col3:
        if porcentaje_descuento > 0:
            st.metric(label="Ahorro vs Sin Descuento", value=f"-${ahorro_total_mxn} MXN", delta=f"{porcentaje_descuento}% USD")
        else:
            st.metric(label="Descuento Aplicado", value="Sin descuento")

    st.info(f"Costo base MXN antes de ganancia: ${precio_con_envio:.2f} — Ganancia neta estimada: ${ganancia_estimada:.2f} MXN")

else:
    st.write("Ingresa un precio arriba para ver el cálculo.")