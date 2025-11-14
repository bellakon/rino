-- ============================================
-- Script: Tabla de bitácora de asistencias
-- Descripción: Registro procesado de asistencias con cálculo de incidencias
-- ============================================

-- Tabla: bitacora
CREATE TABLE IF NOT EXISTS bitacora (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    num_trabajador INT UNSIGNED NOT NULL COMMENT 'Número de trabajador',
    departamento VARCHAR(255) COMMENT 'Nombre del departamento',
    nombre_trabajador VARCHAR(255) NOT NULL COMMENT 'Nombre completo del trabajador',
    fecha DATE NOT NULL COMMENT 'Fecha del registro',
    
    -- Horario asignado
    turno_id BIGINT UNSIGNED COMMENT 'ID de la plantilla de horario asignada',
    horario_texto VARCHAR(50) COMMENT 'Horario en formato texto: 08:00-16:00',
    
    -- Códigos de incidencia
    codigo_incidencia CHAR(2) NOT NULL COMMENT 'A=Asistencia, F=Falta, R+=Retardo Mayor, R-=Retardo Menor, O=Omisión, ST=Salida Temprana, J=Justificado, L=Licencia',
    tipo_movimiento VARCHAR(50) COMMENT 'Tipo de movimiento si tiene justificación: COM, LIC, PER, etc.',
    movimiento_id BIGINT UNSIGNED COMMENT 'ID del movimiento de justificación/licencia',
    
    -- Checadas del día
    checada1 TIME COMMENT 'Entrada 1',
    checada2 TIME COMMENT 'Salida 1',
    checada3 TIME COMMENT 'Entrada 2 (para horarios mixtos)',
    checada4 TIME COMMENT 'Salida 2 (para horarios mixtos)',
    
    -- Cálculos
    minutos_retardo INT DEFAULT 0 COMMENT 'Minutos de retardo calculados',
    horas_trabajadas DECIMAL(5,2) DEFAULT 0.00 COMMENT 'Horas trabajadas en el día',
    descripcion_incidencia TEXT COMMENT 'Descripción detallada de la incidencia',
    
    -- Auditoría
    fecha_procesamiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Cuándo se procesó este registro',
    procesado_por VARCHAR(100) COMMENT 'Usuario que procesó la bitácora',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    CONSTRAINT fk_bitacora_trabajador 
        FOREIGN KEY (num_trabajador) 
        REFERENCES trabajadores(num_trabajador) 
        ON DELETE RESTRICT 
        ON UPDATE CASCADE,
        
    CONSTRAINT fk_bitacora_turno 
        FOREIGN KEY (turno_id) 
        REFERENCES plantillas_horarios(id) 
        ON DELETE SET NULL 
        ON UPDATE CASCADE,
        
    CONSTRAINT fk_bitacora_movimiento 
        FOREIGN KEY (movimiento_id) 
        REFERENCES movimientos(id) 
        ON DELETE SET NULL 
        ON UPDATE CASCADE,
    
    -- Índices para búsquedas rápidas
    INDEX idx_num_trabajador (num_trabajador),
    INDEX idx_fecha (fecha),
    INDEX idx_trabajador_fecha (num_trabajador, fecha),
    INDEX idx_codigo_incidencia (codigo_incidencia),
    INDEX idx_fecha_procesamiento (fecha_procesamiento),
    UNIQUE KEY uk_trabajador_fecha (num_trabajador, fecha)
    
) ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Bitácora procesada de asistencias con incidencias calculadas';


-- ============================================
-- Consultas útiles
-- ============================================

-- Ver bitácora de un trabajador en un rango de fechas
-- SELECT * FROM bitacora 
-- WHERE num_trabajador = ? 
-- AND fecha BETWEEN '2025-11-10' AND '2025-11-14'
-- ORDER BY fecha;

-- Contar incidencias por tipo
-- SELECT codigo_incidencia, COUNT(*) as total 
-- FROM bitacora 
-- WHERE num_trabajador = ? 
-- GROUP BY codigo_incidencia;

-- Ver retardos mayores del mes
-- SELECT * FROM bitacora 
-- WHERE codigo_incidencia = 'R+' 
-- AND MONTH(fecha) = MONTH(CURDATE())
-- ORDER BY fecha DESC;

-- Ver faltas sin justificar
-- SELECT * FROM bitacora 
-- WHERE codigo_incidencia = 'F' 
-- AND movimiento_id IS NULL
-- ORDER BY fecha DESC;
