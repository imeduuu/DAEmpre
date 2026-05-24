import streamlit as st
from datetime import datetime
from models.types import Rendicion, Notificacion
from services import database

def add_historial(rid: str, estado: str, actor: str, nota: str):
    """Add history entry to rendicion"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    st.session_state.rendiciones[rid]["historial"].append({
        "estado": estado,
        "actor": actor,
        "fecha": ts,
        "nota": nota
    })
    st.session_state.rendiciones[rid]["estado"] = estado
    
    # Save to database
    database.update_rendicion(rid, {
        "historial": st.session_state.rendiciones[rid]["historial"],
        "estado": estado
    })

def add_notif(tipo: str, msg: str):
    """Add notification"""
    notif = {"tipo": tipo, "msg": msg, "leida": False}
    st.session_state.notifications.insert(0, notif)
    
    # Save to database
    database.create_notificacion(notif)

def unread_count() -> int:
    """Get count of unread notifications"""
    return sum(1 for n in st.session_state.notifications if not n["leida"])

def mark_notification_read(index: int):
    """Mark notification as read"""
    if 0 <= index < len(st.session_state.notifications):
        st.session_state.notifications[index]["leida"] = True
        # Save to database
        database.update_notificacion(index, {"leida": True})

def mark_all_notifications_read():
    """Mark all notifications as read"""
    for n in st.session_state.notifications:
        n["leida"] = True
    # Save all to database
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE notificaciones SET leida = 1")
    conn.commit()
    conn.close()

def get_rendiciones_by_estado(estado: str) -> list[Rendicion]:
    """Get all rendiciones with specified estado"""
    rends = st.session_state.rendiciones
    return [r for r in rends.values() if r["estado"] == estado]

def get_rendiciones_sorted() -> list[Rendicion]:
    """Get all rendiciones sorted by date (newest first)"""
    rends = st.session_state.rendiciones
    return sorted(rends.values(), key=lambda x: x["historial"][-1]["fecha"], reverse=True)

def get_rendicion(rid: str) -> Rendicion | None:
    """Get specific rendicion by ID"""
    return st.session_state.rendiciones.get(rid)

def update_rendicion(rid: str, updates: dict):
    """Update rendicion with new data"""
    if rid in st.session_state.rendiciones:
        st.session_state.rendiciones[rid].update(updates)
        # Save to database
        database.update_rendicion(rid, updates)

def create_rendicion(rid: str, data: Rendicion):
    """Create new rendicion"""
    st.session_state.rendiciones[rid] = data
    # Save to database
    database.create_rendicion(data)
