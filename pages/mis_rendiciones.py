import streamlit as st
from utils.formatters import fmt_monto
from models.constants import ESTADO_COLOR, ESTADO_ICON
from pages.detalle_rendicion import render_detalle_rendicion

def render_mis_rendiciones():
    """Render user's rendiciones list"""
    st.title("📋 Mis Rendiciones")

    rends = st.session_state.rendiciones
    todos_estados = ["Todas"] + list(dict.fromkeys(r["estado"] for r in rends.values()))

    col_f, col_b = st.columns([3, 1])
    with col_f:
        filtro = st.selectbox("Filtrar por estado", todos_estados, label_visibility="collapsed")
    with col_b:
        if st.button("➕ Nueva", use_container_width=True):
            st.session_state.vista = "Nueva Rendición"
            st.rerun()

    st.markdown("---")

    lista = [r for r in rends.values() if filtro == "Todas" or r["estado"] == filtro]
    lista = sorted(lista, key=lambda x: x["historial"][-1]["fecha"], reverse=True)

    if not lista:
        st.info("No hay rendiciones con ese estado.")
        return

    for r in lista:
        color = ESTADO_COLOR.get(r["estado"], "#94a3b8")
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 1, 1.5, 1])
            with col1:
                st.markdown(f"**{r['descripcion'][:60]}{'…' if len(r['descripcion']) > 60 else ''}**")
                st.caption(f"🗂 `{r['id']}` · {r['categoria']} · {r['fecha_comprobante']}")
            with col2:
                st.markdown(f"**{fmt_monto(r['monto'])}**")
            with col3:
                st.markdown(
                    f"<div style='margin-top:4px'><span style='background:rgba(255,255,255,.06);"
                    f"border:1px solid {color}55;border-radius:99px;padding:3px 10px;"
                    f"font-size:.8rem;color:{color};font-weight:700;'>"
                    f"{ESTADO_ICON.get(r['estado'], '')} {r['estado']}</span></div>",
                    unsafe_allow_html=True
                )
            with col4:
                if st.button("Ver detalle", key=f"ver_{r['id']}"):
                    st.session_state.selected_id = r["id"]
                    st.rerun()
            st.markdown("<hr style='border:none;border-top:1px solid #1e2433;margin:6px 0;'>", unsafe_allow_html=True)

    # Expanded detail view
    if st.session_state.selected_id and st.session_state.selected_id in rends:
        r = rends[st.session_state.selected_id]
        st.markdown("---")
        render_detalle_rendicion(r, rol="rendidor")
