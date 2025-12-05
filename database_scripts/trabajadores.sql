-- ============================================
-- Script: Tabla trabajadores
-- Descripción: Almacena información de trabajadores (optimizado para consultas)
-- ============================================

CREATE TABLE IF NOT EXISTS trabajadores (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    num_trabajador INT UNSIGNED NOT NULL UNIQUE,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(100) DEFAULT NULL COMMENT 'Correo electrónico del trabajador',
    departamento_id INT DEFAULT 0,
    tipoPlaza VARCHAR(100) DEFAULT NULL,
    ingresoSEPfecha DATE DEFAULT NULL,
    captura DATE DEFAULT NULL,
    activo BOOLEAN DEFAULT 1,
    movimiento VARCHAR(100) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Índices para consultas eficientes
    INDEX idx_num_trabajador (num_trabajador),
    INDEX idx_nombre (nombre),
    INDEX idx_tipoPlaza (tipoPlaza),
    INDEX idx_activo (activo),
    INDEX fk_trabajador_departamento (departamento_id),
    
    -- Foreign Key a tabla departamentos
    CONSTRAINT fk_trabajador_departamento 
        FOREIGN KEY (departamento_id) 
        REFERENCES departamentos(id) 
        ON DELETE SET NULL 
        ON UPDATE CASCADE
    
) ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Ejemplo de inserción
-- ============================================
-- INSERT INTO trabajadores (num_trabajador, nombre, departamento_id, tipoPlaza, ingresoSEPfecha, captura) 
-- VALUES (2, 'Juan Pérez', 1, 'Base', '2020-01-15', '2024-10-19');
