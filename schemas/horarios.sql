-- ============================================
-- Script: Tablas de horarios
-- Descripción: Plantillas de horarios y asignaciones a trabajadores
-- ============================================

-- Tabla: plantillas_horarios
CREATE TABLE IF NOT EXISTS plantillas_horarios (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre_horario VARCHAR(255) NOT NULL,
    descripcion_horario TEXT,
    
    -- Lunes
    lunes_entrada_1 TIME,
    lunes_salida_1 TIME,
    lunes_entrada_2 TIME,
    lunes_salida_2 TIME,
    
    -- Martes
    martes_entrada_1 TIME,
    martes_salida_1 TIME,
    martes_entrada_2 TIME,
    martes_salida_2 TIME,
    
    -- Miércoles
    miercoles_entrada_1 TIME,
    miercoles_salida_1 TIME,
    miercoles_entrada_2 TIME,
    miercoles_salida_2 TIME,
    
    -- Jueves
    jueves_entrada_1 TIME,
    jueves_salida_1 TIME,
    jueves_entrada_2 TIME,
    jueves_salida_2 TIME,
    
    -- Viernes
    viernes_entrada_1 TIME,
    viernes_salida_1 TIME,
    viernes_entrada_2 TIME,
    viernes_salida_2 TIME,
    
    -- Sábado
    sabado_entrada_1 TIME,
    sabado_salida_1 TIME,
    sabado_entrada_2 TIME,
    sabado_salida_2 TIME,
    
    -- Domingo
    domingo_entrada_1 TIME,
    domingo_salida_1 TIME,
    domingo_entrada_2 TIME,
    domingo_salida_2 TIME,
    
    activo BOOLEAN DEFAULT 1,
    horario_hash VARCHAR(32) COMMENT 'MD5 hash de los horarios para detectar duplicados',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Índices
    INDEX idx_nombre_horario (nombre_horario),
    INDEX idx_activo (activo),
    UNIQUE INDEX idx_horario_hash (horario_hash)
    
) ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Plantillas reutilizables de horarios';


-- Tabla: horarios_trabajadores
CREATE TABLE IF NOT EXISTS horarios_trabajadores (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    num_trabajador INT UNSIGNED NOT NULL,
    plantilla_horario_id BIGINT UNSIGNED NOT NULL,
    fecha_inicio_asignacion DATE NOT NULL,
    fecha_fin_asignacion DATE,
    semestre VARCHAR(50) NOT NULL COMMENT 'Ej: AGOSTO_DICIEMBRE_2024',
    estado_asignacion VARCHAR(20) DEFAULT 'activo' COMMENT 'activo, finalizado, suspendido',
    activo_asignacion BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    CONSTRAINT fk_horario_trabajador 
        FOREIGN KEY (num_trabajador) 
        REFERENCES trabajadores(num_trabajador) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
        
    CONSTRAINT fk_horario_plantilla 
        FOREIGN KEY (plantilla_horario_id) 
        REFERENCES plantillas_horarios(id) 
        ON DELETE RESTRICT 
        ON UPDATE CASCADE,
    
    -- Índices
    INDEX idx_num_trabajador (num_trabajador),
    INDEX idx_plantilla_horario_id (plantilla_horario_id),
    INDEX idx_semestre (semestre),
    INDEX idx_estado_asignacion (estado_asignacion),
    INDEX idx_fechas (fecha_inicio_asignacion, fecha_fin_asignacion),
    INDEX idx_trabajador_semestre (num_trabajador, semestre)
    
) ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Asignación de horarios a trabajadores por periodo';
