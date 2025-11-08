# Sistema de Checadores ZKTeco

Sistema Flask modular para gestionar checadores de asistencia ZKTeco.

## 📁 Estructura

```
rino/
├── app/
│   ├── config/                 # Configuraciones
│   │   ├── app_config.py      # Flask
│   │   ├── database_config.py # Base de datos
│   │   └── checadores_config.py # ⭐ Editar IPs aquí
│   │
│   ├── features/              # Features por dominio
│   │   ├── checadores/        # Gestión de dispositivos
│   │   │   ├── services/
│   │   │   ├── routes/
│   │   │   └── templates/
│   │   └── asistencias/       # Gestión de registros
│   │       ├── services/
│   │       ├── routes/
│   │       └── templates/
│   │
│   ├── core/                  # Funcionalidad compartida
│   │   └── database/
│   │
│   └── shared/                # Recursos compartidos
│       └── templates/
│
├── main.py                    # Punto de entrada
├── requirements.txt
├── .env.example
└── schema.sql                 # ⭐ Script de creación de BD

```

## 🚀 Inicio Rápido

```bash
# 1. Configurar entorno
cp .env.example .env
# Editar .env con tus datos

# 2. Crear base de datos
mysql -u root -p < schema.sql

# 3. Instalar dependencias (ya instaladas en .venv)
# source .venv/bin/activate
# pip install -r requirements.txt

# 4. Configurar checadores
# Editar: app/config/checadores_config.py

# 5. Iniciar aplicación
python main.py
```

Accede en: http://localhost:5000

## ⚙️ Configuración

### Agregar Checadores
📍 `app/config/checadores_config.py`

```python
CHECADORES = [
    {
        'id': 'principal',
        'nombre': 'Checador Principal',
        'ip': '192.168.1.201',
        'puerto': 4370,
        'ubicacion': 'Entrada',
        'activo': True
    }
]
```

### Base de Datos
📍 `.env`

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=asistencias
```

## 🎯 Características

- ✅ Consultar asistencias de checadores ZKTeco
- ✅ Guardar registros en MySQL
- ✅ Ejecutar queries SQL personalizadas
- ✅ Arquitectura modular por features
- ✅ Sin código duplicado
- ✅ Clean Code

## 📂 Dónde Editar

| Tarea | Archivo |
|-------|---------|
| Agregar checadores | `app/config/checadores_config.py` |
| Config BD | `app/config/database_config.py` o `.env` |
| Nueva funcionalidad checadores | `app/features/checadores/services/` |
| Nueva funcionalidad asistencias | `app/features/asistencias/services/` |

## 🛠️ Stack Tecnológico

- **Backend:** Flask 3.0
- **Checadores:** pyzk 0.9.1
- **Base de Datos:** MySQL (pymysql 1.1.0)
- **Frontend:** Bootstrap 5.3
