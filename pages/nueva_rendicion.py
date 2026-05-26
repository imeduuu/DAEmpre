import streamlit as st
from datetime import date, datetime
import uuid
import os
from utils.formatters import fmt_monto
from services.rendicion_service import add_historial, add_notif, create_rendicion
from models.constants import DESCRIPCION_MIN_CHARS, DIAS_PLAZO_COMPROBANTE, MONTO_UMBRAL_GERENCIA

def render_nueva():
    """Render new rendicion form"""
    st.title("➕ Nueva Rendición de Gasto")
    st.caption("Completa los campos para registrar tu comprobante de gasto.")

    # Get active user from state or default to Tomás Alarcón
    user_name = "Tomás Alarcón"
    if "usuario" in st.session_state and st.session_state.usuario:
        user_name = st.session_state.usuario["nombre"]

    with st.form("form_nueva", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            categoria = st.selectbox("Categoría del gasto *", ["", "Transporte", "Alimentación", "Hospedaje", "Equipamiento", "Otro"])
        with col2:
            monto = st.number_input("Monto (CLP) *", min_value=0, step=100, value=0)

        descripcion = st.text_area(
            "Descripción del gasto * (mínimo 10 caracteres)",
            placeholder="Ej: Almuerzo de trabajo con proveedor durante comisión en Concepción",
            height=90
        )

        fecha_comp = st.date_input(
            "Fecha del comprobante *",
            value=date.today(),
            max_value=date.today()
        )

        archivo = st.file_uploader(
            "Comprobante (foto/PDF) *",
            type=["jpg", "jpeg", "png", "pdf"],
            help="Máximo 10 MB"
        )

        st.markdown("---")

        # Real-time alerts
        if monto > MONTO_UMBRAL_GERENCIA:
            st.warning("⚠ **BR-05:** Montos sobre $500.000 requieren aprobación adicional de Gerencia de Finanzas.")

        dias_diferencia = (date.today() - fecha_comp).days if fecha_comp else 0
        if dias_diferencia > DIAS_PLAZO_COMPROBANTE:
            st.error(f"⚠ **BR-09:** El comprobante tiene {dias_diferencia} días de antigüedad (máximo 30). Requerirá aprobación especial de Gerencia.")

        submitted = st.form_submit_button("Enviar rendición", use_container_width=True, type="primary")

    if submitted:
        errores = []

        # BR-06: descripción mínima
        if len(descripcion.strip()) < DESCRIPCION_MIN_CHARS:
            errores.append(f"**BR-06:** La descripción debe tener al menos {DESCRIPCION_MIN_CHARS} caracteres (tiene {len(descripcion.strip())}).")

        # BR-07: monto > 0
        if monto <= 0:
            errores.append("**BR-07:** El monto debe ser mayor a $0.")

        if not categoria:
            errores.append("Debes seleccionar una categoría.")

        if archivo is None:
            errores.append("Debes adjuntar el comprobante.")

        # BR-09: fecha dentro de plazo
        dias_dif = (date.today() - fecha_comp).days
        fuera_plazo = dias_dif > DIAS_PLAZO_COMPROBANTE

        # Check for duplicates
        for r in st.session_state.rendiciones.values():
            if (r["monto"] == monto and
                r["categoria"] == categoria and
                r["fecha_comprobante"] == str(fecha_comp) and
                r["estado"] not in ("Rechazado", "Cancelado")):
                errores.append(f"**Duplicado detectado:** Ya existe la rendición {r['id']} con el mismo monto, categoría y fecha.")
                break

        if errores:
            for e in errores:
                st.error(e)
        else:
            # Create rendicion ID
            rid = f"TX-{str(uuid.uuid4())[:4].upper()}"
            ts = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            # Save file physically in data/comprobantes
            os.makedirs("data/comprobantes", exist_ok=True)
            safe_filename = f"{rid}_{archivo.name}"
            file_path = os.path.join("data/comprobantes", safe_filename)
            with open(file_path, "wb") as f:
                f.write(archivo.getbuffer())

            nueva = {
                "id": rid,
                "descripcion": descripcion.strip(),
                "categoria": categoria,
                "monto": monto,
                "fecha_comprobante": str(fecha_comp),
                "fecha_envio": ts,
                "estado": "Pendiente",
                "rendidor": user_name,
                "archivo": safe_filename,
                "observaciones": [],
                "historial": [
                    {"estado": "Borrador", "actor": user_name, "fecha": ts, "nota": "Rendición creada y validada localmente y comprobante guardado físicamente."},
                    {"estado": "Pendiente", "actor": "Sistema", "fecha": ts, "nota": "Validaciones OK (BR-06, BR-07). Notificada supervisora Camila Fuentes."},
                ],
                "intentos_correccion": 0,
            }

            if fuera_plazo:
                nueva["estado"] = "Pend. Gerencia"
                nueva["historial"].append({
                    "estado": "Pend. Gerencia",
                    "actor": "Sistema",
                    "fecha": ts,
                    "nota": f"BR-09: Comprobante con {dias_dif} días de antigüedad. Escalado a Gerencia para excepción de plazo."
                })
                add_notif("gerencia", f"{rid}: Comprobante fuera de plazo. Escalado a Gerencia.")

            elif monto > MONTO_UMBRAL_GERENCIA:
                nueva["estado"] = "Pendiente"
                nueva["historial"][1]["nota"] += " BR-05: Monto > $500.000, requerirá aprobación de Gerencia tras Supervisora."
                add_notif("warning", f"{rid}: Monto {fmt_monto(monto)} > $500.000 detectado.")
            else:
                add_notif("pendiente", f"{rid}: Rendición enviada. Esperando aprobación de Camila Fuentes.")

            create_rendicion(rid, nueva)
            st.success(f"Rendición **{rid}** enviada exitosamente. Estado: **{nueva['estado']}**")
            st.info("La supervisora Camila Fuentes ha sido notificada.")
