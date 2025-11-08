# Feature: Departamentos

## 📋 Descripción
Sistema completo de gestión de departamentos con CRUD, importación CSV y asignación a trabajadores.

## 🗂️ Estructura
```
app/features/departamentos/
├── __init__.py
├── services/
│   ├── crear_departamento_use_case.py
│   ├── listar_departamentos_use_case.py
│   ├── actualizar_departamento_use_case.py
│   ├── eliminar_departamento_use_case.py
│   └── importar_departamentos_csv_use_case.py
├── routes/
│   └── departamentos_routes.py
└── templates/
    └── departamentos/
        └── index.html
```

## 📊 Base de Datos

### Tabla: departamentos
```sql
CREATE TABLE departamentos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  num_departamento INT NOT NULL UNIQUE,
  nombre VARCHAR(255) NOT NULL,
  nomenclatura VARCHAR(50) DEFAULT '',
  activo BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Relación con trabajadores
```sql
ALTER TABLE trabajadores 
ADD COLUMN departamento_id INT,
ADD CONSTRAINT fk_trabajador_departamento 
    FOREIGN KEY (departamento_id) 
    REFERENCES departamentos(id);
```

## 🚀 Instalación

### 1. Ejecutar migración SQL
```bash
mysql -u root -p sistema < migrations/create_departamentos_table.sql
```

### 2. Asignar departamentos desde CSV existente
```bash
python asignar_departamentos.py
```

Este script:
- Lee el archivo `departamentos.csv`
- Crea automáticamente los departamentos
- Asigna cada trabajador a su departamento correspondiente

## 📝 Uso del Sistema

### CRUD Manual
1. Acceder a `/departamentos`
2. Crear, editar o eliminar departamentos
3. Filtrar por nombre, nomenclatura o estado

### Importación CSV
1. Click en "Importar CSV"
2. Descargar plantilla de ejemplo (opcional)
3. Subir archivo CSV con formato:
   ```csv
   num_departamento,nombre,nomenclatura,activo
   1,DIRECCIÓN GENERAL,DG,1
   2,RECURSOS HUMANOS,RH,1
   ```

### Formato CSV
- **num_departamento**: Número único del departamento
- **nombre**: Nombre completo del departamento
- **nomenclatura**: Siglas o código corto (ej: DG, RH, SA)
- **activo**: 1 (activo) o 0 (inactivo)

## 🔗 API Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/departamentos/` | Página principal |
| GET | `/departamentos/listar` | Lista departamentos (JSON) |
| POST | `/departamentos/crear` | Crea departamento |
| PUT | `/departamentos/editar/<id>` | Actualiza departamento |
| DELETE | `/departamentos/eliminar/<id>` | Elimina departamento |
| POST | `/departamentos/importar-csv` | Importa desde CSV |
| GET | `/departamentos/descargar-plantilla` | Descarga CSV ejemplo |

## 📌 Notas Importantes

### Validaciones
- El `num_departamento` debe ser único
- No se puede eliminar un departamento con trabajadores asignados
- Los campos `num_departamento` y `nombre` son obligatorios

### Nomenclatura
- Se genera automáticamente en el script `asignar_departamentos.py`
- Toma las primeras letras de cada palabra del nombre

### Relación con Trabajadores
- El campo `departamento` (texto) se mantiene para compatibilidad
- El campo `departamento_id` (FK) es la nueva relación
- Si se elimina un departamento, el `departamento_id` del trabajador se pone en NULL

## 🛠️ Modelo Trabajador Actualizado

```python
@dataclass
class Trabajador:
    num_trabajador: int
    nombre: str
    departamento: Optional[str] = None  # Legacy (texto)
    departamento_id: Optional[int] = None  # Nueva FK
    tipoPlaza: Optional[str] = None
    # ... otros campos
```

## 📦 Plantilla CSV de Ejemplo

El sistema incluye un endpoint para descargar una plantilla CSV con ejemplos:
- Click en "Descargar Plantilla" en el modal de importación
- Editar el archivo con tus departamentos
- Importar de vuelta al sistema

## ⚡ Script de Asignación

El script `asignar_departamentos.py`:
1. Lee `departamentos.csv` (formato especial con departamentos y trabajadores)
2. Crea departamentos automáticamente con nomenclatura
3. Asigna cada trabajador listado a su departamento
4. Muestra resumen con estadísticas y errores

Ejecutar con:
```bash
python asignar_departamentos.py
```

## 🎯 Casos de Uso

### Crear Departamento
```python
from app.features.departamentos.services.crear_departamento_use_case import crear_departamento_use_case
from app.shared.models.departamento import Departamento

departamento = Departamento(
    num_departamento=1,
    nombre="DIRECCIÓN GENERAL",
    nomenclatura="DG",
    activo=True
)

id_insertado, error = crear_departamento_use_case.ejecutar(departamento)
```

### Listar Departamentos
```python
from app.features.departamentos.services.listar_departamentos_use_case import listar_departamentos_use_case

departamentos, error = listar_departamentos_use_case.ejecutar(
    activo=True,  # Solo activos
    buscar="RECURSOS"  # Búsqueda en nombre/nomenclatura
)
```

### Importar desde CSV
```python
from app.features.departamentos.services.importar_departamentos_csv_use_case import importar_departamentos_csv_use_case

resultado, error = importar_departamentos_csv_use_case.ejecutar(archivo_csv)
# resultado contiene: total, insertados, duplicados, errores
```

## ✅ Testing

Para probar la feature:
1. Ejecutar migración SQL
2. Ejecutar script de asignación
3. Acceder a `/departamentos`
4. Verificar que se muestren los departamentos
5. Crear, editar y eliminar departamentos
6. Importar CSV de prueba
7. Verificar que trabajadores tengan `departamento_id` asignado
