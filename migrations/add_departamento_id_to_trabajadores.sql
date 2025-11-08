-- =====================================================
-- Script: Agregar columna departamento_id a trabajadores
-- Descripción: Agrega la FK a la tabla departamentos
-- =====================================================

-- Agregar columna departamento_id
ALTER TABLE `trabajadores` 
ADD COLUMN `departamento_id` INT DEFAULT NULL AFTER `departamento`;

-- Crear FK hacia departamentos
ALTER TABLE `trabajadores` 
ADD CONSTRAINT `fk_trabajador_departamento` 
    FOREIGN KEY (`departamento_id`) 
    REFERENCES `departamentos`(`id`) 
    ON DELETE SET NULL 
    ON UPDATE CASCADE;

-- Crear índice para mejorar performance
CREATE INDEX `idx_departamento_id` ON `trabajadores`(`departamento_id`);
