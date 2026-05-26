import streamlit as st
from utils.formatters import fmt_monto, get_estado_color, get_estado_icon
from models.constants import ESTADO_COLOR, ESTADO_ICON

def render_dashboard():
    """Render premium main dashboard view"""
    st.markdown("""
        <div style="margin-bottom:20px;">
            <h1 style="margin:0; font-size:2.2rem; font-weight:800; color:#ffffff;">📊 Panel de Control y Estadísticas</h1>
            <p style="margin:5px 0 0 0; color:#7d8fa9; font-size:0.95rem;">Resumen de rendimiento de gastos y flujo operacional en tiempo real.</p>
        </div>
    """, unsafe_allow_html=True)

    rends = st.session_state.rendiciones

    # Calculate statistics
    total_pagado = 0
    for r in rends.values():
        e = r["estado"]
        if e in ("Pagado", "Finalizado"):
            total_pagado += r["monto"]

    n_finalizadas = sum(1 for r in rends.values() if r["estado"] in ("Pagado", "Finalizado"))
    n_proceso = sum(1 for r in rends.values() if r["estado"] in ("Pendiente", "Aprobado", "Autorizado", "Pend. Gerencia", "En Cola de Pago", "Borrador"))
    n_rechazadas = sum(1 for r in rends.values() if r["estado"] in ("Rechazado", "Cancelado"))

    # Premium grid cards
    st.markdown(f"""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-bottom: 30px;">
            <div class="stat-card-premium" style="border-left: 4px solid #10b981;">
                <div>
                    <div class="stat-label">Pagadas / Finalizadas</div>
                    <div class="stat-number">{n_finalizadas}</div>
                </div>
                <div style="font-size: 2.2rem; color: #10b981; opacity: 0.9;">✅</div>
            </div>
            <div class="stat-card-premium" style="border-left: 4px solid #3b82f6;">
                <div>
                    <div class="stat-label">En Proceso Activo</div>
                    <div class="stat-number">{n_proceso}</div>
                </div>
                <div style="font-size: 2.2rem; color: #3b82f6; opacity: 0.9;">⌛</div>
            </div>
            <div class="stat-card-premium" style="border-left: 4px solid #ef4444;">
                <div>
                    <div class="stat-label">Rechazadas / Canceladas</div>
                    <div class="stat-number">{n_rechazadas}</div>
                </div>
                <div style="font-size: 2.2rem; color: #ef4444; opacity: 0.9;">❌</div>
            </div>
            <div class="stat-card-premium" style="border-left: 4px solid #fbbf24;">
                <div>
                    <div class="stat-label">Total Reembolsado</div>
                    <div class="stat-number" style="font-size: 1.8rem; margin-top: 5px;">{fmt_monto(total_pagado)}</div>
                </div>
                <div style="font-size: 2.2rem; color: #fbbf24; opacity: 0.9;">💸</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Process Flow Map
    st.markdown("<h3 style='margin-top:0; font-size:1.3rem; font-weight:700;'>🗺️ Mapa de Flujo Operacional</h3>", unsafe_allow_html=True)
    st.markdown("""
        <div class="step-map-container">
            <div class="step-item step-completed">
                <div class="step-dot">1</div>
                <div class="step-label">📝 Borrador</div>
            </div>
            <div style="color:#2e3b5e; font-size:1rem; font-weight:700;">→</div>
            <div class="step-item step-active">
                <div class="step-dot">2</div>
                <div class="step-label">⌛ Pendiente</div>
            </div>
            <div style="color:#2e3b5e; font-size:1rem; font-weight:700;">→</div>
            <div class="step-item">
                <div class="step-dot">3</div>
                <div class="step-label">✔️ Aprobado</div>
            </div>
            <div style="color:#2e3b5e; font-size:1rem; font-weight:700;">→</div>
            <div class="step-item">
                <div class="step-dot">4</div>
                <div class="step-label">🛡️ Autorizado</div>
            </div>
            <div style="color:#2e3b5e; font-size:1rem; font-weight:700;">→</div>
            <div class="step-item">
                <div class="step-dot">5</div>
                <div class="step-label">💸 Pagado</div>
            </div>
            <div style="color:#2e3b5e; font-size:1rem; font-weight:700;">→</div>
            <div class="step-item">
                <div class="step-dot">6</div>
                <div class="step-label">✅ Finalizado</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.caption("ℹ️ Flujo operacional estándar (Camino Ideal). Casos de excepción: Observado (retorna a Borrador) · Pend. Gerencia (Monto > $500.000) · En Cola de Pago (por liquidez)")

    st.markdown("<hr style='border:none;border-top:1px solid #1a2236;margin:25px 0;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0; font-size:1.3rem; font-weight:700;'>📥 Rendiciones de Gasto Recientes</h3>", unsafe_allow_html=True)
    
    # Recent rendiciones in premium cards
    recientes = sorted(rends.values(), key=lambda x: x["historial"][-1]["fecha"], reverse=True)[:5]
    
    for r in recientes:
        color = ESTADO_COLOR.get(r["estado"], "#94a3b8")
        icon = ESTADO_ICON.get(r["estado"], "")
        
        # Display as a premium list item
        with st.container():
            st.markdown(f"""
                <div class="rendicion-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                        <div>
                            <div style="font-weight: 700; color: #ffffff; font-size: 1.05rem;">{r['descripcion'][:65] + '...' if len(r['descripcion']) > 65 else r['descripcion']}</div>
                            <div style="font-size: 0.8rem; color: #7d8fa9; margin-top: 4px;">
                                🗂 <b>{r['id']}</b> · Categoría: {r['categoria']} · Fecha Envío: {r['historial'][-1]['fecha']} · Rendidor: {r['rendidor']}
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
            
            # Action button styled beautifully
            col_spacer, col_btn = st.columns([8.5, 1.5])
            with col_btn:
                if st.button("Ver Detalle", key=f"dash_ver_{r['id']}"):
                    st.session_state.selected_id = r["id"]
                    # Redirect based on active user's roles
                    rol = st.session_state.usuario["rol"]
                    if rol == "rendidor":
                        st.session_state.vista = "Mis Rendiciones"
                    elif rol == "supervisora":
                        st.session_state.vista = "Supervisora"
                    elif rol == "finanzas":
                        st.session_state.vista = "Finanzas"
                    elif rol == "tesorera":
                        st.session_state.vista = "Tesorera"
                    elif rol == "gerencia":
                        st.session_state.vista = "Gerencia"
                    st.rerun()
