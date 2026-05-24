import streamlit as st

def setup_page_config():
    """Setup Streamlit page configuration"""
    st.set_page_config(
        page_title="GastosApp — Rendición de Gastos",
        page_icon="💼",
        layout="wide",
        initial_sidebar_state="expanded",
    )

def setup_custom_css():
    """Setup custom CSS styling"""
    st.markdown("""
<style>
    /* General */
    [data-testid="stAppViewContainer"] { background: #0f1117; }
    [data-testid="stSidebar"] { background: #161b27; border-right: 1px solid #2a3045; }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

    /* Status badges */
    .badge {
        display: inline-block;
        padding: 3px 12px;
        border-radius: 99px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.04em;
    }
    .badge-borrador   { background: rgba(148,163,184,.15); color: #94a3b8; }
    .badge-pendiente  { background: rgba(250,204,21,.15);  color: #facc15; }
    .badge-aprobado   { background: rgba(96,165,250,.15);  color: #60a5fa; }
    .badge-observado  { background: rgba(251,146,60,.15);  color: #fb923c; }
    .badge-autorizado { background: rgba(167,139,250,.15); color: #a78bfa; }
    .badge-pagado     { background: rgba(74,222,128,.15);  color: #4ade80; }
    .badge-finalizado { background: rgba(74,222,128,.1);   color: #4ade80; border: 1px solid rgba(74,222,128,.3); }
    .badge-rechazado  { background: rgba(248,113,113,.15); color: #f87171; }
    .badge-cancelado  { background: rgba(148,163,184,.1);  color: #64748b; }
    .badge-en_cola    { background: rgba(251,146,60,.15);  color: #fb923c; }
    .badge-pend_gerencia { background: rgba(167,139,250,.2); color: #a78bfa; }

    /* Cards */
    .rendicion-card {
        background: #1e2433;
        border: 1px solid #2a3045;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
        transition: border-color .2s;
    }
    .rendicion-card:hover { border-color: #c9a84c; }

    /* Stat cards */
    .stat-card {
        background: #1e2433;
        border: 1px solid #2a3045;
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
    }
    .stat-number { font-size: 2rem; font-weight: 800; }
    .stat-label  { font-size: 0.8rem; color: #7a849c; margin-top: 4px; }

    /* Alerts */
    .alert-warning {
        background: rgba(201,168,76,.1);
        border: 1px solid rgba(201,168,76,.3);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        color: #e8c97a;
        font-size: 0.85rem;
        margin: 0.5rem 0;
    }
    .alert-error {
        background: rgba(248,113,113,.1);
        border: 1px solid rgba(248,113,113,.3);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        color: #f87171;
        font-size: 0.85rem;
        margin: 0.5rem 0;
    }
    .alert-success {
        background: rgba(74,222,128,.1);
        border: 1px solid rgba(74,222,128,.3);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        color: #4ade80;
        font-size: 0.85rem;
        margin: 0.5rem 0;
    }
    .alert-info {
        background: rgba(96,165,250,.1);
        border: 1px solid rgba(96,165,250,.3);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        color: #60a5fa;
        font-size: 0.85rem;
        margin: 0.5rem 0;
    }

    /* Timeline */
    .timeline-item {
        display: flex;
        gap: 0.75rem;
        margin-bottom: 0.6rem;
        font-size: 0.85rem;
        color: #c0c8d8;
    }
    .timeline-dot {
        width: 10px; height: 10px;
        border-radius: 50%;
        flex-shrink: 0;
        margin-top: 4px;
    }

    /* Divider */
    .section-divider {
        border: none;
        border-top: 1px solid #2a3045;
        margin: 1.5rem 0;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)
