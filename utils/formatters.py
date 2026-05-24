from models.constants import ESTADO_COLOR, ESTADO_ICON

def fmt_monto(m: float) -> str:
    """Format amount to Chilean currency format"""
    return f"${m:,.0f}".replace(",", ".")

def badge_html(estado: str) -> str:
    """Generate HTML badge for estado"""
    cls = estado.lower().replace(" ", "_").replace(".", "")
    icon = ESTADO_ICON.get(estado, "")
    return f'<span class="badge badge-{cls}">{icon} {estado}</span>'

def get_estado_color(estado: str) -> str:
    """Get color code for estado"""
    return ESTADO_COLOR.get(estado, "#94a3b8")

def get_estado_icon(estado: str) -> str:
    """Get icon for estado"""
    return ESTADO_ICON.get(estado, "")
