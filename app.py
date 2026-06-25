import streamlit as st
import json
import os

# configuracion de la pagina
st.set_page_config(page_title="Calculadora de Precios Unique", page_icon="🏷️")

# ---------------------------------------------------------------------------
# Presets
# ---------------------------------------------------------------------------

# archivo donde se guardan los presets (junto a app.py)
PRESETS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "presets.json")

# parametros que define cada preset
PARAMS = ["descuento", "impuesto", "tasa_cambio", "costo_envio", "margen_ganancia"]

# presets que vienen por defecto
DEFAULT_PRESETS = {
    "YoungLA":             {"descuento": 15.0, "impuesto": 1.093, "tasa_cambio": 18.0, "costo_envio": 80.0, "margen_ganancia": 1.70},
    "Gymshark":            {"descuento": 10.0, "impuesto": 1.093, "tasa_cambio": 18.0, "costo_envio": 80.0, "margen_ganancia": 1.70},
    "Breathedivinity":     {"descuento": 10.0, "impuesto": 1.093, "tasa_cambio": 18.0, "costo_envio": 80.0, "margen_ganancia": 1.55},
    "Controlled Insanity": {"descuento": 10.0, "impuesto": 1.093, "tasa_cambio": 18.0, "costo_envio": 80.0, "margen_ganancia": 1.70},
    "Darc Sport":          {"descuento": 10.0, "impuesto": 1.093, "tasa_cambio": 18.0, "costo_envio": 80.0, "margen_ganancia": 1.65},
    "Dfyne":               {"descuento": 10.0, "impuesto": 1.093, "tasa_cambio": 18.0, "costo_envio": 80.0, "margen_ganancia": 1.50},
}


def guardar_presets(presets):
    """Escribe los presets al archivo json."""
    try:
        with open(PRESETS_FILE, "w", encoding="utf-8") as f:
            json.dump(presets, f, indent=2, ensure_ascii=False)
    except OSError:
        st.sidebar.error("No se pudieron guardar los presets en disco.")


def _preset_valido(p):
    """Un preset valido es un dict con los 5 parametros, todos numericos."""
    return isinstance(p, dict) and all(
        k in p and isinstance(p[k], (int, float)) and not isinstance(p[k], bool)
        for k in PARAMS
    )


def cargar_presets():
    """Lee los presets del archivo, descartando entradas corruptas. Si el
    archivo no existe o no queda ninguno valido, lo crea con los por defecto."""
    if os.path.exists(PRESETS_FILE):
        try:
            with open(PRESETS_FILE, "r", encoding="utf-8") as f:
                datos = json.load(f)
            if isinstance(datos, dict):
                limpios = {
                    nombre: {k: float(p[k]) for k in PARAMS}
                    for nombre, p in datos.items()
                    if _preset_valido(p)
                }
                if limpios:
                    return limpios
        except (json.JSONDecodeError, OSError, TypeError, ValueError):
            pass
    guardar_presets(DEFAULT_PRESETS)
    return dict(DEFAULT_PRESETS)


# cargar presets una sola vez por sesion
if "presets" not in st.session_state:
    st.session_state["presets"] = cargar_presets()

# inicializar los parametros con el primer preset (solo la primera vez)
if "descuento" not in st.session_state:
    primer_nombre = next(iter(st.session_state["presets"]))
    for clave, valor in st.session_state["presets"][primer_nombre].items():
        st.session_state[clave] = float(valor)
    st.session_state["nombre_guardar"] = primer_nombre


def aplicar_preset():
    """Carga los valores del preset elegido en los parametros (callback del selector)."""
    nombre = st.session_state["selector_preset"]
    preset = st.session_state["presets"].get(nombre)
    if preset:
        for clave in PARAMS:
            st.session_state[clave] = float(preset[clave])
        st.session_state["nombre_guardar"] = nombre


def guardar_preset_actual():
    """Guarda los parametros actuales bajo el nombre escrito (crea nuevo o sobrescribe)."""
    nombre = st.session_state["nombre_guardar"].strip()
    if not nombre:
        st.session_state["_aviso"] = ("warning", "Escribe un nombre para el preset.")
        return
    st.session_state["presets"][nombre] = {clave: float(st.session_state[clave]) for clave in PARAMS}
    guardar_presets(st.session_state["presets"])
    st.session_state["selector_preset"] = nombre  # dejar seleccionado el guardado
    st.session_state["_aviso"] = ("success", f"Preset «{nombre}» guardado.")


def eliminar_preset_actual():
    """Elimina el preset actualmente seleccionado."""
    nombre = st.session_state["selector_preset"]
    if len(st.session_state["presets"]) <= 1:
        st.session_state["_aviso"] = ("warning", "Debe quedar al menos un preset.")
        return
    st.session_state["presets"].pop(nombre, None)
    guardar_presets(st.session_state["presets"])
    nuevo = next(iter(st.session_state["presets"]))
    st.session_state["selector_preset"] = nuevo
    st.session_state["nombre_guardar"] = nuevo
    for clave in PARAMS:
        st.session_state[clave] = float(st.session_state["presets"][nuevo][clave])
    st.session_state["_aviso"] = ("success", f"Preset «{nombre}» eliminado.")


# ---------------------------------------------------------------------------
# Barra lateral: presets + configuracion de costos
# ---------------------------------------------------------------------------

st.sidebar.header("📦 Presets")

st.sidebar.selectbox(
    "Selecciona una marca / preset",
    options=list(st.session_state["presets"].keys()),
    key="selector_preset",
    on_change=aplicar_preset,
)

with st.sidebar.expander("💾 Guardar / administrar presets"):
    st.text_input("Nombre del preset", key="nombre_guardar")
    col_g, col_e = st.columns(2)
    col_g.button("💾 Guardar", on_click=guardar_preset_actual, width="stretch")
    col_e.button("🗑️ Eliminar", on_click=eliminar_preset_actual, width="stretch")
    st.caption("«Guardar» crea un preset nuevo, o sobrescribe si el nombre ya existe.")

# mostrar el aviso de guardado/eliminado si lo hay
if "_aviso" in st.session_state:
    tipo, texto = st.session_state.pop("_aviso")
    getattr(st.sidebar, tipo)(texto)

st.sidebar.markdown("---")
st.sidebar.header("Configuración de Costos")

porcentaje_descuento = st.sidebar.number_input(
    "Descuento Aplicado (%)",
    step=1.0,
    min_value=0.0,
    max_value=100.0,
    key="descuento",
)

impuesto = st.sidebar.number_input(
    "Multiplicador de Impuesto (ej. 1.07, 1.093)",
    step=0.001,
    min_value=1.0,
    format="%.3f",
    key="impuesto",
)

tasa_cambio = st.sidebar.number_input(
    "Tasa de Cambio (USD a MXN)",
    step=0.5,
    min_value=1.0,
    key="tasa_cambio",
)

costo_envio = st.sidebar.number_input(
    "Costo Fijo de Envío (MXN)",
    step=10.0,
    min_value=0.0,
    key="costo_envio",
)

margen_ganancia = st.sidebar.number_input(
    "Margen de Ganancia (Multiplicador)",
    step=0.05,
    min_value=1.0,
    format="%.2f",
    key="margen_ganancia",
)

# ---------------------------------------------------------------------------
# Area principal
# ---------------------------------------------------------------------------

st.title("Calculadora de Precios Unique")

# indicar el preset activo y si fue modificado respecto al guardado
preset_guardado = st.session_state["presets"].get(st.session_state["selector_preset"], {})
modificado = any(
    abs(float(st.session_state[clave]) - float(preset_guardado.get(clave, st.session_state[clave]))) > 1e-9
    for clave in PARAMS
)
st.caption(f"Preset activo: **{st.session_state['selector_preset']}**" + (" — _modificado_ ✏️" if modificado else ""))
st.markdown("----")

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
