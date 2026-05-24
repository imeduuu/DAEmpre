# SQLite Database Integration

## Overview

La aplicación GastosApp ahora incluye **persistencia de datos con SQLite**. Todos los datos (rendiciones y notificaciones) se guardan automáticamente en la base de datos.

## Database Structure

### Location
```
data/gastos.db
```

### Tables

#### `rendiciones`
Almacena todas las rendiciones de gastos.

| Column | Type | Description |
|--------|------|-------------|
| id | TEXT | ID único de la rendición (TX-XXXX) |
| descripcion | TEXT | Descripción del gasto |
| categoria | TEXT | Categoría (Transporte, Alimentación, etc.) |
| monto | REAL | Monto en CLP |
| fecha_comprobante | TEXT | Fecha del comprobante (YYYY-MM-DD) |
| fecha_envio | TEXT | Fecha de envío (YYYY-MM-DD HH:MM) |
| estado | TEXT | Estado actual (Borrador, Pendiente, Aprobado, etc.) |
| rendidor | TEXT | Nombre del que genera la rendición |
| archivo | TEXT | Nombre del archivo adjunto |
| observaciones | TEXT | JSON array de observaciones |
| historial | TEXT | JSON array del historial de cambios |
| intentos_correccion | INTEGER | Contador de intentos de corrección |
| created_at | TIMESTAMP | Fecha de creación (auto) |
| updated_at | TIMESTAMP | Fecha de última actualización (auto) |

#### `notificaciones`
Almacena todas las notificaciones.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | ID auto-incremento |
| tipo | TEXT | Tipo de notificación (observado, cola, gerencia, etc.) |
| msg | TEXT | Mensaje de la notificación |
| leida | BOOLEAN | Si fue leída o no |
| created_at | TIMESTAMP | Fecha de creación (auto) |

## Features

✅ **Datos persistentes**: Los datos sobreviven al reiniciar la app  
✅ **Auto-guardar**: Cada cambio se guarda automáticamente en BD  
✅ **Demo data**: Carga datos de demostración en primera ejecución  
✅ **Reset script**: Script para reinicializar la BD con datos demo  

## How to Use

### First Run
La app automáticamente:
1. Crea la base de datos en `data/gastos.db`
2. Crea las tablas
3. Carga los datos de demostración una sola vez

### Reset Database
Para reinicializar la base de datos con datos de demostración:

```bash
python scripts/reset_db.py
```

### Access Database Directly
Puedes inspeccionar la base de datos con cualquier herramienta SQLite:

```bash
sqlite3 data/gastos.db
```

Ejemplos de queries:

```sql
-- Ver todas las rendiciones
SELECT id, estado, monto, fecha_envio FROM rendiciones ORDER BY updated_at DESC;

-- Ver notificaciones no leídas
SELECT * FROM notificaciones WHERE leida = 0;

-- Ver rendiciones por estado
SELECT COUNT(*) FROM rendiciones WHERE estado = 'Aprobado';
```

## Code Architecture

### Database Module
`services/database.py` - Maneja todas las operaciones con la BD:
- `init_db()` - Crea las tablas si no existen
- `get_all_rendiciones()` - Obtiene todas las rendiciones
- `create_rendicion()` - Crea nueva rendición
- `update_rendicion()` - Actualiza una rendición
- `delete_rendicion()` - Elimina una rendición
- `get_all_notificaciones()` - Obtiene todas las notificaciones
- `create_notificacion()` - Crea nueva notificación

### Service Layer
`services/rendicion_service.py` - Sincroniza con la BD:
- `add_historial()` - Agrega evento al historial y guarda en BD
- `add_notif()` - Agrega notificación y guarda en BD
- `update_rendicion()` - Actualiza en memoria y BD
- Todas las funciones que modifican datos ahora persistirán cambios

## Data Flow

```
User Action
    ↓
UI Component (pages/)
    ↓
Service Layer (services/rendicion_service.py)
    ↓
Session State (memory) + Database (SQLite)
    ↓
Persistence ✅
```

## Important Notes

- **JSON Storage**: `observaciones` e `historial` se almacenan como JSON text
- **Timestamps**: Las tablas tienen `created_at` y `updated_at` automáticas
- **Auto-increment**: Las notificaciones tienen ID auto-incremental
- **Sincronización**: El estado de sesión y la BD se mantienen sincronizados

## Troubleshooting

### Database locked
Si ves error "database is locked":
- Cierra todas las instancias de la app
- Espera unos segundos
- Reinicia

### Corrupted database
Si la BD se corrompe:
```bash
python scripts/reset_db.py
```

### Need fresh data
```bash
rm data/gastos.db
python scripts/reset_db.py
```
