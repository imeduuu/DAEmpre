import sqlite3
import json
from pathlib import Path
from typing import Optional
from models.types import Rendicion, Notificacion

# Database path
DB_PATH = Path(__file__).parent.parent / "data" / "gastos.db"

def get_connection():
    """Get database connection"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database schema"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create rendiciones table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rendiciones (
            id TEXT PRIMARY KEY,
            descripcion TEXT NOT NULL,
            categoria TEXT NOT NULL,
            monto REAL NOT NULL,
            fecha_comprobante TEXT NOT NULL,
            fecha_envio TEXT NOT NULL,
            estado TEXT NOT NULL,
            rendidor TEXT NOT NULL,
            archivo TEXT NOT NULL,
            observaciones TEXT NOT NULL,
            historial TEXT NOT NULL,
            intentos_correccion INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create notificaciones table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notificaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            msg TEXT NOT NULL,
            leida BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def get_all_rendiciones() -> dict[str, Rendicion]:
    """Get all rendiciones from database"""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM rendiciones ORDER BY updated_at DESC")
    rows = cursor.fetchall()
    conn.close()
    
    rendiciones = {}
    for row in rows:
        rid = row['id']
        rendiciones[rid] = {
            "id": row['id'],
            "descripcion": row['descripcion'],
            "categoria": row['categoria'],
            "monto": row['monto'],
            "fecha_comprobante": row['fecha_comprobante'],
            "fecha_envio": row['fecha_envio'],
            "estado": row['estado'],
            "rendidor": row['rendidor'],
            "archivo": row['archivo'],
            "observaciones": json.loads(row['observaciones']),
            "historial": json.loads(row['historial']),
            "intentos_correccion": row['intentos_correccion'],
        }
    
    return rendiciones

def get_rendicion(rid: str) -> Optional[Rendicion]:
    """Get specific rendicion by ID"""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM rendiciones WHERE id = ?", (rid,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
    
    return {
        "id": row['id'],
        "descripcion": row['descripcion'],
        "categoria": row['categoria'],
        "monto": row['monto'],
        "fecha_comprobante": row['fecha_comprobante'],
        "fecha_envio": row['fecha_envio'],
        "estado": row['estado'],
        "rendidor": row['rendidor'],
        "archivo": row['archivo'],
        "observaciones": json.loads(row['observaciones']),
        "historial": json.loads(row['historial']),
        "intentos_correccion": row['intentos_correccion'],
    }

def create_rendicion(rendicion: Rendicion):
    """Create new rendicion"""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO rendiciones 
        (id, descripcion, categoria, monto, fecha_comprobante, fecha_envio, 
         estado, rendidor, archivo, observaciones, historial, intentos_correccion)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        rendicion['id'],
        rendicion['descripcion'],
        rendicion['categoria'],
        rendicion['monto'],
        rendicion['fecha_comprobante'],
        rendicion['fecha_envio'],
        rendicion['estado'],
        rendicion['rendidor'],
        rendicion['archivo'],
        json.dumps(rendicion['observaciones']),
        json.dumps(rendicion['historial']),
        rendicion['intentos_correccion'],
    ))
    
    conn.commit()
    conn.close()

def update_rendicion(rid: str, updates: dict):
    """Update rendicion"""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get current rendicion
    rendicion = get_rendicion(rid)
    if not rendicion:
        conn.close()
        return
    
    # Merge updates
    rendicion.update(updates)
    
    cursor.execute("""
        UPDATE rendiciones 
        SET descripcion=?, categoria=?, monto=?, fecha_comprobante=?, 
            fecha_envio=?, estado=?, rendidor=?, archivo=?, 
            observaciones=?, historial=?, intentos_correccion=?, updated_at=CURRENT_TIMESTAMP
        WHERE id=?
    """, (
        rendicion['descripcion'],
        rendicion['categoria'],
        rendicion['monto'],
        rendicion['fecha_comprobante'],
        rendicion['fecha_envio'],
        rendicion['estado'],
        rendicion['rendidor'],
        rendicion['archivo'],
        json.dumps(rendicion['observaciones']),
        json.dumps(rendicion['historial']),
        rendicion['intentos_correccion'],
        rid,
    ))
    
    conn.commit()
    conn.close()

def delete_rendicion(rid: str):
    """Delete rendicion"""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM rendiciones WHERE id = ?", (rid,))
    conn.commit()
    conn.close()

def get_all_notificaciones() -> list[Notificacion]:
    """Get all notificaciones"""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM notificaciones ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    
    notificaciones = []
    for row in rows:
        notificaciones.append({
            "tipo": row['tipo'],
            "msg": row['msg'],
            "leida": bool(row['leida']),
        })
    
    return notificaciones

def create_notificacion(notificacion: Notificacion):
    """Create new notificacion"""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO notificaciones (tipo, msg, leida)
        VALUES (?, ?, ?)
    """, (
        notificacion['tipo'],
        notificacion['msg'],
        notificacion['leida'],
    ))
    
    conn.commit()
    conn.close()

def update_notificacion(index: int, updates: dict):
    """Update notificacion by index"""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE notificaciones 
        SET leida = ?
        WHERE rowid = (SELECT rowid FROM notificaciones ORDER BY created_at DESC LIMIT 1 OFFSET ?)
    """, (updates.get('leida', False), index))
    
    conn.commit()
    conn.close()

def clear_all_data():
    """Clear all data (for reset)"""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM rendiciones")
    cursor.execute("DELETE FROM notificaciones")
    
    conn.commit()
    conn.close()
