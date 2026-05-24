import streamlit as st
from models.constants import TIPO_COLOR
from services.rendicion_service import mark_notification_read, mark_all_notifications_read

def render_notificaciones():
    """Render notifications view"""
    st.title("🔔 Notificaciones")
    notifs = st.session_state.notifications

    col_a, col_b = st.columns([4, 1])
    with col_b:
        if st.button("✓ Marcar todas leídas"):
            mark_all_notifications_read()
            st.rerun()

    st.markdown("---")
    if not notifs:
        st.info("No hay notificaciones.")
        return

    for i, n in enumerate(notifs):
        color = TIPO_COLOR.get(n["tipo"], "#94a3b8")
        opacidad = "1" if not n["leida"] else "0.5"
        st.markdown(
            f"<div style='background:#1e2433;border:1px solid {color}44;border-left:3px solid {color};"
            f"border-radius:8px;padding:.75rem 1rem;margin-bottom:.5rem;opacity:{opacidad};'>"
            f"<span style='font-size:.9rem;'>{n['msg']}</span></div>",
            unsafe_allow_html=True
        )
        if not n["leida"]:
            if st.button("✓ Marcar leída", key=f"notif_{i}"):
                mark_notification_read(i)
                st.rerun()
