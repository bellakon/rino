# Feature: Horarios

## Estado Actual: ESTRUCTURA BÁSICA CREADA ✅

### Completado:
1. ✅ Estructura de carpetas completa
2. ✅ Archivo de configuración de semestres (`app/config/semestres.py`)
3. ✅ Modelo `PlantillaHorario` con método `generar_hash_horario()` para detectar duplicados
4. ✅ Modelo `HorarioTrabajador` para asignaciones
5. ✅ Script SQL de migración (`migrations/create_horarios_tables.sql`)

### Pendiente de Implementar:

#### Servicios (Casos de Uso):
- `crear_plantilla_horario_use_case.py` - Valida hash único antes de crear
- `listar_plantillas_horarios_use_case.py` - Lista plantillas con filtros
- `actualizar_plantilla_horario_use_case.py` - Actualiza plantilla
- `eliminar_plantilla_horario_use_case.py` - Valida que no esté asignada
- `asignar_horario_trabajador_use_case.py` - Asigna plantilla a trabajador
- `listar_horarios_trabajadores_use_case.py` - Lista asignaciones con JOIN
- `importar_horarios_csv_use_case.py` - Importa desde CSV

#### Rutas:
- `horarios_routes.py` - Blueprint con endpoints para CRUD y importación

#### Templates:
- `index.html` - Vista principal con tabs (Plantillas / Asignaciones)
- `modal_crear_plantilla.html` - Crear plantilla de horario
- `modal_editar_plantilla.html` - Editar plantilla
- `modal_eliminar_plantilla.html` - Confirmar eliminación
- `modal_asignar_horario.html` - Asignar horario a trabajador(es)
- `modal_importar_horarios.html` - Importar desde CSV

#### Otros:
- Registrar blueprint en `app/__init__.py`
- Agregar enlace en navbar (`base.html`)
- Agregar tarjeta en página principal (`index.html`)

### Estructura de Datos:

**Plantilla Horario:**
- Nombre y descripción
- Tolerancias de entrada/salida
- 7 días × 4 campos (entrada_1, salida_1, entrada_2, salida_2)
- Hash MD5 para detectar duplicados
- Estado activo/inactivo

**Horario Trabajador (Asignación):**
- num_trabajador (FK)
- plantilla_horario_id (FK)
- Fechas inicio/fin
- Semestre
- Estados: activo/inactivo

### Lógica de Negocio:

1. **Plantillas Únicas**: No puede haber dos plantillas con el mismo horario (mismo hash)
2. **Eliminación Restringida**: No se puede eliminar plantilla si está asignada (FK RESTRICT)
3. **Importación CSV**: 
   - Crea plantillas si no existen (por hash)
   - Valida que trabajador exista antes de asignar
   - Ignora trabajadores inexistentes

### Próximos Pasos Sugeridos:

1. Ejecutar migración SQL
2. Crear casos de uso básicos (crear, listar)
3. Crear rutas y blueprint
4. Crear template básico con tabs
5. Registrar en app
6. Implementar funcionalidad de importación CSV

### Ejemplo de Plantilla CSV:

```csv
id_trabajador,nombre_completo,departamento,nombre_horario,descripcion_horario,tolerancia_entrada,tolerancia_salida,lunes_entrada_1,lunes_salida_1,martes_entrada_1,martes_salida_1,...
1,Juan Pérez,Sistemas,Horario Administrativo,9am-5pm L-V,15,15,9:00,17:00,9:00,17:00,...
```

¿Deseas que continúe con alguna parte específica de la implementación?
