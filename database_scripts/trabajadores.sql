-- ============================================
-- Script: Tabla trabajadores
-- Descripción: Almacena información de trabajadores (optimizado para consultas)
-- ============================================

CREATE TABLE IF NOT EXISTS trabajadores (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    num_trabajador INT UNSIGNED NOT NULL UNIQUE,
    nombre VARCHAR(255) NOT NULL,
    departamento VARCHAR(100),
    tipoPlaza VARCHAR(100),
    ingresoSEPfecha DATE,
    captura DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Índices para consultas eficientes
    INDEX idx_num_trabajador (num_trabajador),
    INDEX idx_nombre (nombre),
    INDEX idx_departamento (departamento),
    INDEX idx_tipoPlaza (tipoPlaza)
    
) ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Ejemplo de inserción
-- ============================================
-- INSERT INTO trabajadores (num_trabajador, nombre, departamento, tipoPlaza, ingresoSEPfecha, captura) 
-- VALUES (2, 'Juan Pérez', 'Recursos Humanos', 'Base', '2020-01-15', '2024-10-19');
