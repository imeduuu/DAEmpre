# Estado colors and icons mapping
ESTADO_COLOR = {
    "Borrador":      "#94a3b8",
    "Pendiente":     "#facc15",
    "Aprobado":      "#60a5fa",
    "Observado":     "#fb923c",
    "Autorizado":    "#a78bfa",
    "Pend. Gerencia":"#a78bfa",
    "En Cola de Pago":"#fb923c",
    "Pagado":        "#4ade80",
    "Finalizado":    "#4ade80",
    "Rechazado":     "#f87171",
    "Cancelado":     "#64748b",
}

ESTADO_ICON = {
    "Borrador":       "📝",
    "Pendiente":      "⏳",
    "Aprobado":       "✅",
    "Observado":      "🔍",
    "Autorizado":     "🔐",
    "Pend. Gerencia": "🏦",
    "En Cola de Pago":"⏰",
    "Pagado":         "💸",
    "Finalizado":     "🎉",
    "Rechazado":      "❌",
    "Cancelado":      "🚫",
}

# Notification types
TIPO_COLOR = {
    "observado":  "#fb923c",
    "cola":       "#fb923c",
    "gerencia":   "#a78bfa",
    "pendiente":  "#facc15",
    "aprobado":   "#60a5fa",
    "autorizado": "#a78bfa",
    "pagado":     "#4ade80",
    "finalizado": "#4ade80",
    "rechazado":  "#f87171",
    "cancelado":  "#64748b",
    "warning":    "#facc15",
}

# Validation rules
DESCRIPCION_MIN_CHARS = 10
DIAS_PLAZO_COMPROBANTE = 30
MONTO_UMBRAL_GERENCIA = 500000
INTENTOS_CORRECCION_MAX = 3
DIAS_COLA_PAGO_MAX = 10
