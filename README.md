# Calculadora de Precios Unique

Calculadora de precios de reventa hecha con [Streamlit](https://streamlit.io/).
Convierte el precio de un producto en USD a un precio final sugerido en MXN
aplicando, en orden:

> descuento → impuesto → tasa de cambio → envío → margen de ganancia

Incluye **presets por marca** (YoungLA, Gymshark, Breathedivinity, Controlled
Insanity, Darc Sport, Dfyne) que precargan esos parámetros, con opción de
**guardar, crear y eliminar** presets propios.

## Requisitos

- Python 3.9 o superior
- Las dependencias de [`requirements.txt`](requirements.txt)

## Instalación y uso

```bash
# 1. crear y activar el entorno virtual
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. instalar dependencias
pip install -r requirements.txt

# 3. ejecutar la app
streamlit run app.py
```

La app se abre en el navegador (por defecto http://localhost:8501).

## Presets

- Elige una marca en el selector de la barra lateral para precargar sus parámetros.
- En **💾 Guardar / administrar presets** puedes guardar los valores actuales
  (sobrescribe si el nombre ya existe, o crea uno nuevo) y eliminar presets.
- Tus presets se guardan en `presets.json`, que es local y **no** se sube al
  repositorio. Los 6 presets por defecto están definidos en `app.py`, así que
  una copia nueva del proyecto siempre arranca con ellos.

## Fórmula

Para cada preset, partiendo del precio en USD:

| Paso | Operación |
|------|-----------|
| 1 | `precio − descuento%`  → X |
| 2 | `X × impuesto` (ej. 1.093) → Y |
| 3 | `Y × tasa de cambio` (ej. 18.0) → Z |
| 4 | `Z + envío` (ej. 80) → A |
| 5 | `A × margen` (ej. 1.70) → **Total final (MXN)** |
