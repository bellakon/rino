# Sistema de Gestión de Checadores ZKTeco 🕐

Sistema completo para gestionar dispositivos ZKTeco, asistencias, trabajadores, departamentos, horarios y movimientos.

## ¿Qué puedo hacer?

✅ **Checadores**: Conectar dispositivos ZKTeco y descargar registros  
✅ **Asistencias**: Ver entrada/salida de empleados (sincronizado con checadores)  
✅ **Trabajadores**: CRUD + importar masivo desde CSV  
✅ **Departamentos**: CRUD + importar masivo desde CSV  
✅ **Horarios**: Crear plantillas y asignarlas a trabajadores  
✅ **Movimientos**: Licencias, permisos, vacaciones, ausencias, capacitación  
✅ **Migración**: Enviar datos a RinoTime

---

## 🚀 Inicio Rápido

```bash
# 1. Configurar variables de entorno
cp .env.example .env
# Editar: DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

# 2. Crear base de datos
mysql -u root -p < database_scripts/init_schema.sql

# 3. Activar entorno virtual
source .venv/bin/activate

# 4. Instalar dependencias (si es primera vez)
pip install -r requirements.txt

# 5. Ejecutar la aplicación
python main.py
```

🌐 Abre en el navegador: **http://localhost:5000**

---

## 📁 Estructura del Proyecto

```
rino/
├── app/
│   ├── config/                      # ⚙️ CONFIGURACIONES
│   │   ├── database_config.py       # Conexión MySQL
│   │   ├── checadores_config.py     # 👉 IPs de dispositivos ZKTeco
│   │   └── movimientos_config.py    # 👉 Letras para tipos de movimientos
│   │
│   ├── core/
│   │   └── database/
│   │       ├── connection.py        # Conexión singleton a MySQL
│   │       ├── query_executor.py    # Ejecuta queries SQL
│   │       └── query_builder.py     # Construye queries dinámicas
│   │
│   ├── features/                    # 🎯 FEATURES (por dominio)
│   │   ├── checadores/
│   │   ├── asistencias/
│   │   ├── trabajadores/
│   │   ├── departamentos/
│   │   ├── horarios/
│   │   ├── movimientos/
│   │   └── migrar_datos/
│   │
│   ├── shared/
│   │   └── templates/base.html      # 📄 Template base (NO BORRAR)
│   │
│   └── __init__.py                  # 👉 Registra blueprints aquí
│
├── database_scripts/                # 📜 Scripts SQL iniciales
├── main.py                          # 🚀 Inicia la app
├── requirements.txt                 # Dependencias Python
├── .env.example                     # Plantilla de variables
└── README.md
```

---

## 🎯 Estructura de Cada Feature

Cada feature sigue el mismo patrón (Clean Architecture):

```
feature/
├── models/          # Clases de datos + validaciones
├── services/        # Casos de uso (lógica de negocio)
├── routes/          # Endpoints REST (Flask blueprints)
└── templates/       # HTML + JavaScript del frontend
    ├── index.html               # Página principal
    ├── modal_tipo_X.html        # Modales para crear/editar
    └── modal_importar_csv.html  # Modal para importación CSV
```

**Nota**: Cada operación es un caso de uso independiente:
- `listar_X_use_case.py` - Obtener todos/filtrados
- `crear_X_use_case.py` - Insertar nuevo
- `obtener_X_use_case.py` - Obtener uno por ID
- `editar_X_use_case.py` - Actualizar
- `eliminar_X_use_case.py` - Borrar/desactivar

---

## ⚙️ Configuraciones Importantes

### 1️⃣ Dispositivos ZKTeco (Checadores)
📍 Archivo: `app/config/checadores_config.py`

```python
CHECADORES = [
    {
        'id': 'principal',
        'nombre': 'Entrada Principal',
        'ip': '192.168.1.201',      # 👈 Cambiar IP del dispositivo
        'puerto': 4370,
        'ubicacion': 'Puerta de entrada',
        'activo': True
    }
]
```

### 2️⃣ Letras de Movimientos
📍 Archivo: `app/config/movimientos_config.py`

Define qué letras (A, B, C...) están permitidas en tipos de movimientos.

### 3️⃣ Conexión a Base de Datos
📍 Archivo: `.env`

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=contraseña123
DB_NAME=asistencias
MYSQL_PORT=3306
```

### 2️⃣ Base de Datos
📍 `.env`

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=contraseña123
DB_NAME=asistencias
MYSQL_PORT=3306
```

### 3️⃣ Letras de Movimientos
📍 `app/config/movimientos_config.py`

Controla qué letras (A, B, C...) puedes usar en tipos de movimientos.

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología |
|-----------|-----------|
| **Backend** | Flask 3.0 |
| **Base de Datos** | MySQL 8.0+ |
| **Drivers** | pymysql 1.1.0, pyzk 0.9.1 |
| **Frontend** | Bootstrap 5.3 + JavaScript Vanilla |
| **Python** | 3.9+ |

---

## 📂 Dónde Editar por Tarea

| Necesito... | Editar aquí |
|-----------|-----------|
| Agregar un checador | `app/config/checadores_config.py` |
| Cambiar credenciales BD | `.env` |
| Permitir nueva letra de movimiento | `app/config/movimientos_config.py` |
| Crear nuevo CRUD en trabajadores | `app/features/trabajadores/services/` |
| Crear nuevo CRUD en departamentos | `app/features/departamentos/services/` |
| Cambiar cómo se ve la página | `app/features/*/templates/` |
| Agregar nuevo endpoint | `app/features/*/routes/` |
| Modificar base de datos | `database_scripts/` |

---

## 🔄 Patrones Clave del Proyecto

### QueryExecutor - Ejecuta SQL
```python
from app.core.database.query_executor import QueryExecutor
from app.core.database.connection import db_connection

executor = QueryExecutor(db_connection)
resultados, error = executor.ejecutar("SELECT * FROM trabajadores", ())

if error:
    print(f"Error: {error}")
else:
    for row in resultados:
        print(row)
```

### QueryBuilder - Construye SQL dinámico
```python
from app.core.database.query_builder import QueryBuilder

builder = QueryBuilder("SELECT * FROM trabajadores")
builder.add_filter("departamento_id", 5)
builder.add_filter("activo", 1)
query, params = builder.build()
# Resultado: SELECT * FROM trabajadores WHERE departamento_id = %s AND activo = %s
# Parámetros: (5, 1)
```

### Casos de Uso - Estructura estándar
```python
from app.core.database.query_executor import QueryExecutor
from app.core.database.connection import db_connection

class MiCasoUsoUseCase:
    def __init__(self):
        self.query_executor = QueryExecutor(db_connection)
    
    def ejecutar(self, parametro):
        # Lógica aquí
        query = "SELECT * FROM mi_tabla WHERE id = %s"
        resultado, error = self.query_executor.ejecutar(query, (parametro,))
        
        if error:
            return None, error
        return resultado, None

# Instancia global (singleton)
mi_caso_uso_use_case = MiCasoUsoUseCase()
```

### Frontend - Cargar datos dinámicamente
```javascript
// Ejemplo: Cargar lista de trabajadores
fetch('/trabajadores/listar')
    .then(response => response.json())
    .then(data => {
        console.log(data.trabajadores);
        // Procesar y mostrar datos
    })
    .catch(error => console.error('Error:', error));
```

---

## � Troubleshooting Rápido

| Problema | Solución |
|---------|----------|
| "cannot import name 'get_connection'" | Usa `db_connection` en lugar de `get_connection()` |
| La tabla no muestra datos | Abre consola del navegador (F12), busca errores en Network |
| Error CORS o 404 en endpoint | Verifica que el blueprint esté registrado en `app/__init__.py` |
| Checador no conecta | Revisa IP y puerto en `app/config/checadores_config.py` |
| Base de datos no sincroniza | Verifica credenciales en `.env` |
| JavaScript no ejecuta | Usa `{% block extra_js %}` no `{% block scripts %}` |
| Botón de modal no funciona | Verifica que el modal esté incluido con `{% include %}` |
| Error "No module named 'X'" | Instala dependencias: `pip install -r requirements.txt` |

---

## 📝 Notas Importantes

🔴 **NO hagas esto:**
- No elimines `app/shared/templates/base.html` - todos los features lo necesitan
- No cambies el nombre de `db_connection` - se usa en todo el proyecto
- No uses `{% block scripts %}` - usa `{% block extra_js %}`

✅ **Haz esto siempre:**
- Cuando registres un nuevo blueprint, hazlo en `app/__init__.py`
- Usa QueryBuilder para filtros dinámicos en SELECT
- Cada caso de uso tiene su propio archivo
- Los modales van en archivos separados (modal_X.html)
- Importa modales en index.html con `{% include %}`

💡 **Recuerda:**
- Las rutas del backend usan `/feature/ruta` (ej: `/trabajadores/listar`)
- Los endpoints retornan JSON
- El frontend hace fetch para obtener datos
- QueryBuilder construye WHERE con AND (no OR)

---

## 🎓 Próximos Pasos

1. Familiarízate con la estructura ejecutando la app
2. Crea algunos trabajadores y departamentos
3. Asigna horarios
4. Crea tipos de movimientos
5. Crea movimientos
6. Conecta un checador y descarga asistencias
7. Prueba la migración a RinoTime
