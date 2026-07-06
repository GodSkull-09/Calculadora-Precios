import streamlit as st
import json
import os
import base64

# ---------------------------------------------------------------------------
# Rutas y configuracion de la pagina
# ---------------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRESETS_FILE = os.path.join(BASE_DIR, "presets.json")
LOGO_PATH = os.path.join(BASE_DIR, "assets", "logo.jpg")

st.set_page_config(
    page_title="UQ GYM · Calculadora de Precios",
    page_icon=LOGO_PATH if os.path.exists(LOGO_PATH) else "🏷️",
    layout="centered",
    initial_sidebar_state="expanded",
)


@st.cache_data(show_spinner=False)
def _logo_uri():
    """Devuelve el logo como data-URI para incrustarlo con estilos propios."""
    if not os.path.exists(LOGO_PATH):
        return None
    with open(LOGO_PATH, "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()


# ---------------------------------------------------------------------------
# Estilos — tema oscuro premium UQ GYM
# ---------------------------------------------------------------------------

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

:root{
  --uq-panel:#0E0E10; --uq-panel-2:#141417;
  --uq-line:rgba(255,255,255,.12); --uq-line-soft:rgba(255,255,255,.06);
  --uq-text:#ECECEE; --uq-muted:#8C8C92; --uq-white:#FFFFFF;
}

/* fondo con un halo sutil detras del logo */
.stApp{ background:radial-gradient(1100px 540px at 50% -8%, #1A1A20 0%, #050506 48%, #000 100%); }
[data-testid="stAppViewContainer"], .stMarkdown, .block-container{ font-family:'Inter',sans-serif; }
.block-container{ max-width:840px; padding-top:1.4rem; padding-bottom:4rem; }

/* limpiar chrome de streamlit (sin tocar el control de la barra lateral) */
#MainMenu, footer, [data-testid="stToolbar"]{ visibility:hidden; height:0; }
[data-testid="stHeader"]{ background:transparent !important; }

/* boton para ABRIR la barra lateral: fijo arriba-izquierda, visible y con contraste */
[data-testid="stExpandSidebarButton"]{
  position:fixed !important; top:12px !important; left:14px !important; z-index:1000 !important;
  display:inline-flex !important; visibility:visible !important; opacity:1 !important;
  color:#fff !important; background:rgba(255,255,255,.10) !important;
  border:1px solid rgba(255,255,255,.34) !important; border-radius:9px !important; padding:5px !important;
}
[data-testid="stExpandSidebarButton"]:hover{ background:rgba(255,255,255,.20) !important; }
[data-testid="stExpandSidebarButton"] svg, [data-testid="stExpandSidebarButton"] *{ color:#fff !important; fill:#fff !important; }
/* boton para cerrar la barra lateral (cuando esta abierta) */
[data-testid="stSidebarCollapseButton"] svg, [data-testid="stSidebarCollapseButton"] *{ color:#fff !important; fill:#fff !important; }

/* ---------- cabecera de marca ---------- */
.uq-header{ text-align:center; padding:6px 0 0; }
.uq-logo{
  width:134px; height:134px; border-radius:50%; object-fit:cover; display:inline-block;
  border:1px solid rgba(255,255,255,.16);
  box-shadow:0 0 0 7px rgba(255,255,255,.018), 0 22px 55px rgba(0,0,0,.75);
}
.uq-logo-fallback{
  display:flex; align-items:center; justify-content:center;
  font-family:'Oswald'; font-weight:700; font-size:54px; color:#fff; background:#101013;
}
.uq-brand{
  font-family:'Oswald',sans-serif; font-weight:700; font-size:30px;
  letter-spacing:.30em; color:var(--uq-white); text-transform:uppercase;
  line-height:1; margin-top:16px; padding-left:.30em;
}
.uq-tagline{
  font-family:'Oswald',sans-serif; font-weight:300; font-size:12px;
  letter-spacing:.44em; color:var(--uq-muted); text-transform:uppercase;
  margin-top:11px; padding-left:.44em;
}
.uq-rule{ height:1px; border:0; margin:22px 0 18px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.20),transparent); }

/* ---------- titulos de seccion ---------- */
.uq-section{
  font-family:'Oswald',sans-serif; font-weight:600; text-transform:uppercase;
  letter-spacing:.20em; font-size:12.5px; color:var(--uq-muted); margin:2px 0 10px;
}

/* ---------- hero: precio final ---------- */
.uq-hero{
  text-align:center; border-radius:18px; padding:26px 20px 22px; margin-top:6px;
  background:linear-gradient(180deg,#17171B 0%,#0A0A0C 100%);
  border:1px solid rgba(255,255,255,.13);
  box-shadow:0 24px 60px rgba(0,0,0,.55), inset 0 1px 0 rgba(255,255,255,.05);
}
.uq-hero-label{ font-family:'Oswald'; letter-spacing:.30em; font-size:11.5px;
  color:var(--uq-muted); text-transform:uppercase; }
.uq-hero-value{ font-family:'Oswald'; font-weight:700; font-size:56px; color:#fff;
  line-height:1.04; margin-top:8px; }
.uq-hero-value span{ font-size:19px; color:var(--uq-muted); font-weight:500;
  margin-left:8px; letter-spacing:.14em; }
.uq-hero-sub{ color:var(--uq-muted); font-size:12.5px; margin-top:12px; letter-spacing:.02em; }

/* ---------- tarjetas secundarias ---------- */
.uq-grid{ display:flex; gap:14px; margin-top:14px; }
.uq-card{ flex:1; border-radius:14px; padding:16px 18px;
  background:var(--uq-panel); border:1px solid var(--uq-line-soft); }
.uq-card-label{ font-family:'Oswald'; text-transform:uppercase; letter-spacing:.16em;
  font-size:10.5px; color:var(--uq-muted); }
.uq-card-value{ font-family:'Oswald'; font-weight:600; font-size:25px; color:#fff; margin-top:5px; }
.uq-card-sub{ font-size:11px; color:var(--uq-muted); margin-top:3px; letter-spacing:.04em; }

/* ---------- desglose ---------- */
.uq-steps{ width:100%; border-collapse:collapse; font-size:13.5px; }
.uq-steps td{ padding:9px 4px; border-bottom:1px solid var(--uq-line-soft); color:var(--uq-text); }
.uq-steps td:first-child{ color:var(--uq-muted); }
.uq-steps td:last-child{ text-align:right; font-family:'Oswald'; letter-spacing:.02em; }
.uq-steps tr:last-child td{ border-bottom:0; color:#fff; }

.uq-empty{ text-align:center; color:var(--uq-muted); padding:40px 0; font-size:14px; }
.uq-foot{ text-align:center; color:#46464c; font-size:10.5px; letter-spacing:.28em;
  text-transform:uppercase; font-family:'Oswald'; margin-top:34px; }

/* ---------- widgets ---------- */
[data-testid="stNumberInput"] input, [data-testid="stTextInput"] input{
  background:#0B0B0D !important; color:#fff !important;
  border:1px solid var(--uq-line) !important; border-radius:10px !important;
}
[data-testid="stNumberInput"] input:focus, [data-testid="stTextInput"] input:focus{
  border-color:rgba(255,255,255,.55) !important; box-shadow:0 0 0 2px rgba(255,255,255,.08) !important;
}
[data-testid="stWidgetLabel"] p{ color:var(--uq-text) !important; font-size:13px !important; }

/* selectbox */
[data-baseweb="select"] > div{
  background:#0B0B0D !important; border:1px solid var(--uq-line) !important; border-radius:10px !important;
}

/* botones */
.stButton button{
  width:100%; background:transparent; color:#fff; border:1px solid rgba(255,255,255,.32);
  font-family:'Oswald',sans-serif; font-weight:600; letter-spacing:.10em; text-transform:uppercase;
  border-radius:10px; padding:.45rem 0; transition:.15s ease;
}
.stButton button:hover{ border-color:#fff; background:rgba(255,255,255,.06); }
.stButton button[kind="primary"]{ background:#fff; color:#000; border-color:#fff; }
.stButton button[kind="primary"]:hover{ background:#E6E6EA; color:#000; }

/* contenedor con borde (entrada) */
[data-testid="stVerticalBlockBorderWrapper"]{ border-radius:16px !important; }

/* sidebar */
[data-testid="stSidebar"]{ background:#070708; border-right:1px solid var(--uq-line-soft); }
[data-testid="stSidebar"] .block-container{ padding-top:1.2rem; }
.uq-side-brand{ font-family:'Oswald'; font-weight:700; letter-spacing:.34em; color:#fff;
  text-transform:uppercase; font-size:17px; padding:2px 0 4px 2px; }
.uq-pill{ display:inline-block; font-family:'Oswald'; font-size:10px; letter-spacing:.14em;
  text-transform:uppercase; color:#0a0a0a; background:#fff; border-radius:999px;
  padding:2px 9px; margin-top:8px; }
.uq-pill.mod{ background:transparent; color:var(--uq-muted); border:1px solid var(--uq-line); }

/* expander */
[data-testid="stExpander"]{ border:1px solid var(--uq-line-soft) !important; border-radius:12px !important;
  background:var(--uq-panel) !important; }
[data-testid="stExpander"] summary{ font-family:'Oswald'; letter-spacing:.06em; }
</style>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Presets
# ---------------------------------------------------------------------------

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

with st.sidebar:
    if os.path.exists(LOGO_PATH):
        st.logo(LOGO_PATH)
    st.markdown('<div class="uq-side-brand">UQ&nbsp;GYM</div>', unsafe_allow_html=True)

    st.markdown('<div class="uq-section">Presets</div>', unsafe_allow_html=True)
    st.selectbox(
        "Marca / preset",
        options=list(st.session_state["presets"].keys()),
        key="selector_preset",
        on_change=aplicar_preset,
        label_visibility="collapsed",
    )

    # indicador de preset activo / modificado
    activo = st.session_state["selector_preset"]
    guardado = st.session_state["presets"].get(activo, {})
    modificado = any(
        abs(float(st.session_state[c]) - float(guardado.get(c, st.session_state[c]))) > 1e-9
        for c in PARAMS
    )
    if modificado:
        st.markdown(f'<span class="uq-pill mod">{activo} · modificado</span>', unsafe_allow_html=True)
    else:
        st.markdown(f'<span class="uq-pill">{activo}</span>', unsafe_allow_html=True)

    with st.expander("💾 Guardar / administrar"):
        st.text_input("Nombre del preset", key="nombre_guardar")
        col_g, col_e = st.columns(2)
        col_g.button("Guardar", type="primary", on_click=guardar_preset_actual)
        col_e.button("Eliminar", on_click=eliminar_preset_actual)
        st.caption("«Guardar» crea uno nuevo o sobrescribe si el nombre ya existe.")

    if "_aviso" in st.session_state:
        tipo, texto = st.session_state.pop("_aviso")
        getattr(st, tipo)(texto)

    st.markdown('<div class="uq-section" style="margin-top:18px;">Configuración de costos</div>', unsafe_allow_html=True)

    porcentaje_descuento = st.number_input(
        "Descuento Aplicado (%)", step=1.0, min_value=0.0, max_value=100.0, key="descuento",
    )
    impuesto = st.number_input(
        "Multiplicador de Impuesto", step=0.001, min_value=1.0, format="%.3f", key="impuesto",
    )
    tasa_cambio = st.number_input(
        "Tasa de Cambio (USD → MXN)", step=0.5, min_value=1.0, key="tasa_cambio",
    )
    costo_envio = st.number_input(
        "Costo Fijo de Envío (MXN)", step=10.0, min_value=0.0, key="costo_envio",
    )
    margen_ganancia = st.number_input(
        "Margen de Ganancia (×)", step=0.05, min_value=1.0, format="%.2f", key="margen_ganancia",
    )


# ---------------------------------------------------------------------------
# Cabecera de marca
# ---------------------------------------------------------------------------

uri = _logo_uri()
logo_html = (
    f'<img class="uq-logo" src="{uri}" alt="UQ GYM"/>'
    if uri else '<div class="uq-logo uq-logo-fallback">UQ</div>'
)
st.markdown(
    '<div class="uq-header">'
    f"{logo_html}"
    '<div class="uq-brand">Unique Gym Shop</div>'
    '<div class="uq-tagline">Calculadora de Precios</div>'
    "</div>"
    '<hr class="uq-rule"/>',
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Entrada de producto
# ---------------------------------------------------------------------------

with st.container(border=True):
    st.markdown('<div class="uq-section">Entrada de producto</div>', unsafe_allow_html=True)
    precio_dolares = st.number_input("Precio del producto (USD)", min_value=0.0, step=1.0)


# ---------------------------------------------------------------------------
# Calculo y resultados
# ---------------------------------------------------------------------------

if precio_dolares > 0:

    # 1. Descuento  -> 2. Impuesto -> 3. MXN -> 4. Envio -> 5. Margen
    monto_descuento_usd = precio_dolares * (porcentaje_descuento / 100)
    precio_con_descuento = precio_dolares - monto_descuento_usd
    precio_con_impuesto = precio_con_descuento * impuesto
    precio_pesos = precio_con_impuesto * tasa_cambio
    precio_con_envio = precio_pesos + costo_envio
    precio_final = round(precio_con_envio * margen_ganancia, 2)

    precio_sin_descuento = round(precio_dolares * impuesto * tasa_cambio * margen_ganancia + costo_envio * margen_ganancia, 2)
    ahorro_total_mxn = round(precio_sin_descuento - precio_final, 2)
    ganancia_estimada = round(precio_final - precio_con_envio, 2)

    # ---- hero: precio final ----
    st.markdown(
        '<div class="uq-hero">'
        '<div class="uq-hero-label">Precio Final Sugerido</div>'
        f'<div class="uq-hero-value">${precio_final:,.2f}<span>MXN</span></div>'
        f'<div class="uq-hero-sub">Costo base ${precio_con_envio:,.2f} &nbsp;·&nbsp; Margen ×{margen_ganancia:.2f} &nbsp;·&nbsp; {activo}</div>'
        "</div>",
        unsafe_allow_html=True,
    )

    # ---- tarjetas secundarias ----
    if porcentaje_descuento > 0:
        ahorro_label, ahorro_value, ahorro_sub = (
            "Ahorro vs sin descuento",
            f"−${ahorro_total_mxn:,.2f}",
            f"Descuento {porcentaje_descuento:g}% en USD",
        )
    else:
        ahorro_label, ahorro_value, ahorro_sub = "Descuento aplicado", "—", "Sin descuento"

    st.markdown(
        '<div class="uq-grid">'
        '<div class="uq-card">'
        '<div class="uq-card-label">Ganancia bruta</div>'
        f'<div class="uq-card-value">${ganancia_estimada:,.2f}</div>'
        f'<div class="uq-card-sub">+{int((margen_ganancia - 1) * 100)}% sobre el costo base</div>'
        "</div>"
        '<div class="uq-card">'
        f'<div class="uq-card-label">{ahorro_label}</div>'
        f'<div class="uq-card-value">{ahorro_value}</div>'
        f'<div class="uq-card-sub">{ahorro_sub}</div>'
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    # ---- desglose paso a paso ----
    with st.expander("Ver desglose paso a paso"):
        st.markdown(
            '<table class="uq-steps">'
            f'<tr><td>1 · Precio original</td><td>${precio_dolares:,.2f} USD</td></tr>'
            f'<tr><td>2 · Descuento ({porcentaje_descuento:g}%)</td><td>−${monto_descuento_usd:,.2f} → ${precio_con_descuento:,.2f} USD</td></tr>'
            f'<tr><td>3 · Impuesto (×{impuesto:.3f})</td><td>${precio_con_impuesto:,.2f} USD</td></tr>'
            f'<tr><td>4 · Conversión (×{tasa_cambio:g} MXN)</td><td>${precio_pesos:,.2f} MXN</td></tr>'
            f'<tr><td>5 · Envío (+${costo_envio:g})</td><td>${precio_con_envio:,.2f} MXN</td></tr>'
            f'<tr><td>6 · Margen (×{margen_ganancia:.2f})</td><td>${precio_final:,.2f} MXN</td></tr>'
            "</table>",
            unsafe_allow_html=True,
        )

else:
    st.markdown('<div class="uq-empty">Ingresa un precio en USD para ver el cálculo.</div>', unsafe_allow_html=True)


st.markdown('<div class="uq-foot">Unique Gym Shop — UQ GYM</div>', unsafe_allow_html=True)
