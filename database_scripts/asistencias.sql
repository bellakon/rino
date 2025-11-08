-- ============================================
-- Script: Tabla asistencias
-- Descripción: Almacena registros de checadas (optimizado para millones de registros)
-- ============================================

CREATE TABLE IF NOT EXISTS asistencias (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    num_trabajador INT UNSIGNED NOT NULL,
    nombre VARCHAR(255) DEFAULT NULL COMMENT 'Nombre del trabajador obtenido del checador',
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    checador VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Índices compuestos optimizados para consultas frecuentes
    INDEX idx_trabajador_fecha (num_trabajador, fecha),
    INDEX idx_fecha_hora (fecha, hora),
    INDEX idx_checador_fecha (checador, fecha),
    INDEX idx_nombre (nombre),
    
    -- Prevenir duplicados exactos (mismo trabajador, misma fecha/hora, mismo checador)
    UNIQUE KEY uk_asistencia_unica (num_trabajador, fecha, hora, checador)
    
) ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci
  ROW_FORMAT=COMPRESSED
  KEY_BLOCK_SIZE=8;

-- ============================================
-- Particionamiento por fecha (recomendado para millones de registros)
-- Descomenta si necesitas particionamiento por año
-- ============================================
/*
ALTER TABLE asistencias
PARTITION BY RANGE (YEAR(fecha)) (
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION p2026 VALUES LESS THAN (2027),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
*/

-- ============================================
-- Ejemplo de inserción
-- ============================================
-- INSERT INTO asistencias (num_trabajador, nombre, fecha, hora, checador) 
-- VALUES (2, 'JUAN PEREZ', '2024-10-19', '16:45', 'CHK002')
-- ON DUPLICATE KEY UPDATE created_at = CURRENT_TIMESTAMP;
