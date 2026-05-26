import streamlit as st
from models.types import Rendicion
from utils.formatters import fmt_monto
from services.rendicion_service import add_historial, add_notif
from models.constants import INTENTOS_CORRECCION_MAX, MONTO_UMBRAL_GERENCIA

def render_acciones(r: Rendicion, rol: str):
    """Render role-based actions for rendicion"""
    rid = r["id"]
    estado = r["estado"]

    # Get active user from state or default based on role
    user_name = "Sistema"
    if "usuario" in st.session_state and st.session_state.usuario:
        user_name = st.session_state.usuario["nombre"]
    else:
        # Fallback names
        fallback_names = {
            "rendidor": "Tomás Alarcón",
            "supervisora": "Camila Fuentes",
            "finanzas": "Mario Leal",
            "tesorera": "Rosa Pinto",
            "gerencia": "Gerente de Finanzas"
        }
        user_name = fallback_names.get(rol, "Sistema")

    # RENDIDOR: Correct observado
    if rol == "rendidor" and estado == "Observado":
        st.markdown("**Corregir y reenviar**")
        st.caption(f"Intentos usados: {r['intentos_correccion']}/{INTENTOS_CORRECCION_MAX} (BR-08)")
        nuevo_archivo = st.file_uploader("Subir comprobante corregido", type=["jpg", "jpeg", "png", "pdf"], key=f"fix_{rid}")
        if st.button("Reenviar rendición corregida", key=f"reenviar_{rid}", type="primary"):
            if nuevo_archivo:
                if r["intentos_correccion"] >= INTENTOS_CORRECCION_MAX:
                    add_historial(rid, "Rechazado", "Sistema", "BR-08: Límite de 3 correcciones alcanzado.")
                    add_notif("rechazado", f"{rid}: Rechazada automáticamente por límite de correcciones (BR-08).")
                    st.error("BR-08: Límite de correcciones alcanzado. Rendición rechazada.")
                else:
                    # Save physical file
                    import os
                    os.makedirs("data/comprobantes", exist_ok=True)
                    safe_filename = f"{rid}_REV{r['intentos_correccion'] + 1}_{nuevo_archivo.name}"
                    file_path = os.path.join("data/comprobantes", safe_filename)
                    with open(file_path, "wb") as f:
                        f.write(nuevo_archivo.getbuffer())

                    r["archivo"] = safe_filename
                    r["intentos_correccion"] += 1
                    r["observaciones"] = []
                    add_historial(rid, "Borrador", user_name, f"Comprobante corregido subido físicamente: {nuevo_archivo.name}")
                    add_historial(rid, "Pendiente", "Sistema", "Rendición reenviada. Aprobación previa de Supervisora queda nula. Re-notificada Camila Fuentes.")
                    add_notif("pendiente", f"{rid}: Rendición corregida. Camila Fuentes debe re-aprobar.")
                    st.success("Rendición reenviada. Camila Fuentes debe re-aprobar.")
                    st.rerun()
            else:
                st.warning("Debes adjuntar el comprobante corregido.")

    # RENDIDOR: Cancel
    if rol == "rendidor" and estado in ("Borrador", "Pendiente", "Observado"):
        if st.button("Cancelar esta rendición", key=f"cancel_{rid}"):
            add_historial(rid, "Cancelado", user_name, "Cancelación voluntaria por el rendidor.")
            add_notif("cancelado", f"{rid}: Cancelada voluntariamente.")
            st.warning("Rendición cancelada.")
            st.session_state.selected_id = None
            st.rerun()

    # SUPERVISORA
    if rol == "supervisora" and estado == "Pendiente":
        st.markdown("**Acción Supervisora**")
        obs_s = st.text_area("Observación (opcional para rechazo):", key=f"obs_sup_{rid}", height=70)
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Aprobar pertinencia operativa", key=f"apr_{rid}", type="primary", use_container_width=True):
                if r["monto"] > MONTO_UMBRAL_GERENCIA:
                    add_historial(rid, "Aprobado", user_name, "Pertinencia operativa confirmada.")
                    add_historial(rid, "Pend. Gerencia", "Sistema", f"BR-05: Monto {fmt_monto(r['monto'])} > $500.000. Escalado a Gerencia de Finanzas.")
                    add_notif("gerencia", f"{rid}: Escalada a Gerencia por monto {fmt_monto(r['monto'])}.")
                else:
                    add_historial(rid, "Aprobado", user_name, "Pertinencia operativa confirmada.")
                    add_historial(rid, "Aprobado", "Sistema", "Notificado Mario Leal (Analista Finanzas).")
                    add_notif("aprobado", f"{rid}: Aprobada por Supervisora. Pendiente Finanzas.")
                st.success("Aprobada. Escalada a siguiente etapa.")
                st.session_state.selected_id = None
                st.rerun()
        with col_b:
            if st.button("Rechazar", key=f"rec_{rid}", use_container_width=True):
                nota = obs_s if obs_s else "Rechazada por Supervisora sin observación específica."
                add_historial(rid, "Rechazado", user_name, nota)
                r["observaciones"].append(nota)
                add_notif("rechazado", f"{rid}: Rechazada por Supervisora. Motivo: {nota}")
                st.error("Rechazada.")
                st.session_state.selected_id = None
                st.rerun()

    # FINANZAS
    if rol == "finanzas" and estado == "Aprobado":
        st.markdown("**Acción Analista de Finanzas**")
        obs_f = st.text_area("Observación:", key=f"obs_fin_{rid}", height=70)
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            if st.button("Autorizar", key=f"aut_{rid}", type="primary", use_container_width=True):
                add_historial(rid, "Autorizado", user_name, "Documento válido en SII. Monto coincide.")
                add_notif("autorizado", f"{rid}: Autorizada por Finanzas. Pendiente pago.")
                st.success("Autorizada.")
                st.session_state.selected_id = None
                st.rerun()
        with col_b:
            if st.button("Observar", key=f"obs_{rid}", use_container_width=True):
                nota = obs_f if obs_f else "Documento requiere corrección."
                if r["intentos_correccion"] >= INTENTOS_CORRECCION_MAX:
                    add_historial(rid, "Rechazado", "Sistema", "BR-08: Límite de 3 observaciones alcanzado.")
                    add_notif("rechazado", f"{rid}: Rechazada por límite de observaciones.")
                else:
                    add_historial(rid, "Observado", user_name, nota)
                    r["observaciones"].append(nota)
                    add_notif("observado", f"{rid}: Observada por Finanzas: {nota}")
                st.warning("Marcada como Observada.")
                st.session_state.selected_id = None
                st.rerun()
        with col_c:
            if st.button("Rechazar", key=f"rec_fin_{rid}", use_container_width=True):
                nota = obs_f if obs_f else "Documento fraudulento o inválido."
                add_historial(rid, "Rechazado", user_name, nota)
                r["observaciones"].append(nota)
                add_notif("rechazado", f"{rid}: Rechazada por Finanzas.")
                st.error("Rechazada definitivamente.")
                st.session_state.selected_id = None
                st.rerun()

    # GERENCIA
    if rol == "gerencia" and estado == "Pend. Gerencia":
        st.markdown("**Acción Gerencia de Finanzas**")
        obs_g = st.text_area("Fundamento (opcional):", key=f"obs_ger_{rid}", height=70)
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Aprobar gasto extraordinario", key=f"ger_apr_{rid}", type="primary", use_container_width=True):
                add_historial(rid, "Autorizado", user_name, obs_g or "Gasto extraordinario aprobado por Gerencia.")
                add_notif("autorizado", f"{rid}: Aprobada por Gerencia. Pendiente pago.")
                st.success("Aprobada por Gerencia.")
                st.session_state.selected_id = None
                st.rerun()
        with col_b:
            if st.button("Rechazar", key=f"ger_rec_{rid}", use_container_width=True):
                nota = obs_g if obs_g else "Gasto extraordinario no justificado."
                add_historial(rid, "Rechazado", user_name, nota)
                add_notif("rechazado", f"{rid}: Rechazada por Gerencia.")
                st.error("Rechazada por Gerencia.")
                st.session_state.selected_id = None
                st.rerun()

    # TESORERA
    if rol == "tesorera" and estado == "Autorizado":
        st.markdown("**Acción Tesorera**")
        hay_liquidez = st.radio("¿Hay liquidez en caja?", ["Sí, ejecutar pago", "No, encolar pago"], key=f"liq_{rid}")
        if st.button("Confirmar", key=f"pagar_{rid}", type="primary"):
            if "Sí" in hay_liquidez:
                add_historial(rid, "Pagado", user_name, "Transferencia ejecutada. Comprobante bancario subido.")
                add_historial(rid, "Finalizado", "Sistema", "Proceso cerrado. Archivado en solo lectura.")
                add_notif("pagado", f"{rid}: ¡Reembolso de {fmt_monto(r['monto'])} depositado!")
                st.success(f"Pago de {fmt_monto(r['monto'])} ejecutado. Rendición finalizada.")
            else:
                add_historial(rid, "En Cola de Pago", user_name, "Sin liquidez en caja. Rendición en cola. Fecha estimada: 3 días hábiles (BR-10).")
                add_notif("cola", f"{rid}: Sin liquidez. Pago en cola ~3 días hábiles.")
                st.warning("Rendición encolada. El sistema reintentará diariamente a las 9:00 AM (BR-10).")
            st.session_state.selected_id = None
            st.rerun()

    if rol == "tesorera" and estado == "En Cola de Pago":
        st.markdown(
            "<div class='alert-warning'><b>En Cola de Pago:</b> Sin liquidez en caja. "
            "El sistema reintenta diariamente a las 9:00 AM (BR-10). "
            "Si pasan 10 días hábiles sin liquidez, la rendición será rechazada automáticamente.</div>",
            unsafe_allow_html=True
        )
        if st.button("Liberar pago manualmente (hay fondos)", key=f"liberar_{rid}", type="primary"):
            add_historial(rid, "Pagado", user_name, "Pago liberado manualmente desde lista de pagos pendientes.")
            add_historial(rid, "Finalizado", "Sistema", "Proceso cerrado. Archivado en solo lectura.")
            add_notif("pagado", f"{rid}: ¡Reembolso {fmt_monto(r['monto'])} depositado (liberado manualmente)!")
            st.success(f"Pago liberado. {fmt_monto(r['monto'])} transferido.")
            st.session_state.selected_id = None
            st.rerun()
