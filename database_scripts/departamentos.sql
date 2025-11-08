-- Crear tabla departamentos
CREATE TABLE IF NOT EXISTS `departamentos` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `num_departamento` INT NOT NULL UNIQUE,
  `nombre` VARCHAR(255) NOT NULL,
  `nomenclatura` VARCHAR(50) DEFAULT '',
  `activo` BOOLEAN DEFAULT TRUE,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX `idx_num_departamento` (`num_departamento`),
  INDEX `idx_activo` (`activo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insertar departamento por defecto (SIN ASIGNAR)
INSERT INTO `departamentos` (`num_departamento`, `nombre`, `nomenclatura`, `activo`)
VALUES (0, 'SIN ASIGNAR', 'SA', 1)
ON DUPLICATE KEY UPDATE nombre = nombre;
