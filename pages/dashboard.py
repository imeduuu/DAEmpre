import streamlit as st
from utils.formatters import fmt_monto, get_estado_color, get_estado_icon
from models.constants import ESTADO_COLOR, ESTADO_ICON

def render_dashboard():
    """Render main dashboard view"""
    st.title("📊 Dashboard")
    rends = st.session_state.rendiciones

    # Calculate statistics
    estados_count = {}
    total_pagado = 0
    for r in rends.values():
        e = r["estado"]
        estados_count[e] = estados_count.get(e, 0) + 1
        if e in ("Pagado", "Finalizado"):
            total_pagado += r["monto"]

    # Stat cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        n = sum(1 for r in rends.values() if r["estado"] in ("Pagado", "Finalizado"))
        st.metric("✅ Finalizadas / Pagadas", n)
    with col2:
        n = sum(1 for r in rends.values() if r["estado"] in ("Pendiente", "Aprobado", "Autorizado", "Pend. Gerencia", "En Cola de Pago", "Borrador"))
        st.metric("⏳ En proceso", n)
    with col3:
        n = sum(1 for r in rends.values() if r["estado"] in ("Rechazado", "Cancelado"))
        st.metric("❌ Rechazadas / Canceladas", n)
    with col4:
        st.metric("💰 Total reembolsado", fmt_monto(total_pagado))

    st.markdown("---")
    st.subheader("📌 Flujo principal del proceso")

    # Process flow
    flujo = ["Borrador", "Pendiente", "Aprobado", "Autorizado", "Pagado", "Finalizado"]
    cols = st.columns(len(flujo) * 2 - 1)
    for i, paso in enumerate(flujo):
        with cols[i * 2]:
            color = ESTADO_COLOR.get(paso, "#94a3b8")
            st.markdown(
                f"<div style='background:rgba(255,255,255,.05);border:1px solid {color}44;"
                f"border-radius:8px;padding:8px 6px;text-align:center;font-size:.8rem;"
                f"color:{color};font-weight:700;'>{ESTADO_ICON.get(paso, '')} {paso}</div>",
                unsafe_allow_html=True
            )
        if i < len(flujo) - 1:
            with cols[i * 2 + 1]:
                st.markdown("<div style='text-align:center;color:#4a5568;font-size:1.2rem;padding-top:6px;'>→</div>", unsafe_allow_html=True)

    st.caption("⚠ Excepciones: Observado → Borrador (máx 3 intentos) · Pend. Gerencia (monto > $500.000) · En Cola de Pago (sin liquidez)")

    st.markdown("---")
    st.subheader("📋 Rendiciones recientes")
    
    # Recent rendiciones
    recientes = sorted(rends.values(), key=lambda x: x["historial"][-1]["fecha"], reverse=True)[:5]
    for r in recientes:
        col_a, col_b, col_c, col_d = st.columns([3, 1, 1, 1])
        with col_a:
            st.markdown(f"**{r['descripcion'][:55]}{'…' if len(r['descripcion']) > 55 else ''}**")
            st.caption(f"🗂 {r['id']} · {r['categoria']} · {r['historial'][-1]['fecha']}")
        with col_b:
            st.markdown(f"**{fmt_monto(r['monto'])}**")
        with col_c:
            color = ESTADO_COLOR.get(r["estado"], "#94a3b8")
            st.markdown(f"<span style='color:{color};font-weight:700;font-size:.85rem;'>{ESTADO_ICON.get(r['estado'], '')} {r['estado']}</span>", unsafe_allow_html=True)
        with col_d:
            if st.button("Ver", key=f"dash_ver_{r['id']}"):
                st.session_state.selected_id = r["id"]
                st.session_state.vista = "Mis Rendiciones"
                st.rerun()
        st.markdown("<hr style='border:none;border-top:1px solid #1e2433;margin:4px 0;'>", unsafe_allow_html=True)
