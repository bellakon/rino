-- ============================================
-- Script: Tablas de movimientos
-- Descripción: Catálogo de tipos de movimientos y movimientos aplicados a trabajadores
-- ============================================

-- Tabla: tipos_movimientos
CREATE TABLE IF NOT EXISTS tipos_movimientos (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nomenclatura VARCHAR(20) NOT NULL UNIQUE COMMENT 'Código alfanumérico único (COM001, LIC002, AH, etc.)',
    nombre VARCHAR(255) NOT NULL COMMENT 'Nombre descriptivo del tipo de movimiento',
    descripcion TEXT COMMENT 'Descripción detallada del movimiento',
    categoria VARCHAR(50) NOT NULL COMMENT 'Comisión, Licencia, Permiso, Autorización, Capacitación, Otros',
    letra CHAR(1) NOT NULL COMMENT 'Clasificación por letra: A, B, C, D, E, F, G',
    
    -- Configuración dinámica de campos personalizados (JSON)
    campos_personalizados JSON COMMENT 'Definición de campos adicionales que requiere este tipo de movimiento',
    -- Ejemplo: [
    --   {"nombre": "archivo_pdf", "tipo": "file", "requerido": true, "label": "Documento PDF"},
    --   {"nombre": "datos_consulta", "tipo": "text", "requerido": false, "label": "Datos de la consulta"},
    --   {"nombre": "folio", "tipo": "number", "requerido": true, "label": "Número de folio"}
    -- ]
    
    activo BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Índices
    INDEX idx_nomenclatura (nomenclatura),
    INDEX idx_categoria (categoria),
    INDEX idx_letra (letra),
    INDEX idx_activo (activo),
    INDEX idx_nombre (nombre)
    
) ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Catálogo maestro de tipos de movimientos';


-- Tabla: movimientos
CREATE TABLE IF NOT EXISTS movimientos (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    num_trabajador INT UNSIGNED NOT NULL COMMENT 'Número de trabajador (puede estar inactivo)',
    tipo_movimiento_id BIGINT UNSIGNED NOT NULL,
    fecha_inicio DATE NOT NULL COMMENT 'Fecha de inicio del movimiento',
    fecha_fin DATE NOT NULL COMMENT 'Fecha de fin del movimiento',
    observaciones TEXT COMMENT 'Justificación o motivo del movimiento',
    
    -- Datos personalizados según el tipo de movimiento (JSON)
    datos_personalizados JSON COMMENT 'Valores de los campos personalizados del tipo de movimiento',
    -- Ejemplo: {
    --   "archivo_pdf": "/uploads/movimientos/12345_documento.pdf",
    --   "datos_consulta": "Consulta médica general",
    --   "folio": "00123"
    -- }
    
    -- Auditoría
    usuario_registro VARCHAR(100) COMMENT 'Usuario que registró el movimiento',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    CONSTRAINT fk_movimiento_trabajador 
        FOREIGN KEY (num_trabajador) 
        REFERENCES trabajadores(num_trabajador) 
        ON DELETE RESTRICT 
        ON UPDATE CASCADE,
        
    CONSTRAINT fk_movimiento_tipo 
        FOREIGN KEY (tipo_movimiento_id) 
        REFERENCES tipos_movimientos(id) 
        ON DELETE RESTRICT 
        ON UPDATE CASCADE,
    
    -- Índices
    INDEX idx_num_trabajador (num_trabajador),
    INDEX idx_tipo_movimiento (tipo_movimiento_id),
    INDEX idx_fechas (fecha_inicio, fecha_fin),
    INDEX idx_trabajador_fechas (num_trabajador, fecha_inicio, fecha_fin),
    INDEX idx_created_at (created_at)
    
) ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Movimientos aplicados a trabajadores';


-- ============================================
-- Datos iniciales: Tipos de movimientos comunes
-- ============================================

INSERT INTO tipos_movimientos (nomenclatura, nombre, descripcion, categoria, letra, campos_personalizados, activo) VALUES
-- Comisiones
('COM001', 'Comisión Oficial', 'Comisión oficial con oficio', 'Comisión', 'A',
 '[{"nombre":"archivo_pdf","tipo":"file","requerido":true,"label":"Documento PDF del oficio"}]', 1),

('COM002', 'Comisión Sindical', 'Comisión por actividades sindicales', 'Comisión', 'B',
 '[{"nombre":"folio","tipo":"text","requerido":true,"label":"Número de folio"},{"nombre":"archivo_pdf","tipo":"file","requerido":false,"label":"Documento PDF"}]', 1),

-- Licencias
('LIC001', 'Licencia Médica', 'Licencia médica con incapacidad', 'Licencia', 'A',
 '[{"nombre":"datos_consulta","tipo":"textarea","requerido":true,"label":"Datos de la consulta médica"},{"nombre":"archivo_pdf","tipo":"file","requerido":true,"label":"Incapacidad médica (PDF)"},{"nombre":"folio_incapacidad","tipo":"text","requerido":true,"label":"Folio de incapacidad"}]', 1),

('LIC002', 'Licencia sin Goce de Sueldo', 'Licencia sin goce de sueldo', 'Licencia', 'C',
 '[{"nombre":"motivo","tipo":"textarea","requerido":true,"label":"Motivo de la licencia"},{"nombre":"archivo_pdf","tipo":"file","requerido":false,"label":"Documento de solicitud"}]', 1),

-- Permisos
('PER001', 'Permiso Económico', 'Permiso económico por horas', 'Permiso', 'B',
 '[{"nombre":"horas","tipo":"number","requerido":true,"label":"Número de horas"},{"nombre":"motivo","tipo":"text","requerido":true,"label":"Motivo del permiso"}]', 1),

('PER002', 'Permiso por Defunción', 'Permiso por fallecimiento de familiar', 'Permiso', 'A',
 '[{"nombre":"parentesco","tipo":"text","requerido":true,"label":"Parentesco con el difunto"},{"nombre":"archivo_pdf","tipo":"file","requerido":true,"label":"Acta de defunción"}]', 1),

-- Ausencias
('AH', 'Ausencia por Horas', 'Ausencia justificada por horas', 'Permiso', 'C',
 '[{"nombre":"horas","tipo":"number","requerido":true,"label":"Horas de ausencia"}]', 1),

('AF', 'Ausencia por Falta', 'Ausencia injustificada', 'Otros', 'E', NULL, 1),

-- Compensaciones
('CCM', 'Compensación de Comisión', 'Compensación de tiempo por comisión', 'Comisión', 'D', NULL, 1),

-- Maternidad/Lactancia
('LAC', 'Lactancia', 'Permiso de lactancia', 'Autorización', 'B',
 '[{"nombre":"horario","tipo":"text","requerido":true,"label":"Horario de lactancia"}]', 1),

-- Vacaciones
('VAC', 'Vacaciones', 'Período vacacional', 'Autorización', 'A',
 '[{"nombre":"dias_habiles","tipo":"number","requerido":true,"label":"Días hábiles"},{"nombre":"periodo","tipo":"text","requerido":true,"label":"Período que corresponde"}]', 1),

-- Capacitación
('CAP001', 'Capacitación Oficial', 'Curso o capacitación oficial', 'Capacitación', 'B',
 '[{"nombre":"nombre_curso","tipo":"text","requerido":true,"label":"Nombre del curso"},{"nombre":"institucion","tipo":"text","requerido":true,"label":"Institución"},{"nombre":"archivo_pdf","tipo":"file","requerido":false,"label":"Constancia o programa"}]', 1)

ON DUPLICATE KEY UPDATE nombre = nombre;


-- ============================================
-- Consultas útiles
-- ============================================

-- Ver todos los tipos de movimientos activos
-- SELECT id, nomenclatura, nombre, categoria, letra, activo FROM tipos_movimientos WHERE activo = 1 ORDER BY letra, categoria, nombre;

-- Ver movimientos de un trabajador
-- SELECT m.*, tm.nomenclatura, tm.nombre as tipo_nombre, t.nombre as trabajador_nombre 
-- FROM movimientos m
-- INNER JOIN tipos_movimientos tm ON m.tipo_movimiento_id = tm.id
-- INNER JOIN trabajadores t ON m.num_trabajador = t.num_trabajador
-- WHERE m.num_trabajador = ? ORDER BY m.fecha_inicio DESC;

-- Ver campos personalizados de un tipo de movimiento
-- SELECT nomenclatura, nombre, campos_personalizados FROM tipos_movimientos WHERE id = ?;
