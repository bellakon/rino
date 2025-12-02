# AI Coding Agent Instructions - TecnoTime/Rino

## Architecture Overview

This is a **Flask 3.0 web application** for managing ZKTeco biometric devices, employee attendance, departments, schedules, and employee movements (licenses, permits, etc.). The project follows **Clean Architecture** organized by **feature domains** (not layers).

**Key architectural patterns:**
- **Feature-based modules**: Each domain (trabajadores, asistencias, checadores, etc.) is self-contained in `app/features/`
- **Use case pattern**: Business logic isolated in `services/*_use_case.py` files (one file per operation)
- **Database abstraction**: Three core components handle all data access (see below)
- **Dual database support**: `db_connection` (main system) and `db_sync_connection` (RinoTime sync)
- **Singleton pattern**: Use cases and database executors are instantiated as singletons at module level

## Database Layer (Critical)

**ALWAYS use these three components** - never write raw SQL in routes:

### 1. `QueryExecutor` - Execute SQL queries
```python
from app.core.database.query_executor import query_executor
from app.core.database.connection import db_connection

# SELECT example
resultados, error = query_executor.ejecutar(
    "SELECT * FROM trabajadores WHERE activo = %s", 
    (1,)
)

# INSERT/UPDATE/DELETE example  
resultado, error = query_executor.ejecutar(
    "INSERT INTO trabajadores (num_trabajador, nombre) VALUES (%s, %s)",
    (123, "Juan Pérez")
)
# Returns: {'affected_rows': 1}, None

# Batch insert with duplicate handling
registros_insertados, error = query_executor.ejecutar_batch(
    "INSERT INTO trabajadores (num_trabajador, nombre) VALUES (%s, %s)",
    [(123, "Juan"), (456, "María")],
    ignore_duplicates=True  # Continues on IntegrityError
)
```

**For sync database**, use `query_executor_sync`:
```python
from app.core.database.query_executor import query_executor_sync
```

### 2. `QueryBuilder` - Build dynamic queries
```python
from app.core.database.query_builder import QueryBuilder

builder = QueryBuilder("SELECT * FROM trabajadores")
builder.add_filter("departamento_id", departamento_id)  # Only adds if not None
builder.add_filter("activo", 1)
builder.add_date_filter("created_at", fecha_desde, fecha_hasta)
builder.add_search(["nombre", "email"], search_term)  # OR across columns
builder.add_order_by("nombre", "ASC")
builder.add_limit(50, offset=100)

query, params = builder.build()
resultados, error = query_executor.ejecutar(query, params)
```

### 3. `DatabaseConnection` - Context manager
```python
from app.core.database.connection import db_connection

with db_connection.get_connection() as conn:
    with conn.cursor(DictCursor) as cursor:
        cursor.execute(query, params)
        # Connection commits automatically on success, rolls back on exception
```

**Important**: Use `db_connection` (singleton instance), NOT `get_connection()` function.

## Feature Structure Pattern

Every feature follows this exact structure:
```
app/features/{feature_name}/
├── models/              # Dataclasses with to_dict/from_dict
│   └── {entity}.py
├── services/            # Business logic - ONE use case per file
│   ├── crear_{entity}_use_case.py
│   ├── obtener_{entity}_use_case.py
│   ├── listar_{entity}s_use_case.py
│   ├── actualizar_{entity}_use_case.py
│   └── eliminar_{entity}_use_case.py
├── routes/              # Flask blueprints - thin controllers
│   └── {entity}_routes.py
└── templates/           # Feature-specific HTML
    └── {feature}/
        ├── index.html
        ├── modal_crear_{entity}.html
        └── modal_editar_{entity}.html
```

**Use case singleton pattern** (always use this):
```python
class MiUseCase:
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(self, param1, param2):
        query = "SELECT * FROM tabla WHERE id = %s"
        resultado, error = self.query_executor.ejecutar(query, (param1,))
        
        if error:
            return None, error
        return resultado, None

# Singleton instance at module level
mi_use_case = MiUseCase()
```

**Routes pattern** (thin controllers):
```python
from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from app.features.{feature}.services.mi_use_case import mi_use_case

{feature}_bp = Blueprint('{feature}', __name__, url_prefix='/{feature}')

@{feature}_bp.route('/')
def index():
    resultado, error = mi_use_case.ejecutar()
    if error:
        flash(f'Error: {error}', 'error')
    return render_template('{feature}/index.html', datos=resultado)
```

## Configuration Files

**Checadores (ZKTeco devices)**: `app/config/checadores_config.py`
```python
CHECADORES = [
    {
        'id': 'principal',
        'nombre': 'Entrada Principal',
        'ip': '192.168.1.201',      # Edit IP here
        'puerto': 4370,
        'ubicacion': 'Building A',
        'activo': True
    }
]
```

**Database connections**: `.env` file (never commit!)
```env
# Main system database
DB_SISTEMA_HOST=localhost
DB_SISTEMA_PORT=3306
DB_SISTEMA_USER=root
DB_SISTEMA_PASSWORD=secret
DB_SISTEMA_NAME=asistencias

# Sync database (RinoTime)
DB_SYNC_HOST=localhost
DB_SYNC_PORT=3306
DB_SYNC_USER=root
DB_SYNC_PASSWORD=secret
DB_SYNC_NAME=checadas_sync
```

**Movement types config**: `app/config/movimientos_config.py` - defines allowed letters (A, B, C, etc.) for movement types.

## Frontend Patterns

**Template inheritance** - ALWAYS use:
```html
{% extends "base.html" %}

{% block title %}Mi Feature{% endblock %}

{% block content %}
<!-- Your content -->
{% endblock %}

{% block extra_js %}
<script>
    // Your JavaScript - runs after base.html loads Bootstrap & jQuery
</script>
{% endblock %}
```

**CRITICAL**: Use `{% block extra_js %}` NOT `{% block scripts %}` (won't work).

**Including modals**:
```html
{% include 'mi_feature/modal_crear.html' %}
{% include 'mi_feature/modal_editar.html' %}
```

**Fetch API pattern** (frontend → backend):
```javascript
fetch('/trabajadores/listar?activo=true')
    .then(response => response.json())
    .then(data => {
        console.log(data.trabajadores);
        // Update UI
    })
    .catch(error => console.error('Error:', error));
```

## Adding New Features

1. **Create feature directory structure** in `app/features/new_feature/`
2. **Create models** with dataclasses (see `app/features/trabajadores/models/trabajador.py`)
3. **Create use cases** in `services/` (one per operation)
4. **Create routes** (Flask blueprint) 
5. **Register blueprint** in `app/__init__.py`:
   ```python
   from app.features.new_feature.routes.routes import new_feature_bp
   app.register_blueprint(new_feature_bp)
   ```
6. **Add template folder** to `app/__init__.py` jinja loader:
   ```python
   os.path.join(base_dir, 'features/new_feature/templates'),
   ```

## Running the Application

**Development**:
```bash
source .venv/bin/activate
python main.py
# Runs on http://0.0.0.0:5000
```

**Production** (systemd service):
```bash
sudo systemctl start tecnotime
sudo systemctl status tecnotime
sudo journalctl -u tecnotime -f  # View logs
```

Service uses **Gunicorn** with 4 workers, see `tecnotime.service`.

## Common Pitfalls

❌ **Don't do this:**
- Write SQL queries directly in routes (use use cases)
- Use `get_connection()` as a function (use `db_connection` singleton)
- Delete or rename `app/shared/templates/base.html` (all features need it)
- Use `{% block scripts %}` in templates (use `{% block extra_js %}`)
- Forget to register new blueprints in `app/__init__.py`
- Hardcode database credentials (use `.env`)

✅ **Do this:**
- Always use `QueryExecutor` for database operations
- Use `QueryBuilder` for dynamic filters
- Create singleton use case instances at module level
- Return `(result, error)` tuple from use cases
- Keep routes thin - move logic to use cases
- Use `flash()` for user messages in web routes
- Return JSON in API routes: `jsonify({'data': result})`

## Dependencies

Core stack (see `requirements.txt`):
- **Flask 3.0** - Web framework
- **pymysql 1.1.0** - MySQL driver (use DictCursor for dict results)
- **pyzk 0.9.1** - ZKTeco device communication
- **python-dotenv 1.0.0** - Environment variable management
- **reportlab** - PDF generation (for reports)

## Data Models

Models use **dataclasses** with helper methods:
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class MiModelo:
    id: Optional[int] = None
    nombre: str = ""
    
    def to_dict(self):
        return {'id': self.id, 'nombre': self.nombre}
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(id=data.get('id'), nombre=data.get('nombre'))
```

## CSV Import Pattern

All imports use `ejecutar_batch` with `ignore_duplicates=True`:
```python
trabajadores_lista = [
    {'num_trabajador': 123, 'nombre': 'Juan', 'activo': 1},
    # ...
]

query = "INSERT INTO trabajadores (num_trabajador, nombre, activo) VALUES (%(num_trabajador)s, %(nombre)s, %(activo)s)"

registros_insertados, error = query_executor.ejecutar_batch(
    query,
    trabajadores_lista,
    ignore_duplicates=True  # Skips duplicates instead of failing
)
```

Handle BOM in CSV files:
```python
contenido = archivo.stream.read()
texto = contenido.decode("utf-8-sig")  # Handles UTF-8 BOM
stream = io.StringIO(texto, newline=None)
csv_reader = csv.DictReader(stream)
```

## URL Patterns

- Feature routes: `/{feature}/` (e.g., `/trabajadores/`, `/asistencias/`)
- API endpoints: `/{feature}/listar`, `/{feature}/crear`, etc.
- All endpoints return JSON for AJAX calls
- Use `url_prefix` in blueprints to avoid repeating route base

## Debugging

**Common issues:**
- "cannot import name 'get_connection'" → Use `db_connection` singleton
- Table doesn't show data → Check browser console (F12) Network tab
- 404 on endpoint → Verify blueprint registered in `app/__init__.py`
- Checador won't connect → Check IP/port in `app/config/checadores_config.py`
- Modal not working → Ensure modal HTML is included with `{% include %}`

**Enable debug mode**: Set `DEBUG=True` in `.env`
