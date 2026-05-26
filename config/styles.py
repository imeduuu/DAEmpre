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
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    /* Global Body and Layout Styles */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at 10% 20%, #0d111c 0%, #07090f 90%);
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stSidebar"] {
        background: #090c15;
        border-right: 1px solid #1a2035;
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.4);
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Font Hierarchy and Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        color: #ffffff;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    p, span, label, li {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #c0c8d8;
    }

    /* Scrollbars Styling */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #07090f;
    }
    ::-webkit-scrollbar-thumb {
        background: #1e2433;
        border-radius: 99px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #facc15;
    }

    /* Streamlit Form Element Overrides - Premium Styling */
    div[data-baseweb="select"] > div {
        background-color: #121826 !important;
        border: 1px solid #202738 !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        transition: all 0.2s ease-in-out;
    }
    div[data-baseweb="select"] > div:hover {
        border-color: #60a5fa !important;
    }
    
    input, textarea {
        background-color: #121826 !important;
        border: 1px solid #202738 !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        transition: all 0.2s ease-in-out;
    }
    input:focus, textarea:focus {
        border-color: #60a5fa !important;
        box-shadow: 0 0 0 1px rgba(96,165,250,0.2) !important;
    }

    /* Premium Glassmorphic Badges */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 5px 14px;
        border-radius: 99px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .badge-borrador      { background: rgba(148,163,184,.1);  color: #94a3b8; border-color: rgba(148,163,184,.2); }
    .badge-pendiente     { background: rgba(250,204,21,.1);   color: #facc15; border-color: rgba(250,204,21,.3); }
    .badge-aprobado      { background: rgba(96,165,250,.1);   color: #60a5fa; border-color: rgba(96,165,250,.3); }
    .badge-observado     { background: rgba(251,146,60,.1);   color: #fb923c; border-color: rgba(251,146,60,.3); }
    .badge-autorizado    { background: rgba(167,139,250,.15);  color: #a78bfa; border-color: rgba(167,139,250,.3); }
    .badge-pagado        { background: rgba(74,222,128,.1);   color: #4ade80; border-color: rgba(74,222,128,.3); }
    .badge-finalizado    { background: rgba(34,197,94,.08);   color: #4ade80; border: 1px solid rgba(74,222,128,.4); }
    .badge-rechazado     { background: rgba(248,113,113,.1);  color: #f87171; border-color: rgba(248,113,113,.3); }
    .badge-cancelado     { background: rgba(148,163,184,.06); color: #64748b; border-color: rgba(148,163,184,.15); }
    .badge-en_cola       { background: rgba(251,146,60,.1);   color: #fb923c; border-color: rgba(251,146,60,.3); }
    .badge-pend_gerencia  { background: rgba(167,139,250,.15);  color: #c084fc; border-color: rgba(167,139,250,.25); }

    /* Custom Premium Button (stButton Override) */
    .stButton>button {
        background: linear-gradient(135deg, #1e2538 0%, #131826 100%) !important;
        border: 1px solid #202738 !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15) !important;
    }
    .stButton>button:hover {
        border-color: #facc15 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 15px rgba(250, 204, 21, 0.15) !important;
    }
    .stButton>button:active {
        transform: translateY(1px) !important;
    }
    
    /* Primary buttons (blue/gold gradient) */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #facc15 0%, #d97706 100%) !important;
        border: none !important;
        color: #0b0d12 !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 12px rgba(250, 204, 21, 0.3) !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #fde047 0%, #f59e0b 100%) !important;
        box-shadow: 0 6px 20px rgba(250, 204, 21, 0.45) !important;
    }

    /* Cards - Premium look */
    .rendicion-card {
        background: linear-gradient(145deg, #121724 0%, #0d101b 100%);
        border: 1px solid #1a2236;
        border-radius: 16px;
        padding: 1.25rem 1.6rem;
        margin-bottom: 0.9rem;
        transition: all .28s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .rendicion-card:hover { 
        border-color: #facc15; 
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(250, 204, 21, 0.12);
    }

    /* Stat Card Style */
    .stat-card-premium {
        background: linear-gradient(145deg, #121829 0%, #0c0f1b 100%);
        border: 1px solid #1c243b;
        border-radius: 16px;
        padding: 1.4rem;
        box-shadow: 0 8px 20px rgba(0,0,0,0.25);
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: all 0.3s ease;
    }
    .stat-card-premium:hover {
        transform: translateY(-3px);
        border-color: #3b82f6;
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.15);
    }

    /* Interactive Process Flow Step Map */
    .step-map-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(18, 24, 41, 0.5);
        border: 1px solid #1a2236;
        border-radius: 16px;
        padding: 1.25rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(8px);
    }
    .step-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        flex: 1;
        position: relative;
    }
    .step-dot {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.85rem;
        background: #1c243a;
        border: 2px solid #2e3b5e;
        color: #7d8fa9;
        margin-bottom: 6px;
        transition: all 0.3s ease;
        box-shadow: 0 0 10px rgba(0,0,0,0.2);
    }
    .step-label {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        color: #7d8fa9;
        letter-spacing: 0.05em;
    }
    .step-active .step-dot {
        background: #facc15;
        border-color: #d97706;
        color: #0b0d12;
        box-shadow: 0 0 15px rgba(250, 204, 21, 0.4);
    }
    .step-active .step-label {
        color: #facc15;
    }
    .step-completed .step-dot {
        background: #10b981;
        border-color: #047857;
        color: white;
        box-shadow: 0 0 12px rgba(16, 185, 129, 0.3);
    }
    .step-completed .step-label {
        color: #10b981;
    }

    /* Custom Form Layout Panel */
    .form-panel {
        background: linear-gradient(150deg, #121826 0%, #0a0d16 100%);
        border: 1px solid #1a2236;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.35);
        margin-bottom: 1.5rem;
    }

    /* Alerts */
    .alert-warning {
        background: rgba(251,146,60,.06);
        border: 1px solid rgba(251,146,60,.2);
        border-radius: 10px;
        padding: 0.85rem 1.25rem;
        color: #fb923c;
        font-size: 0.85rem;
        margin: 0.6rem 0;
        font-weight: 500;
    }
    .alert-error {
        background: rgba(248,113,113,.06);
        border: 1px solid rgba(248,113,113,.2);
        border-radius: 10px;
        padding: 0.85rem 1.25rem;
        color: #f87171;
        font-size: 0.85rem;
        margin: 0.6rem 0;
        font-weight: 500;
    }
    .alert-success {
        background: rgba(74,222,128,.06);
        border: 1px solid rgba(74,222,128,.2);
        border-radius: 10px;
        padding: 0.85rem 1.25rem;
        color: #4ade80;
        font-size: 0.85rem;
        margin: 0.6rem 0;
        font-weight: 500;
    }
    .alert-info {
        background: rgba(96,165,250,.06);
        border: 1px solid rgba(96,165,250,.2);
        border-radius: 10px;
        padding: 0.85rem 1.25rem;
        color: #60a5fa;
        font-size: 0.85rem;
        margin: 0.6rem 0;
        font-weight: 500;
    }

    /* Timeline Styles */
    .timeline-item {
        display: flex;
        gap: 1rem;
        margin-bottom: 0.9rem;
        font-size: 0.85rem;
        color: #c0c8d8;
        padding-left: 5px;
        background: rgba(255,255,255,0.01);
        border: 1px solid rgba(255,255,255,0.02);
        padding: 10px 14px;
        border-radius: 10px;
    }
    .timeline-dot {
        width: 10px; height: 10px;
        border-radius: 50%;
        flex-shrink: 0;
        margin-top: 4px;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)
