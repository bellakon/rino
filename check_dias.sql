-- Verificar por qué no aparecen los días 22 y 23 de octubre para trabajador 65

-- 1. Checadas en esas fechas
SELECT '=== CHECADAS 22-23 OCTUBRE ===' as info;
SELECT fecha, hora 
FROM asistencias 
WHERE num_trabajador = 65 
AND fecha IN ('2024-10-22', '2024-10-23') 
ORDER BY fecha, hora;

-- 2. Movimientos que cubran esas fechas
SELECT '=== MOVIMIENTOS 22-23 OCTUBRE ===' as info;
SELECT m.fecha_inicio, m.fecha_fin, tm.nomenclatura, tm.nombre, tm.letra 
FROM movimientos m 
INNER JOIN tipos_movimientos tm ON m.tipo_movimiento_id = tm.id 
WHERE m.num_trabajador = 65 
AND (
    (m.fecha_inicio <= '2024-10-22' AND m.fecha_fin >= '2024-10-22') OR
    (m.fecha_inicio <= '2024-10-23' AND m.fecha_fin >= '2024-10-23')
);

-- 3. Horario asignado
SELECT '=== HORARIO ASIGNADO ===' as info;
SELECT 
    ha.fecha_inicio, 
    ha.fecha_fin, 
    hp.nombre,
    hp.lunes_entrada_1, hp.lunes_salida_1,
    hp.martes_entrada_1, hp.martes_salida_1,
    hp.miercoles_entrada_1, hp.miercoles_salida_1
FROM horarios_asignados ha
INNER JOIN horarios_plantillas hp ON ha.horario_plantilla_id = hp.id
WHERE ha.num_trabajador = 65
AND ha.fecha_inicio <= '2024-10-23'
AND (ha.fecha_fin IS NULL OR ha.fecha_fin >= '2024-10-22');

-- 4. Registros existentes en bitácora
SELECT '=== REGISTROS EN BITACORA ===' as info;
SELECT fecha, codigo_incidencia, tipo_movimiento, descripcion_incidencia
FROM bitacora
WHERE num_trabajador = 65
AND fecha IN ('2024-10-22', '2024-10-23')
ORDER BY fecha;

-- Nota: 22 Oct 2024 = Martes, 23 Oct 2024 = Miércoles
