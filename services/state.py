import streamlit as st
from services.database import get_all_rendiciones, get_all_notificaciones, init_db
from data.demo import get_demo_data, get_demo_notifications

def init_state():
    """Initialize session state with default values"""
    # Initialize database
    init_db()
    
    if "rendiciones" not in st.session_state:
        # Try to load from database
        rends = get_all_rendiciones()
        if not rends:
            # If empty, load demo data once
            rends = get_demo_data()
            for rid, rend in rends.items():
                from services.database import create_rendicion
                create_rendicion(rend)
        st.session_state.rendiciones = rends
    
    if "notifications" not in st.session_state:
        # Try to load from database
        notifs = get_all_notificaciones()
        if not notifs:
            # If empty, load demo notifications once
            notifs = get_demo_notifications()
            for notif in notifs:
                from services.database import create_notificacion
                create_notificacion(notif)
        st.session_state.notifications = notifs
    
    if "selected_id" not in st.session_state:
        st.session_state.selected_id = None
    if "vista" not in st.session_state:
        st.session_state.vista = "Dashboard"
