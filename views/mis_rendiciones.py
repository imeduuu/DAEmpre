import streamlit as st
from utils.formatters import fmt_monto
from models.constants import ESTADO_COLOR, ESTADO_ICON
from views.detalle_rendicion import render_detalle_rendicion

def render_mis_rendiciones():
    """Render user's rendiciones list in premium card interface"""
    st.markdown("""
        <div style="margin-bottom:20px;">
            <h1 style="margin:0; font-size:2.2rem; font-weight:800; color:#ffffff;">🗂 Mis Rendiciones de Gastos</h1>
            <p style="margin:5px 0 0 0; color:#7d8fa9; font-size:0.95rem;">Revisa y gestiona el estado y el historial de tus solicitudes de reembolso.</p>
        </div>
    """, unsafe_allow_html=True)

    rends = st.session_state.rendiciones
    todos_estados = ["Todas"] + list(dict.fromkeys(r["estado"] for r in rends.values()))

    # Beautiful filter card panel
    st.markdown("""
        <div style="background:#121826; border:1px solid #1a2236; border-radius:12px; padding:12px 20px; margin-bottom:20px;">
            <div style="font-size:0.8rem; font-weight:700; color:#7d8fa9; text-transform:uppercase; margin-bottom:5px;">Filtro rápido</div>
        </div>
    """, unsafe_allow_html=True)
    
    col_f, col_spacer, col_b = st.columns([3, 1.5, 1.5])
    with col_f:
        filtro = st.selectbox("Filtrar por estado", todos_estados, label_visibility="collapsed")
    with col_b:
        if st.button("➕ Registrar Gasto", use_container_width=True, type="primary"):
            st.session_state.vista = "Nueva Rendición"
            st.session_state.selected_id = None
            st.rerun()

    st.markdown("<hr style='border:none;border-top:1px solid #1a2236;margin:15px 0;'>", unsafe_allow_html=True)

    lista = [r for r in rends.values() if filtro == "Todas" or r["estado"] == filtro]
    lista = sorted(lista, key=lambda x: x["historial"][-1]["fecha"], reverse=True)

    if not lista:
        st.info("ℹ️ No se encontraron solicitudes registradas con ese filtro de estado.")
        return

    # Render with premium cards
    for r in lista:
        color = ESTADO_COLOR.get(r["estado"], "#94a3b8")
        icon = ESTADO_ICON.get(r["estado"], "")
        
        st.markdown(f"""
            <div class="rendicion-card">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                    <div>
                        <div style="font-weight: 700; color: #ffffff; font-size: 1.05rem;">{r['descripcion'][:70] + '...' if len(r['descripcion']) > 70 else r['descripcion']}</div>
                        <div style="font-size: 0.8rem; color: #7d8fa9; margin-top: 4px;">
                            🗂 <b>{r['id']}</b> · Categoría: {r['categoria']} · Fecha Comprobante: {r['fecha_comprobante']}
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
        
        col_spacer_r, col_btn_r = st.columns([5, 1])
        with col_btn_r:
            if st.button("Administrar / Ver", key=f"ver_{r['id']}", use_container_width=True):
                st.session_state.selected_id = r["id"]
                st.rerun()

    # Expanded detail view styled beautifully inside a highlighted zone
    if st.session_state.selected_id and st.session_state.selected_id in rends:
        r = rends[st.session_state.selected_id]
        st.markdown("<hr style='border:none;border-top:1px solid #1a2236;margin:30px 0;'>", unsafe_allow_html=True)
        st.markdown("""
            <div style="border-left: 4px solid #facc15; padding-left: 15px; margin-bottom: 15px;">
                <h3 style="margin:0; font-size:1.3rem; font-weight:800; color:#ffffff;">🔍 Vista Detallada de Solicitud</h3>
            </div>
        """, unsafe_allow_html=True)
        render_detalle_rendicion(r, rol="rendidor")
