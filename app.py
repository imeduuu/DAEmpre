"""
GastosApp - Sistema de Rendición de Gastos
Main entry point for the Streamlit application
"""

import streamlit as st
from config.styles import setup_page_config, setup_custom_css
from services.state import init_state
from ui.components import render_sidebar
from pages.dashboard import render_dashboard
from pages.nueva_rendicion import render_nueva
from pages.mis_rendiciones import render_mis_rendiciones
from pages.vista_rol import render_vista_rol
from pages.notificaciones import render_notificaciones

def render_login():
    """Render an ultra-premium glassmorphic login screen for corporate intranet"""
    
    # Outer layout wrapper
    st.markdown("""
        <div style="text-align: center; margin-top: 1vh; margin-bottom: 2.5rem;">
            <div style="display: inline-flex; align-items: center; justify-content: center; background: rgba(250, 204, 21, 0.08); border: 1px solid rgba(250, 204, 21, 0.2); border-radius: 99px; padding: 6px 20px; margin-bottom: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.15);">
                <span style="font-size: 0.82rem; font-weight: 700; color: #facc15; letter-spacing: 0.05em; text-transform: uppercase;">🔒 Acceso Seguro Intranet</span>
            </div>
            <h1 style="font-size: 3.5rem; font-weight: 900; margin: 0; background: linear-gradient(135deg, #ffffff 30%, #a5b4fc 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -2px;">💼 GastosApp</h1>
            <p style="color: #7d8fa9; font-size: 1rem; margin-top: 6px; font-weight: 500;">Sistema de Rendición y Aprobación de Gastos Empresariales · Fase Final PMV</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col_spacer, col2 = st.columns([1.1, 0.15, 1])
    
    with col1:
        st.markdown("""
            <div style="background: linear-gradient(145deg, #121826 0%, #0a0d16 100%); border: 1px solid #1a2236; border-radius: 20px; padding: 2rem; box-shadow: 0 15px 35px rgba(0,0,0,0.4);">
                <h3 style="margin-top:0; color:#60a5fa; font-size: 1.4rem; font-weight: 800; display:flex; align-items:center; gap:8px;">🔑 Iniciar Sesión</h3>
                <p style="color:#7d8fa9; font-size:0.85rem; margin-top: 5px; margin-bottom: 20px;">Ingresa tus credenciales registradas para autenticarte.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # We will embed the form inside this beautiful container
        with st.form("login_form"):
            username = st.text_input("Nombre de Usuario", placeholder="ej: tomas, camila, mario, rosa, gerente")
            password = st.text_input("Contraseña", type="password", placeholder="••••")
            submitted = st.form_submit_button("Entrar al Sistema", use_container_width=True, type="primary")
            
            if submitted:
                from services.database import validate_credentials
                user = validate_credentials(username, password)
                if user:
                    st.session_state.usuario = user
                    st.session_state.vista = "Dashboard"
                    st.success(f"¡Bienvenido(a), {user['nombre']}!")
                    st.rerun()
                else:
                    st.error("❌ Credenciales incorrectas. Pista: Contraseña es '1234'")
                    
    with col2:
        st.markdown("""
            <div style="background: linear-gradient(145deg, #121826 0%, #0a0d16 100%); border: 1px solid #1a2236; border-radius: 20px; padding: 2rem; box-shadow: 0 15px 35px rgba(0,0,0,0.4); height: 100%;">
                <h3 style="margin-top:0; color:#facc15; font-size: 1.4rem; font-weight: 800;">⚙️ Acceso Rápido (Evaluador)</h3>
                <p style="color:#7d8fa9; font-size:0.85rem; margin-top: 5px; margin-bottom: 20px;">Haz clic en un empleado para iniciar sesión automáticamente y auditar su flujo operacional:</p>
            </div>
        """, unsafe_allow_html=True)
        
        from services.database import get_all_usuarios
        usuarios = get_all_usuarios()
        
        # Grid layout for quick login buttons to make it gorgeous
        for u in usuarios:
            btn_label = f"{u['avatar']} {u['nombre']} — {u['cargo']}"
            if st.button(btn_label, key=f"quick_{u['username']}", use_container_width=True):
                st.session_state.usuario = u
                st.session_state.vista = "Dashboard"
                st.success(f"Sesión iniciada como {u['nombre']}")
                st.rerun()

def main():
    """Main application router"""
    # Setup
    setup_page_config()
    setup_custom_css()
    init_state()
    
    # Check if user is logged in
    if not st.session_state.usuario:
        render_login()
        return
        
    # Render sidebar for logged in users
    render_sidebar()

    # Route to correct view with role access control
    vista = st.session_state.vista
    rol = st.session_state.usuario["rol"]
    
    # Role-based path authorization
    allowed_vistas = {
        "rendidor": ["Dashboard", "Nueva Rendición", "Mis Rendiciones", "Notificaciones"],
        "supervisora": ["Dashboard", "Supervisora", "Notificaciones"],
        "finanzas": ["Dashboard", "Finanzas", "Notificaciones"],
        "tesorera": ["Dashboard", "Tesorera", "Notificaciones"],
        "gerencia": ["Dashboard", "Gerencia", "Notificaciones"]
    }
    
    # If the user tries to access a view not allowed for their role, redirect to Dashboard
    if vista not in allowed_vistas.get(rol, ["Dashboard"]):
        vista = "Dashboard"
        st.session_state.vista = "Dashboard"

    if vista == "Dashboard":
        render_dashboard()

    elif vista == "Nueva Rendición" and rol == "rendidor":
        render_nueva()

    elif vista == "Mis Rendiciones" and rol == "rendidor":
        render_mis_rendiciones()

    elif vista == "Supervisora" and rol == "supervisora":
        render_vista_rol(
            rol="supervisora",
            titulo="✔️ Vista Supervisora — Camila Fuentes",
            descripcion="Valida pertinencia operativa del gasto (BR-03: no verifica legalidad tributaria).",
            estados_visibles=["Pendiente"]
        )

    elif vista == "Finanzas" and rol == "finanzas":
        render_vista_rol(
            rol="finanzas",
            titulo="🔍 Vista Analista de Finanzas — Mario Leal",
            descripcion="Verifica validez tributaria en SII, legibilidad e integridad del documento.",
            estados_visibles=["Aprobado"]
        )

    elif vista == "Tesorera" and rol == "tesorera":
        render_vista_rol(
            rol="tesorera",
            titulo="💸 Vista Tesorera — Rosa Pinto",
            descripcion="Ejecuta reembolsos. Gestiona cola de pagos por falta de liquidez (BR-10).",
            estados_visibles=["Autorizado", "En Cola de Pago"]
        )

    elif vista == "Gerencia" and rol == "gerencia":
        render_vista_rol(
            rol="gerencia",
            titulo="👔 Vista Gerencia de Finanzas",
            descripcion="Aprueba gastos extraordinarios (> $500.000, BR-05) y excepciones de plazo (BR-09).",
            estados_visibles=["Pend. Gerencia"]
        )

    elif vista == "Notificaciones":
        render_notificaciones()

if __name__ == "__main__":
    main()
