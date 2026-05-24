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

def main():
    """Main application router"""
    # Setup
    setup_page_config()
    setup_custom_css()
    init_state()
    
    # Render sidebar
    render_sidebar()

    # Route to correct view
    vista = st.session_state.vista

    if vista == "Dashboard":
        render_dashboard()

    elif vista == "Nueva Rendición":
        render_nueva()

    elif vista == "Mis Rendiciones":
        render_mis_rendiciones()

    elif vista == "Supervisora":
        render_vista_rol(
            rol="supervisora",
            titulo="✔️ Vista Supervisora — Catalina Vergara",
            descripcion="Valida pertinencia operativa del gasto (BR-03: no verifica legalidad tributaria).",
            estados_visibles=["Pendiente"]
        )

    elif vista == "Finanzas":
        render_vista_rol(
            rol="finanzas",
            titulo="🔎 Vista Analista de Finanzas — Mario Leal",
            descripcion="Verifica validez tributaria en SII, legibilidad e integridad del documento.",
            estados_visibles=["Aprobado"]
        )

    elif vista == "Tesorera":
        render_vista_rol(
            rol="tesorera",
            titulo="🏦 Vista Tesorera — Rosa Pinto",
            descripcion="Ejecuta reembolsos. Gestiona cola de pagos por falta de liquidez (BR-10).",
            estados_visibles=["Autorizado", "En Cola de Pago"]
        )

    elif vista == "Gerencia":
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
