import streamlit as st
from utils.formatters import fmt_monto
from models.constants import ESTADO_COLOR, ESTADO_ICON
from pages.detalle_rendicion import render_detalle_rendicion

def render_vista_rol(rol: str, titulo: str, descripcion: str, estados_visibles: list[str]):
    """Render premium role-based workflow queue"""
    st.markdown(f"""
        <div style="margin-bottom:20px;">
            <h1 style="margin:0; font-size:2.2rem; font-weight:800; color:#ffffff;">{titulo}</h1>
            <p style="margin:5px 0 0 0; color:#7d8fa9; font-size:0.95rem;">{descripcion}</p>
        </div>
    """, unsafe_allow_html=True)

    rends = st.session_state.rendiciones
    lista = [r for r in rends.values() if r["estado"] in estados_visibles]
    lista = sorted(lista, key=lambda x: x["historial"][-1]["fecha"], reverse=True)

    if not lista:
        st.markdown(f"""
            <div class="alert-success" style="padding: 20px; border-radius: 12px; margin-top:10px;">
                🎉 <b>¡Excelente trabajo!</b> No tienes rendiciones de gasto pendientes de acción bajo tu rol actual.<br>
                <span style="font-size:0.8rem;opacity:0.8;">Estados que requieren tu validación: {', '.join(estados_visibles)}</span>
            </div>
        """, unsafe_allow_html=True)
        return

    # Elegant task counter badge
    st.markdown(f"""
        <div style="display:inline-flex; align-items:center; gap:8px; background:rgba(96,165,250,0.08); border:1px solid rgba(96,165,250,0.2); border-radius:30px; padding:6px 16px; margin-bottom:20px;">
            <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#60a5fa; animation: pulse 1.5s infinite;"></span>
            <span style="font-size:0.82rem; font-weight:600; color:#60a5fa;">Tienes {len(lista)} solicitud(es) esperando tu revisión</span>
        </div>
    """, unsafe_allow_html=True)

    # Style list with premium cards
    for r in lista:
        color = ESTADO_COLOR.get(r["estado"], "#94a3b8")
        icon = ESTADO_ICON.get(r["estado"], "")
        
        # Check if amount is extremely high to display caution tag
        monto_warning_html = ""
        if r["monto"] > 500000:
            monto_warning_html = f"""
                <span style="background:rgba(239,68,68,0.1); color:#ef4444; border:1px solid rgba(239,68,68,0.25); border-radius:6px; padding:2px 8px; font-size:0.7rem; font-weight:700; margin-left:10px;">
                    ⚠ BR-05: EXTRAORDINARIO (> $500K)
                </span>
            """

        st.markdown(f"""
            <div class="rendicion-card">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                    <div>
                        <div style="font-weight: 700; color: #ffffff; font-size: 1.05rem;">
                            {r['descripcion'][:65] + '...' if len(r['descripcion']) > 65 else r['descripcion']}
                            {monto_warning_html}
                        </div>
                        <div style="font-size: 0.8rem; color: #7d8fa9; margin-top: 4px;">
                            🗂 <b>{r['id']}</b> · Categoría: {r['categoria']} · Rendidor: {r['rendidor']} · Fecha Envío: {r['fecha_envio']}
                        </div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 15px;">
                        <div style="font-size: 1.15rem; font-weight: 800; color: #ffffff;">{fmt_monto(r['monto'])}</div>
                        <div>
                            <span class="badge" style="background:rgba({int(color[1:3], 16)},{int(color[3:5], 16)},{int(color[5:7], 16)},0.12); color:{color}; border-color:{color}33;">
                                {icon} {r['estado']}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        col_spacer_v, col_btn_v = st.columns([5, 1])
        with col_btn_v:
            if st.button("Gestionar Gasto", key=f"{rol}_gestionar_{r['id']}", use_container_width=True):
                st.session_state.selected_id = r["id"]
                st.rerun()

    # Detail block inside a beautiful layout focus container
    if st.session_state.selected_id and st.session_state.selected_id in rends:
        r = rends[st.session_state.selected_id]
        if r["estado"] in estados_visibles:
            st.markdown("<hr style='border:none;border-top:1px solid #1a2236;margin:30px 0;'>", unsafe_allow_html=True)
            st.markdown("""
                <div style="border-left: 4px solid #60a5fa; padding-left: 15px; margin-bottom: 15px;">
                    <h3 style="margin:0; font-size:1.3rem; font-weight:800; color:#ffffff;">⚙️ Panel de Gestión y Bitácora</h3>
                </div>
            """, unsafe_allow_html=True)
            render_detalle_rendicion(r, rol=rol)
