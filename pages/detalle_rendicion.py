import streamlit as st
from models.types import Rendicion
from utils.formatters import fmt_monto, get_estado_color
from models.constants import ESTADO_COLOR, ESTADO_ICON
from ui.components import render_timeline_item
from pages.acciones import render_acciones

def render_detalle_rendicion(r: Rendicion, rol: str = "rendidor"):
    """Render detailed view of a rendicion"""
    color = ESTADO_COLOR.get(r["estado"], "#94a3b8")
    st.markdown(f"### 📄 Detalle · `{r['id']}`")

    col1, col2, col3 = st.columns(3)
    col1.metric("Monto", fmt_monto(r["monto"]))
    col2.metric("Categoría", r["categoria"])
    col3.markdown(
        f"**Estado**<br><span style='color:{color};font-size:1.1rem;font-weight:700;'>"
        f"{ESTADO_ICON.get(r['estado'], '')} {r['estado']}</span>",
        unsafe_allow_html=True
    )

    st.markdown(f"**Descripción:** {r['descripcion']}")
    st.caption(f"📅 Fecha comprobante: {r['fecha_comprobante']} · 📎 Archivo: {r['archivo']} · 👤 Rendidor: {r['rendidor']}")

    if r["observaciones"]:
        for obs in r["observaciones"]:
            st.markdown(f"<div class='alert-warning'>🔍 <b>Observación:</b> {obs}</div>", unsafe_allow_html=True)

    # Actions based on role and estado
    st.markdown("---")
    render_acciones(r, rol)

    # Historial timeline
    st.markdown("**📅 Historial del proceso**")
    for h in r["historial"]:
        render_timeline_item(h["estado"], h["fecha"], h["nota"], h["actor"])

    if st.button("✕ Cerrar detalle", key=f"cerrar_{r['id']}"):
        st.session_state.selected_id = None
        st.rerun()
