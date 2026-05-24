# GastosApp — Sistema de Rendición de Gastos
## PMN · Fase 2 · Modelado de Procesos de Negocio

Prototipo Mínimo Navegable del sistema de rendición de gastos desarrollado
en base al modelo de la Entrega 3.

---

## Cómo ejecutar

### 1. Instalar dependencias
```
pip install -r requirements.txt
```

### 2. Ejecutar la app
```
streamlit run app.py
```

Se abrirá automáticamente en tu navegador en `http://localhost:8501`

---

## Recorrido principal cubierto (Caso A — Camino Ideal)

1. **Nueva Rendición** → Francisco crea y envía la rendición
2. **Vista Supervisora** (Catalina Vergara) → Aprueba pertinencia operativa
3. **Vista Finanzas** (Mario Leal) → Autoriza validez tributaria
4. **Vista Tesorera** (Rosa Pinto) → Ejecuta el pago

---

## Reglas de negocio implementadas

| Regla | Descripción |
|-------|-------------|
| BR-05 | Montos > $500.000 escalan a Gerencia automáticamente |
| BR-06 | Descripción mínima de 10 caracteres |
| BR-07 | Monto debe ser > $0 |
| BR-08 | Máximo 3 correcciones desde estado Observado |
| BR-09 | Comprobantes de más de 30 días requieren excepción de Gerencia |
| BR-10 | Sin liquidez: sistema encola y reintenta. Tras 10 días → Rechazado |

---

## Estados del sistema implementados

- Borrador → Pendiente → Aprobado → Autorizado → Pagado → Finalizado
- Observado (con re-aprobación de Supervisora al corregir)
- Pend. Gerencia (BR-05 y BR-09)
- En Cola de Pago (BR-10)
- Rechazado · Cancelado

---

## Casos de prueba disponibles

Los datos de demostración incluyen:
- **TX-001**: Almuerzo $42.300 → Finalizado
- **TX-002**: Hospedaje $68.000 → Observado (imagen ilegible)
- **TX-003**: Equipo $620.000 → Pend. Gerencia (BR-05)
- **TX-004**: Taxi $12.500 → En Cola de Pago (sin liquidez)
- **TX-005**: Gasto personal → Rechazado por Supervisora

---

Autores: Benjamín Cantero · Eduardo Domínguez
Ingeniería Civil en Informática · UC Temuco
Profesor: Gastón Contreras
