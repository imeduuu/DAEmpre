import streamlit as st
from models.constants import ESTADO_COLOR, ESTADO_ICON
from services.database import get_all_usuarios

def render_sidebar():
    """Render main sidebar navigation based on active user role"""
    from services.rendicion_service import unread_count
    
    # Active user
    user = st.session_state.usuario
    if not user:
        return
        
    st.sidebar.markdown(f"## 💼 GastosApp")
    st.sidebar.caption("Intranet · Prototipo Mínimo Viable (PMV)")
    st.sidebar.markdown("---")

    # User Profile Section
    st.sidebar.markdown(
        f"<div style='background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:10px; padding:10px; margin-bottom:15px;'>"
        f"<div style='display:flex; align-items:center; gap:10px;'>"
        f"<span style='font-size:2.2rem;'>{user['avatar']}</span>"
        f"<div>"
        f"<b style='font-size:0.95rem; color:#facc15;'>{user['nombre']}</b><br>"
        f"<span style='font-size:0.75rem; color:#94a3b8; font-weight:500;'>{user['cargo']}</span>"
        f"</div>"
        f"</div>"
        f"</div>",
        unsafe_allow_html=True
    )
    
    # Logout Button
    if st.sidebar.button("🚪 Cerrar Sesión", key="logout_btn", use_container_width=True, type="secondary"):
        st.session_state.usuario = None
        st.session_state.selected_id = None
        st.session_state.vista = "Dashboard"
        st.rerun()
        
    st.sidebar.markdown("---")

    # Dynamic Menu Items based on Role
    rol = user["rol"]
    st.sidebar.markdown(f"**MENÚ ({rol.upper()})**")
    
    # Common Dashboard
    if st.sidebar.button("📊 Dashboard", key="nav_Dashboard", use_container_width=True):
        st.session_state.vista = "Dashboard"
        st.session_state.selected_id = None
        st.rerun()

    # Role specific views
    if rol == "rendidor":
        if st.sidebar.button("➕ Nueva Rendición", key="nav_Nueva", use_container_width=True):
            st.session_state.vista = "Nueva Rendición"
            st.session_state.selected_id = None
            st.rerun()
        if st.sidebar.button("🗂 Mis Rendiciones", key="nav_Mis", use_container_width=True):
            st.session_state.vista = "Mis Rendiciones"
            st.session_state.selected_id = None
            st.rerun()
            
    elif rol == "supervisora":
        if st.sidebar.button("✔️ Vista Supervisora", key="nav_Supervisora", use_container_width=True):
            st.session_state.vista = "Supervisora"
            st.session_state.selected_id = None
            st.rerun()
            
    elif rol == "finanzas":
        if st.sidebar.button("🔍 Vista Finanzas", key="nav_Finanzas", use_container_width=True):
            st.session_state.vista = "Finanzas"
            st.session_state.selected_id = None
            st.rerun()
            
    elif rol == "tesorera":
        if st.sidebar.button("💸 Vista Tesorera", key="nav_Tesorera", use_container_width=True):
            st.session_state.vista = "Tesorera"
            st.session_state.selected_id = None
            st.rerun()
            
    elif rol == "gerencia":
        if st.sidebar.button("👔 Vista Gerencia", key="nav_Gerencia", use_container_width=True):
            st.session_state.vista = "Gerencia"
            st.session_state.selected_id = None
            st.rerun()

    # Notifications
    notifs = unread_count()
    notif_label = f"🔔 Notificaciones ({notifs})" if notifs else "🔔 Notificaciones"
    if st.sidebar.button(notif_label, key="nav_notif", use_container_width=True):
        st.session_state.vista = "Notificaciones"
        st.session_state.selected_id = None
        st.rerun()

    # Demo Simulation Panel
    st.sidebar.markdown("---")
    with st.sidebar.expander("⚙️ Panel de Simulación (Demo)", expanded=True):
        st.caption("Cambia instantáneamente de usuario activo para probar el flujo de punta a punta:")
        usuarios = get_all_usuarios()
        for u in usuarios:
            # Highlight current simulated user
            is_current = u["username"] == user["username"]
            btn_style = "primary" if is_current else "secondary"
            btn_txt = f"{u['avatar']} {u['nombre']}"
            if is_current:
                btn_txt += " (Activo)"
            if st.button(btn_txt, key=f"sim_{u['username']}", use_container_width=True, type=btn_style):
                st.session_state.usuario = u
                st.session_state.selected_id = None
                st.session_state.vista = "Dashboard"
                st.rerun()

def render_estado_badge(estado: str):
    """Render estado badge HTML"""
    color = ESTADO_COLOR.get(estado, "#94a3b8")
    icon = ESTADO_ICON.get(estado, "")
    st.markdown(
        f"<span class='badge badge-{estado.lower().replace(' ', '_').replace('.', '')}'>"
        f"{icon} {estado}</span>",
        unsafe_allow_html=True
    )

def render_timeline_item(estado: str, fecha: str, nota: str, actor: str):
    """Render timeline item for historial"""
    color = ESTADO_COLOR.get(estado, "#94a3b8")
    st.markdown(
        f"<div class='timeline-item'>"
        f"<div class='timeline-dot' style='background:{color};margin-top:5px;'></div>"
        f"<div><b style='color:{color};'>{estado}</b> · <span style='color:#94a3b8;font-size:.8rem;'>{fecha}</span><br>"
        f"<span style='font-size:.85rem;color:#c0c8d8;'>{nota}</span><br>"
        f"<span style='font-size:.78rem;color:#64748b;'>Actor: {actor}</span></div>"
        f"</div>",
        unsafe_allow_html=True
    )

def render_alert_warning(text: str):
    """Render warning alert"""
    st.markdown(f"<div class='alert-warning'>⚠ {text}</div>", unsafe_allow_html=True)

def render_alert_error(text: str):
    """Render error alert"""
    st.markdown(f"<div class='alert-error'>{text}</div>", unsafe_allow_html=True)

def render_alert_success(text: str):
    """Render success alert"""
    st.markdown(f"<div class='alert-success'>{text}</div>", unsafe_allow_html=True)

def render_alert_info(text: str):
    """Render info alert"""
    st.markdown(f"<div class='alert-info'>ℹ {text}</div>", unsafe_allow_html=True)

def render_divider():
    """Render horizontal divider"""
    st.markdown("<hr style='border:none;border-top:1px solid #1e2433;margin:6px 0;'>", unsafe_allow_html=True)
