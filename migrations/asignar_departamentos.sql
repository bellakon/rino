-- =====================================================
-- Script de Asignación de Departamentos
-- Generado automáticamente desde: departamentos.csv
-- =====================================================

-- =====================================================
-- 1. CREAR DEPARTAMENTOS (si no existen)
-- =====================================================

-- Departamento: SUBDIRECCIÓN ADMINISTRATIVA
INSERT INTO `departamentos` (`num_departamento`, `nombre`, `nomenclatura`, `activo`)
VALUES (2, 'SUBDIRECCIÓN ADMINISTRATIVA', 'SA', 1)
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), nomenclatura = VALUES(nomenclatura);

-- Departamento: CENTRO DE CÓMPUTO
INSERT INTO `departamentos` (`num_departamento`, `nombre`, `nomenclatura`, `activo`)
VALUES (3, 'CENTRO DE CÓMPUTO', 'CDC', 1)
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), nomenclatura = VALUES(nomenclatura);

-- Departamento: MANTENIMIENTO Y EQUIPO
INSERT INTO `departamentos` (`num_departamento`, `nombre`, `nomenclatura`, `activo`)
VALUES (4, 'MANTENIMIENTO Y EQUIPO', 'MYE', 1)
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), nomenclatura = VALUES(nomenclatura);

-- Departamento: RECURSOS  FINANCIEROS
INSERT INTO `departamentos` (`num_departamento`, `nombre`, `nomenclatura`, `activo`)
VALUES (5, 'RECURSOS  FINANCIEROS', 'RF', 1)
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), nomenclatura = VALUES(nomenclatura);

-- Departamento: HUGO HERNÁNDEZ  SEVILLA
INSERT INTO `departamentos` (`num_departamento`, `nombre`, `nomenclatura`, `activo`)
VALUES (6, 'HUGO HERNÁNDEZ  SEVILLA', 'HHS', 1)
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), nomenclatura = VALUES(nomenclatura);

-- Departamento: CARLOS DANIEL CRUZ LANDEROS
INSERT INTO `departamentos` (`num_departamento`, `nombre`, `nomenclatura`, `activo`)
VALUES (7, 'CARLOS DANIEL CRUZ LANDEROS', 'CDCL', 1)
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), nomenclatura = VALUES(nomenclatura);

-- Departamento: RECURSOS HUMANOS
INSERT INTO `departamentos` (`num_departamento`, `nombre`, `nomenclatura`, `activo`)
VALUES (8, 'RECURSOS HUMANOS', 'RH', 1)
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), nomenclatura = VALUES(nomenclatura);

-- Departamento: RECURSOS MATERIALES Y DE SERVICIOS
INSERT INTO `departamentos` (`num_departamento`, `nombre`, `nomenclatura`, `activo`)
VALUES (9, 'RECURSOS MATERIALES Y DE SERVICIOS', 'RMYDS', 1)
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), nomenclatura = VALUES(nomenclatura);

-- Departamento: DIRECCIÓN
INSERT INTO `departamentos` (`num_departamento`, `nombre`, `nomenclatura`, `activo`)
VALUES (10, 'DIRECCIÓN', 'DIR', 1)
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), nomenclatura = VALUES(nomenclatura);

-- Departamento: SUBDIRECCIÓN DE PLANEACIÓN Y VINCULACIÓN
INSERT INTO `departamentos` (`num_departamento`, `nombre`, `nomenclatura`, `activo`)
VALUES (11, 'SUBDIRECCIÓN DE PLANEACIÓN Y VINCULACIÓN', 'SDPYV', 1)
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), nomenclatura = VALUES(nomenclatura);

-- Departamento: ACTIVIDADES EXTRAESCOARES
INSERT INTO `departamentos` (`num_departamento`, `nombre`, `nomenclatura`, `activo`)
VALUES (12, 'ACTIVIDADES EXTRAESCOARES', 'AE', 1)
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), nomenclatura = VALUES(nomenclatura);

-- Departamento: CENTRO DE INFORMACIÓN
INSERT INTO `departamentos` (`num_departamento`, `nombre`, `nomenclatura`, `activo`)
VALUES (13, 'CENTRO DE INFORMACIÓN', 'CDI', 1)
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), nomenclatura = VALUES(nomenclatura);

-- Departamento: COMUNICACIÓN Y DIFUSIÓN
INSERT INTO `departamentos` (`num_departamento`, `nombre`, `nomenclatura`, `activo`)
VALUES (14, 'COMUNICACIÓN Y DIFUSIÓN', 'CYD', 1)
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), nomenclatura = VALUES(nomenclatura);

-- Departamento: GESTIÓN TECNOLÓGICO Y VINCULACIÓN
INSERT INTO `departamentos` (`num_departamento`, `nombre`, `nomenclatura`, `activo`)
VALUES (15, 'GESTIÓN TECNOLÓGICO Y VINCULACIÓN', 'GTYV', 1)
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), nomenclatura = VALUES(nomenclatura);

-- Departamento: PLANEACIÓN, PROGRAMACIÓN Y PRESUPUESTACIÓN
INSERT INTO `departamentos` (`num_departamento`, `nombre`, `nomenclatura`, `activo`)
VALUES (16, 'PLANEACIÓN, PROGRAMACIÓN Y PRESUPUESTACIÓN', 'PPYP', 1)
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), nomenclatura = VALUES(nomenclatura);

-- Departamento: SERVICIOS ESCOLARES
INSERT INTO `departamentos` (`num_departamento`, `nombre`, `nomenclatura`, `activo`)
VALUES (17, 'SERVICIOS ESCOLARES', 'SE', 1)
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), nomenclatura = VALUES(nomenclatura);

-- Departamento: SUB  ACADÉMICA
INSERT INTO `departamentos` (`num_departamento`, `nombre`, `nomenclatura`, `activo`)
VALUES (18, 'SUB  ACADÉMICA', 'SA', 1)
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), nomenclatura = VALUES(nomenclatura);

-- Departamento: DESARROLLO ACADÉMICO
INSERT INTO `departamentos` (`num_departamento`, `nombre`, `nomenclatura`, `activo`)
VALUES (19, 'DESARROLLO ACADÉMICO', 'DA', 1)
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), nomenclatura = VALUES(nomenclatura);

-- Departamento: DIVISIÓN DE ESTUDIOS DEPOSGRADO
INSERT INTO `departamentos` (`num_departamento`, `nombre`, `nomenclatura`, `activo`)
VALUES (20, 'DIVISIÓN DE ESTUDIOS DEPOSGRADO', 'DDED', 1)
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), nomenclatura = VALUES(nomenclatura);

-- Departamento: DIVISIÓN DE ESTUDIOS PROFESIONALES
INSERT INTO `departamentos` (`num_departamento`, `nombre`, `nomenclatura`, `activo`)
VALUES (21, 'DIVISIÓN DE ESTUDIOS PROFESIONALES', 'DDEP', 1)
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), nomenclatura = VALUES(nomenclatura);

-- Departamento: ELECTROMÉCANICA
INSERT INTO `departamentos` (`num_departamento`, `nombre`, `nomenclatura`, `activo`)
VALUES (22, 'ELECTROMÉCANICA', 'ELE', 1)
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), nomenclatura = VALUES(nomenclatura);

-- Departamento: ELECTRICA
INSERT INTO `departamentos` (`num_departamento`, `nombre`, `nomenclatura`, `activo`)
VALUES (23, 'ELECTRICA', 'ELE', 1)
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), nomenclatura = VALUES(nomenclatura);

-- Departamento: ING EN SISTEMAS Y COMPUTACIÓN
INSERT INTO `departamentos` (`num_departamento`, `nombre`, `nomenclatura`, `activo`)
VALUES (24, 'ING EN SISTEMAS Y COMPUTACIÓN', 'IESYC', 1)
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), nomenclatura = VALUES(nomenclatura);

-- Departamento: ING INDUSTRIAL
INSERT INTO `departamentos` (`num_departamento`, `nombre`, `nomenclatura`, `activo`)
VALUES (25, 'ING INDUSTRIAL', 'II', 1)
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), nomenclatura = VALUES(nomenclatura);

-- Departamento: SUB DIRECCIÓN ACADÉMICA
INSERT INTO `departamentos` (`num_departamento`, `nombre`, `nomenclatura`, `activo`)
VALUES (26, 'SUB DIRECCIÓN ACADÉMICA', 'SDA', 1)
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), nomenclatura = VALUES(nomenclatura);

-- Departamento: LOBATO FRANCO JESÚS ANTONIO
INSERT INTO `departamentos` (`num_departamento`, `nombre`, `nomenclatura`, `activo`)
VALUES (27, 'LOBATO FRANCO JESÚS ANTONIO', 'LFJA', 1)
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), nomenclatura = VALUES(nomenclatura);

-- Departamento: QQQQaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
INSERT INTO `departamentos` (`num_departamento`, `nombre`, `nomenclatura`, `activo`)
VALUES (28, 'QQQQaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'QQQ', 1)
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), nomenclatura = VALUES(nomenclatura);

-- Departamento: CCS ECONÓMADMTVAS
INSERT INTO `departamentos` (`num_departamento`, `nombre`, `nomenclatura`, `activo`)
VALUES (29, 'CCS ECONÓMADMTVAS', 'CE', 1)
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), nomenclatura = VALUES(nomenclatura);

-- Departamento: CIENCIAS BÁSICAS
INSERT INTO `departamentos` (`num_departamento`, `nombre`, `nomenclatura`, `activo`)
VALUES (30, 'CIENCIAS BÁSICAS', 'CB', 1)
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), nomenclatura = VALUES(nomenclatura);


-- =====================================================
-- 2. ASIGNAR DEPARTAMENTOS A TRABAJADORES DEL CSV (330 trabajadores)
-- =====================================================

-- Asignar a: CENTRO DE CÓMPUTO (num_departamento 3)
UPDATE `trabajadores` t
INNER JOIN `departamentos` d ON d.num_departamento = 3
SET t.`departamento_id` = d.`id`
WHERE t.`num_trabajador` IN (392, 48, 65, 81, 134, 145, 374, 103);

-- Asignar a: MANTENIMIENTO Y EQUIPO (num_departamento 4)
UPDATE `trabajadores` t
INNER JOIN `departamentos` d ON d.num_departamento = 4
SET t.`departamento_id` = d.`id`
WHERE t.`num_trabajador` IN (27, 50, 157, 178, 194, 266, 304, 329);

-- Asignar a: CARLOS DANIEL CRUZ LANDEROS (num_departamento 7)
UPDATE `trabajadores` t
INNER JOIN `departamentos` d ON d.num_departamento = 7
SET t.`departamento_id` = d.`id`
WHERE t.`num_trabajador` IN (38, 97, 104, 328);

-- Asignar a: RECURSOS HUMANOS (num_departamento 8)
UPDATE `trabajadores` t
INNER JOIN `departamentos` d ON d.num_departamento = 8
SET t.`departamento_id` = d.`id`
WHERE t.`num_trabajador` IN (318, 36, 51, 147, 159, 212, 232, 377, 425, 428);

-- Asignar a: RECURSOS MATERIALES Y DE SERVICIOS (num_departamento 9)
UPDATE `trabajadores` t
INNER JOIN `departamentos` d ON d.num_departamento = 9
SET t.`departamento_id` = d.`id`
WHERE t.`num_trabajador` IN (322, 427, 247, 21, 25, 32, 52, 53, 60, 72, 77, 80, 84, 113, 115, 160, 161, 168, 174, 181, 189, 204, 213, 240, 245, 320, 321, 401);

-- Asignar a: DIRECCIÓN (num_departamento 10)
UPDATE `trabajadores` t
INNER JOIN `departamentos` d ON d.num_departamento = 10
SET t.`departamento_id` = d.`id`
WHERE t.`num_trabajador` IN (1, 116);

-- Asignar a: SUBDIRECCIÓN DE PLANEACIÓN Y VINCULACIÓN (num_departamento 11)
UPDATE `trabajadores` t
INNER JOIN `departamentos` d ON d.num_departamento = 11
SET t.`departamento_id` = d.`id`
WHERE t.`num_trabajador` IN (8, 312, 416);

-- Asignar a: ACTIVIDADES EXTRAESCOARES (num_departamento 12)
UPDATE `trabajadores` t
INNER JOIN `departamentos` d ON d.num_departamento = 12
SET t.`departamento_id` = d.`id`
WHERE t.`num_trabajador` IN (362, 417, 95, 132, 201, 55, 381, 389);

-- Asignar a: CENTRO DE INFORMACIÓN (num_departamento 13)
UPDATE `trabajadores` t
INNER JOIN `departamentos` d ON d.num_departamento = 13
SET t.`departamento_id` = d.`id`
WHERE t.`num_trabajador` IN (302, 28, 86, 148, 234, 127, 290);

-- Asignar a: COMUNICACIÓN Y DIFUSIÓN (num_departamento 14)
UPDATE `trabajadores` t
INNER JOIN `departamentos` d ON d.num_departamento = 14
SET t.`departamento_id` = d.`id`
WHERE t.`num_trabajador` IN (358, 118);

-- Asignar a: GESTIÓN TECNOLÓGICO Y VINCULACIÓN (num_departamento 15)
UPDATE `trabajadores` t
INNER JOIN `departamentos` d ON d.num_departamento = 15
SET t.`departamento_id` = d.`id`
WHERE t.`num_trabajador` IN (179, 231, 244, 214, 267);

-- Asignar a: PLANEACIÓN, PROGRAMACIÓN Y PRESUPUESTACIÓN (num_departamento 16)
UPDATE `trabajadores` t
INNER JOIN `departamentos` d ON d.num_departamento = 16
SET t.`departamento_id` = d.`id`
WHERE t.`num_trabajador` IN (144, 195, 44, 372);

-- Asignar a: SERVICIOS ESCOLARES (num_departamento 17)
UPDATE `trabajadores` t
INNER JOIN `departamentos` d ON d.num_departamento = 17
SET t.`departamento_id` = d.`id`
WHERE t.`num_trabajador` IN (205, 340, 13, 85, 149, 246, 227, 225, 135, 271, 31);

-- Asignar a: DESARROLLO ACADÉMICO (num_departamento 19)
UPDATE `trabajadores` t
INNER JOIN `departamentos` d ON d.num_departamento = 19
SET t.`departamento_id` = d.`id`
WHERE t.`num_trabajador` IN (307, 47, 102, 126, 185, 283);

-- Asignar a: DIVISIÓN DE ESTUDIOS DEPOSGRADO (num_departamento 20)
UPDATE `trabajadores` t
INNER JOIN `departamentos` d ON d.num_departamento = 20
SET t.`departamento_id` = d.`id`
WHERE t.`num_trabajador` IN (348, 339);

-- Asignar a: DIVISIÓN DE ESTUDIOS PROFESIONALES (num_departamento 21)
UPDATE `trabajadores` t
INNER JOIN `departamentos` d ON d.num_departamento = 21
SET t.`departamento_id` = d.`id`
WHERE t.`num_trabajador` IN (130, 209, 151, 198, 90, 380, 202, 196, 327, 343, 373, 22, 325);

-- Asignar a: ELECTROMÉCANICA (num_departamento 22)
UPDATE `trabajadores` t
INNER JOIN `departamentos` d ON d.num_departamento = 22
SET t.`departamento_id` = d.`id`
WHERE t.`num_trabajador` IN (422, 3, 29, 37, 41, 42, 43, 64, 66, 140, 188, 238, 248, 249, 291, 293, 299, 300, 319, 337, 351, 391, 424);

-- Asignar a: ELECTRICA (num_departamento 23)
UPDATE `trabajadores` t
INNER JOIN `departamentos` d ON d.num_departamento = 23
SET t.`departamento_id` = d.`id`
WHERE t.`num_trabajador` IN (359, 33, 45, 39, 23, 107, 382, 123, 119, 152, 139, 58, 313, 162, 17, 228, 253, 369, 279, 106, 281, 34, 334, 336);

-- Asignar a: ING EN SISTEMAS Y COMPUTACIÓN (num_departamento 24)
UPDATE `trabajadores` t
INNER JOIN `departamentos` d ON d.num_departamento = 24
SET t.`departamento_id` = d.`id`
WHERE t.`num_trabajador` IN (10, 91, 131, 164, 190, 255, 264, 270, 272, 285, 294, 324, 331, 368);

-- Asignar a: ING INDUSTRIAL (num_departamento 25)
UPDATE `trabajadores` t
INNER JOIN `departamentos` d ON d.num_departamento = 25
SET t.`departamento_id` = d.`id`
WHERE t.`num_trabajador` IN (4, 9, 15, 30, 40, 49, 56, 75, 94, 110, 120, 137, 146, 170, 183, 220, 251, 256, 258, 295, 296, 332, 346, 353, 366, 375, 378, 387, 388, 390);

-- Asignar a: LOBATO FRANCO JESÚS ANTONIO (num_departamento 27)
UPDATE `trabajadores` t
INNER JOIN `departamentos` d ON d.num_departamento = 27
SET t.`departamento_id` = d.`id`
WHERE t.`num_trabajador` IN (74, 12);

-- Asignar a: QQQQaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa (num_departamento 28)
UPDATE `trabajadores` t
INNER JOIN `departamentos` d ON d.num_departamento = 28
SET t.`departamento_id` = d.`id`
WHERE t.`num_trabajador` IN (73, 11, 46, 59, 62, 63, 67, 76, 83, 129, 155, 166, 169, 197, 206, 207, 215, 221, 224, 239, 241, 254, 262, 268, 273, 274, 280, 309, 310, 341, 345, 370, 393);

-- Asignar a: CCS ECONÓMADMTVAS (num_departamento 29)
UPDATE `trabajadores` t
INNER JOIN `departamentos` d ON d.num_departamento = 29
SET t.`departamento_id` = d.`id`
WHERE t.`num_trabajador` IN (5, 24, 26, 35, 61, 71, 82, 93, 98, 101, 108, 111, 114, 167, 171, 177, 184, 192, 203, 223, 229, 233, 260, 278, 284, 303, 316, 317, 349, 354, 356, 383, 384, 385, 394, 409, 410, 415, 418, 419, 422);

-- Asignar a: CIENCIAS BÁSICAS (num_departamento 30)
UPDATE `trabajadores` t
INNER JOIN `departamentos` d ON d.num_departamento = 30
SET t.`departamento_id` = d.`id`
WHERE t.`num_trabajador` IN (6, 7, 14, 16, 18, 67, 69, 70, 79, 87, 88, 92, 96, 98, 100, 105, 122, 153, 172, 175, 186, 193, 222, 235, 250, 261, 311, 314, 316, 350, 352, 364, 371, 376, 379, 386, 403, 404, 406, 412, 414, 420);


-- =====================================================
-- 3. ASIGNAR 'SIN ASIGNAR' A TRABAJADORES NO LISTADOS
-- =====================================================

-- Todos los trabajadores que NO están en el CSV se asignan a departamento_id = 1 (SIN ASIGNAR)
UPDATE `trabajadores`
SET `departamento_id` = 1
WHERE `num_trabajador` NOT IN (1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 55, 56, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 69, 70, 71, 72, 73, 74, 75, 76, 77, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 90, 91, 92, 93, 94, 95, 96, 97, 98, 100, 101, 102, 103, 104, 105, 106, 107, 108, 110, 111, 113, 114, 115, 116, 118, 119, 120, 122, 123, 126, 127, 129, 130, 131, 132, 134, 135, 137, 139, 140, 144, 145, 146, 147, 148, 149, 151, 152, 153, 155, 157, 159, 160, 161, 162, 164, 166, 167, 168, 169, 170, 171, 172, 174, 175, 177, 178, 179, 181, 183, 184, 185, 186, 188, 189, 190, 192, 193, 194, 195, 196, 197, 198, 201, 202, 203, 204, 205, 206, 207, 209, 212, 213, 214, 215, 220, 221, 222, 223, 224, 225, 227, 228, 229, 231, 232, 233, 234, 235, 238, 239, 240, 241, 244, 245, 246, 247, 248, 249, 250, 251, 253, 254, 255, 256, 258, 260, 261, 262, 264, 266, 267, 268, 270, 271, 272, 273, 274, 278, 279, 280, 281, 283, 284, 285, 290, 291, 293, 294, 295, 296, 299, 300, 302, 303, 304, 307, 309, 310, 311, 312, 313, 314, 316, 317, 318, 319, 320, 321, 322, 324, 325, 327, 328, 329, 331, 332, 334, 336, 337, 339, 340, 341, 343, 345, 346, 348, 349, 350, 351, 352, 353, 354, 356, 358, 359, 362, 364, 366, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 401, 403, 404, 406, 409, 410, 412, 414, 415, 416, 417, 418, 419, 420, 422, 424, 425, 427, 428);


-- =====================================================
-- 4. VERIFICACIÓN (ejecutar después para revisar)
-- =====================================================

-- Ver resumen de asignaciones
SELECT 
    d.num_departamento,
    d.nombre,
    d.nomenclatura,
    COUNT(t.id) as total_trabajadores
FROM departamentos d
LEFT JOIN trabajadores t ON t.departamento_id = d.id
GROUP BY d.id
ORDER BY d.num_departamento;

-- Ver trabajadores sin departamento
SELECT num_trabajador, nombre
FROM trabajadores
WHERE departamento_id IS NULL;
