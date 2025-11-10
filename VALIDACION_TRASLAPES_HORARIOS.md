# Validación de Traslapes en Asignación de Horarios

## Reglas de Negocio

### Restricción Principal
**Un trabajador NO puede tener dos asignaciones de horario que se traslapen en fechas**, sin importar:
- El semestre
- La plantilla de horario
- El estado de la asignación

### Definición de Traslape

Dos asignaciones se traslapan si sus rangos de fechas se cruzan de cualquier forma:

```
Asignación A: [inicio_A, fin_A]
Asignación B: [inicio_B, fin_B]

Hay traslape si:
- inicio_A <= fin_B (o fin_B es NULL)
- fin_A >= inicio_B (o fin_A es NULL)
```

### Casos de Validación

#### Caso 1: Nueva asignación con fecha fin definida
```sql
-- Busca asignaciones existentes que se traslapen
WHERE num_trabajador = ?
  AND activo_asignacion = 1
  AND (
      -- Asignación existente contiene el inicio de la nueva
      (fecha_inicio_asignacion <= nueva_fecha_fin 
       AND (fecha_fin_asignacion >= nueva_fecha_inicio OR fecha_fin_asignacion IS NULL))
      
      OR
      
      -- El inicio de asignación existente está dentro del rango nuevo
      (fecha_inicio_asignacion BETWEEN nueva_fecha_inicio AND nueva_fecha_fin)
  )
```

#### Caso 2: Nueva asignación sin fecha fin (indefinida)
```sql
-- Cualquier asignación que no haya terminado antes del inicio de la nueva
WHERE num_trabajador = ?
  AND activo_asignacion = 1
  AND (fecha_fin_asignacion >= nueva_fecha_inicio OR fecha_fin_asignacion IS NULL)
```

### Ejemplos

#### ✅ PERMITIDO - Sin traslape
```
Asignación 1: 2024-01-01 a 2024-06-30
Asignación 2: 2024-07-01 a 2024-12-31
```

#### ❌ RECHAZADO - Traslape parcial
```
Asignación 1: 2024-01-01 a 2024-08-31
Asignación 2: 2024-06-01 a 2024-12-31  # Se traslapa de junio a agosto
```

#### ❌ RECHAZADO - Traslape total
```
Asignación 1: 2024-01-01 a 2024-12-31
Asignación 2: 2024-06-01 a 2024-08-31  # Completamente contenida
```

#### ❌ RECHAZADO - Asignación indefinida
```
Asignación 1: 2024-01-01 a NULL (indefinido)
Asignación 2: 2024-06-01 a 2024-12-31  # Se traslapa porque la 1 nunca termina
```

#### ✅ PERMITIDO - Misma fecha de inicio/fin
```
Asignación 1: 2024-01-01 a 2024-06-30
Asignación 2: 2024-07-01 a 2024-12-31  # Comienza justo después
```

### Escenarios por Semestre

Aunque las asignaciones están etiquetadas por semestre, **la validación se hace solo por fechas**:

#### Escenario Válido
```
Semestre: AGOSTO_DICIEMBRE_2024
- Asignación 1: 2024-08-01 a 2024-10-31 (Plantilla A)
- Asignación 2: 2024-11-01 a 2024-12-31 (Plantilla B)
✅ PERMITIDO - Mismo semestre, diferentes rangos sin traslape
```

#### Escenario Inválido
```
Semestre: AGOSTO_DICIEMBRE_2024
- Asignación 1: 2024-08-01 a 2024-11-30 (Plantilla A)
- Asignación 2: 2024-10-01 a 2024-12-31 (Plantilla B)
❌ RECHAZADO - Mismo semestre, rangos se traslapan (octubre-noviembre)
```

#### Escenario Inválido (Diferentes semestres)
```
- Asignación 1: AGOSTO_DICIEMBRE_2024 → 2024-08-01 a 2025-01-31
- Asignación 2: ENERO_JUNIO_2025 → 2025-01-01 a 2025-06-30
❌ RECHAZADO - Diferentes semestres pero rangos se traslapan (enero 2025)
```

## Mensajes de Error

Cuando se detecta un traslape, el sistema retorna:

```
No se puede asignar el horario. El trabajador {num} ya tiene asignaciones 
que se traslapan con el rango de fechas solicitado ({inicio} - {fin}).

Asignaciones conflictivas:
ID 123: 2024-08-01 - 2024-11-30 (Semestre: AGOSTO_DICIEMBRE_2024)
ID 456: 2024-10-01 - Indefinido (Semestre: AGOSTO_DICIEMBRE_2024)
```

## Implementación

### Archivo
`/app/features/horarios/services/asignar_horario_trabajador_use_case.py`

### Flujo de Validación
1. ✅ Verificar que el trabajador existe
2. ✅ Verificar que la plantilla existe  
3. ✅ **VALIDAR que NO haya traslapes de fechas**
4. ✅ Insertar la asignación

### Uso en CSV Import
El caso de uso `importar_horarios_csv_use_case.py` utiliza internamente 
`asignar_horario_trabajador_use_case`, por lo que **automáticamente aplica 
todas las validaciones de traslape** durante la importación masiva.

## Base de Datos

### Tabla: horarios_trabajadores
```sql
CREATE TABLE horarios_trabajadores (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    num_trabajador INT UNSIGNED NOT NULL,
    plantilla_horario_id BIGINT UNSIGNED NOT NULL,
    fecha_inicio_asignacion DATE NOT NULL,
    fecha_fin_asignacion DATE,  -- NULL = indefinido
    semestre VARCHAR(50) NOT NULL,
    estado_asignacion VARCHAR(20) DEFAULT 'activo',
    activo_asignacion BOOLEAN DEFAULT 1,
    
    -- Índices para optimizar validación de traslapes
    INDEX idx_trabajador_semestre (num_trabajador, semestre),
    INDEX idx_fechas (fecha_inicio_asignacion, fecha_fin_asignacion)
);
```

### Índices Relevantes
- `idx_trabajador_semestre`: Optimiza búsquedas por trabajador
- `idx_fechas`: Acelera comparaciones de rangos de fechas
- `activo_asignacion`: Solo se validan asignaciones activas

## Consideraciones Especiales

1. **Asignaciones Inactivas**: Solo se validan traslapes con asignaciones donde `activo_asignacion = 1`

2. **Fecha Fin NULL**: Se interpreta como "indefinido" o "hasta el presente"

3. **Rendimiento**: Los índices compuestos aseguran que la validación sea rápida incluso con miles de asignaciones

4. **Atomicidad**: Cada asignación se valida individualmente durante importación CSV, permitiendo importaciones parcialmente exitosas
