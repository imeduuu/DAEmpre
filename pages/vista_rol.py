import streamlit as st
from utils.formatters import fmt_monto
from models.constants import ESTADO_COLOR, ESTADO_ICON
from pages.detalle_rendicion import render_detalle_rendicion

def render_vista_rol(rol: str, titulo: str, descripcion: str, estados_visibles: list[str]):
    """Render role-based view"""
    st.title(titulo)
    st.caption(descripcion)
    st.markdown("---")

    rends = st.session_state.rendiciones
    lista = [r for r in rends.values() if r["estado"] in estados_visibles]
    lista = sorted(lista, key=lambda x: x["historial"][-1]["fecha"], reverse=True)

    if not lista:
        st.info(f"No hay rendiciones pendientes de acción en este rol.")
        st.caption(f"Estados que requieren tu acción: {', '.join(estados_visibles)}")
        return

    st.caption(f"🔔 {len(lista)} rendición(es) requieren tu acción.")

    for r in lista:
        color = ESTADO_COLOR.get(r["estado"], "#94a3b8")
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 1.2, 1.5, 1])
            with col1:
                st.markdown(f"**{r['descripcion'][:55]}{'…' if len(r['descripcion']) > 55 else ''}**")
                st.caption(f"`{r['id']}` · {r['categoria']} · {r['rendidor']}")
            with col2:
                st.markdown(f"**{fmt_monto(r['monto'])}**")
                if r["monto"] > 500000:
                    st.caption("⚠ > $500.000")
            with col3:
                st.markdown(
                    f"<div style='margin-top:4px'><span style='border:1px solid {color}55;border-radius:99px;"
                    f"padding:3px 10px;font-size:.8rem;color:{color};font-weight:700;'>"
                    f"{ESTADO_ICON.get(r['estado'], '')} {r['estado']}</span></div>",
                    unsafe_allow_html=True
                )
            with col4:
                if st.button("Gestionar", key=f"{rol}_gestionar_{r['id']}"):
                    st.session_state.selected_id = r["id"]
                    st.rerun()
            st.markdown("<hr style='border:none;border-top:1px solid #1e2433;margin:4px 0;'>", unsafe_allow_html=True)

    # Expanded detail view
    if st.session_state.selected_id and st.session_state.selected_id in rends:
        r = rends[st.session_state.selected_id]
        if r["estado"] in estados_visibles:
            st.markdown("---")
            render_detalle_rendicion(r, rol=rol)
