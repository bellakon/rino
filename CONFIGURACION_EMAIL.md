# Configuración de Correo Electrónico

## ⚠️ ERROR COMÚN: Authentication unsuccessful, basic authentication is disabled

**Error completo:**
```
(535, b'5.7.139 Authentication unsuccessful, basic authentication is disabled.')
```

**Causa:** Microsoft/Outlook ha deshabilitado la autenticación básica (usuario/contraseña normal) por seguridad.

**Solución:** Usar una **Contraseña de Aplicación** en lugar de tu contraseña normal.

---

## 🔐 Cómo Generar una Contraseña de Aplicación

### Para cuentas de Outlook/Hotmail/Microsoft 365:

#### Paso 1: Habilitar verificación en dos pasos
1. Ve a: https://account.microsoft.com/security
2. Inicia sesión con tu cuenta
3. Busca **"Verificación en dos pasos"** o **"Opciones de seguridad avanzadas"**
4. Si no está activa, actívala (es requisito para contraseñas de aplicación)

#### Paso 2: Generar contraseña de aplicación
1. En la misma página de seguridad, busca **"Contraseñas de aplicación"** o **"App passwords"**
2. Haz clic en **"Crear nueva contraseña de aplicación"**
3. Dale un nombre descriptivo (ej: "Sistema RH Python")
4. Copia la contraseña generada (formato: `xxxx-xxxx-xxxx-xxxx`)
   - ⚠️ **Importante:** Esta contraseña solo se muestra una vez

#### Paso 3: Configurar en el sistema
1. Abre el archivo `.env` en la raíz del proyecto
2. Reemplaza `SMTP_PASSWORD` con la contraseña de aplicación generada:

```env
SMTP_USERNAME=tu_correo@outlook.com
SMTP_PASSWORD=abcd-efgh-ijkl-mnop    # ← Contraseña de aplicación (no tu contraseña normal)
SMTP_FROM_EMAIL=tu_correo@outlook.com
```

---

## 📧 Configuración Completa en .env

```env
# CONFIGURACIÓN SMTP PARA ENVÍO DE CORREOS
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USE_TLS=True
SMTP_USERNAME=tu_correo@outlook.com
SMTP_PASSWORD=xxxx-xxxx-xxxx-xxxx         # Contraseña de aplicación
SMTP_FROM_EMAIL=tu_correo@outlook.com
SMTP_FROM_NAME=Sistema de Recursos Humanos
```

---

## 🧪 Probar la Configuración

Ejecuta este script para verificar que todo funciona:

```bash
python -c "
from app.config.smtp_config import SMTP_CONFIG, validar_config
import smtplib

print('🔍 Validando configuración...')
es_valida, mensaje = validar_config()
print(f'   {mensaje}')

if es_valida:
    print('\n📧 Probando conexión SMTP...')
    try:
        servidor = smtplib.SMTP(SMTP_CONFIG['host'], SMTP_CONFIG['port'])
        servidor.starttls()
        servidor.login(SMTP_CONFIG['username'], SMTP_CONFIG['password'])
        print('   ✅ Conexión exitosa!')
        servidor.quit()
    except Exception as e:
        print(f'   ❌ Error: {e}')
"
```

---

## 🔧 Alternativas si No Puedes Usar Contraseñas de Aplicación

### Opción 1: Habilitar autenticación básica (NO RECOMENDADO)
Microsoft lo permite para cuentas empresariales con administrador, pero es menos seguro.

### Opción 2: Usar otro proveedor de correo

#### Gmail:
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=tu_correo@gmail.com
SMTP_PASSWORD=xxxx-xxxx-xxxx-xxxx    # También requiere contraseña de aplicación
```

**Generar contraseña de aplicación en Gmail:**
1. https://myaccount.google.com/security
2. Verificación en dos pasos → Activar
3. Contraseñas de aplicaciones → Generar

#### SendGrid (servicio especializado):
```env
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=tu_api_key_de_sendgrid
```

---

## 📝 Funcionalidad de Envío de Correos

### Bitácora de Asistencias

El sistema puede enviar automáticamente las bitácoras de asistencias por correo electrónico:

1. **Ubicación**: Modal de resultados del procesamiento masivo de bitácoras
2. **Botón**: "Enviar por Correo"
3. **Archivos adjuntos**:
   - PDF de la bitácora generada
   - `plantilla.pdf` con instrucciones de interpretación

### Requisitos

- El trabajador debe tener un **correo electrónico registrado** en el sistema
- Las credenciales SMTP deben estar configuradas en `.env`

### Contenido del Correo

**Asunto**: `Bitácora de Asistencias - [Nombre] ([Número])`

**Cuerpo**:
```
Estimado(a) [Nombre],

Adjunto encontrará su bitácora de asistencias del periodo:
📅 Fecha Inicio: [fecha]
📅 Fecha Fin: [fecha]
📊 Total de días procesados: [total]

Se incluyen dos archivos adjuntos:
1️⃣ Bitácora de Asistencias (PDF) - Su registro de asistencias completo
2️⃣ Guía de Interpretación (PDF) - Instrucciones para leer la bitácora

Si tiene alguna duda sobre los registros, por favor contacte al departamento de Recursos Humanos.

Atentamente,
Sistema de Recursos Humanos
```

---

## 👥 Gestión del Campo Email

### Agregar Email a Trabajadores

#### Crear nuevo trabajador
- Formulario incluye campo "Correo Electrónico" (opcional)
- Se muestra nota: "Requerido para envío de bitácoras por correo"

#### Editar trabajador existente
- Campo email disponible en el formulario de edición

#### Importar desde CSV
- La plantilla CSV incluye columna `email` (opcional)
- Descargar plantilla desde el modal de importación

**Formato de plantilla CSV**:
```csv
num,nombre,email
65,MOLINA GÓMEZ KEVIN DAVID,kevin.molina@ejemplo.com
70,GARCÍA LÓPEZ MARÍA FERNANDA,maria.garcia@ejemplo.com
```

---

## 🐛 Solución de Problemas

### Error: "El trabajador no tiene correo electrónico registrado"
**Solución**: Agregar email al trabajador desde el formulario de edición o importación

### Error de autenticación SMTP (535)
**Causa**: Contraseña incorrecta o autenticación básica deshabilitada  
**Solución**: Usar contraseña de aplicación (ver sección principal de este documento)

### Error de encoding
El sistema maneja automáticamente caracteres especiales (ñ, acentos) usando UTF-8.

---

## ❓ Preguntas Frecuentes

**P: ¿Por qué no funciona mi contraseña normal?**  
R: Microsoft deshabilitó la autenticación básica por seguridad. Debes usar contraseñas de aplicación.

**P: ¿Es seguro usar contraseñas de aplicación?**  
R: Sí, son más seguras porque:
- Tienen permisos limitados
- Puedes revocarlas sin cambiar tu contraseña principal
- Se usan solo para esta aplicación específica

**P: ¿Puedo usar varios servicios con la misma contraseña de aplicación?**  
R: Sí, pero es mejor generar una contraseña diferente para cada aplicación.

**P: ¿Qué hago si pierdo la contraseña de aplicación?**  
R: Simplemente genera una nueva y actualiza el `.env`. La anterior dejará de funcionar.

---

## ✅ Checklist de Configuración

- [ ] Cuenta de Outlook/Microsoft configurada
- [ ] Verificación en dos pasos activada
- [ ] Contraseña de aplicación generada
- [ ] Archivo `.env` actualizado con la contraseña de aplicación
- [ ] Prueba de conexión ejecutada exitosamente
- [ ] Envío de correo de prueba funcionando

---

## 📁 Archivos Relacionados

- **Configuración**: `/app/config/smtp_config.py`
- **Plantillas**: `/app/config/email_templates.py`
- **Caso de uso**: `/app/features/bitacora/services/enviar_correo_bitacora_use_case.py`
- **Plantilla PDF**: `/plantilla.pdf`
- **Plantilla CSV**: `/app/static/plantilla_trabajadores.csv`

---

**Última actualización:** 21 de noviembre de 2025
