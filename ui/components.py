import streamlit as st
from models.constants import ESTADO_COLOR, ESTADO_ICON

def render_sidebar():
    """Render main sidebar navigation"""
    from services.rendicion_service import unread_count
    
    st.sidebar.markdown("## 💼 GastosApp")
    st.sidebar.caption("Sistema de Rendición de Gastos · PMN Fase 2")
    st.sidebar.markdown("---")

    notifs = unread_count()
    menu_items = {
        "Dashboard": "Dashboard",
        "Nueva Rendición": "Nueva Rendición",
        f"Mis Rendiciones": "Mis Rendiciones",
    }
    st.sidebar.markdown("**EMPLEADO**")
    for label, vista in menu_items.items():
        if st.sidebar.button(label, key=f"nav_{vista}", use_container_width=True):
            st.session_state.vista = vista
            st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("**OTROS ROLES**")
    roles = {
        "✔️ Supervisora (Catalina)": "Supervisora",
        "Finanzas (Mario)": "Finanzas",
        "Tesorera (Rosa)": "Tesorera",
        "👔 Gerencia (Finanzas)": "Gerencia",
    }
    for label, vista in roles.items():
        if st.sidebar.button(label, key=f"nav_{vista}", use_container_width=True):
            st.session_state.vista = vista
            st.rerun()

    st.sidebar.markdown("---")
    notif_label = f"🔔 Notificaciones ({notifs})" if notifs else "🔔 Notificaciones"
    if st.sidebar.button(notif_label, key="nav_notif", use_container_width=True):
        st.session_state.vista = "Notificaciones"
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Francisco Benavides**")
    st.sidebar.caption("Ingeniero de Terreno")

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
