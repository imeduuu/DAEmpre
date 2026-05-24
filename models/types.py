from typing import TypedDict, List, Optional
from datetime import datetime

class HistorialItem(TypedDict):
    estado: str
    actor: str
    fecha: str
    nota: str

class Rendicion(TypedDict):
    id: str
    descripcion: str
    categoria: str
    monto: float
    fecha_comprobante: str
    fecha_envio: str
    estado: str
    rendidor: str
    archivo: str
    observaciones: List[str]
    historial: List[HistorialItem]
    intentos_correccion: int

class Notificacion(TypedDict):
    tipo: str
    msg: str
    leida: bool
