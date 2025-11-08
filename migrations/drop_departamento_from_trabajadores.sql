-- Eliminar columna departamento (VARCHAR) de tabla trabajadores
-- Ejecutar DESPUÉS de haber migrado todos los datos a departamento_id

-- Verificar que departamento_id está poblado antes de eliminar departamento
-- SELECT COUNT(*) FROM trabajadores WHERE departamento_id IS NULL;

-- Eliminar columna departamento
ALTER TABLE trabajadores DROP COLUMN IF EXISTS departamento;

-- Verificación
SELECT 
    COLUMN_NAME, 
    DATA_TYPE, 
    IS_NULLABLE,
    COLUMN_KEY
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = DATABASE() 
  AND TABLE_NAME = 'trabajadores'
ORDER BY ORDINAL_POSITION;
