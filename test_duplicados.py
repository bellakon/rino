"""
Script de prueba: Insertar registros duplicados en RinoTime
Verifica que el sistema ignore duplicados correctamente
"""
from app.core.database.query_executor import QueryExecutor
from app.core.database.connection import db_sync_connection
from datetime import datetime

# Crear ejecutor para la BD de RinoTime
query_executor_sync = QueryExecutor(db_sync_connection)

# Registro de prueba
emp_code_test = '998'  # Número de trabajador de prueba
punch_time_test = '2025-11-08 12:00:00.000000'
terminal_sn_test = 'CLN5204760269'

print("=" * 60)
print("PRUEBA DE DUPLICADOS EN RINOTIME")
print("=" * 60)

# Query INSERT
insert_query = """
    INSERT INTO iclock_transaction (
        emp_code,
        punch_time,
        punch_state,
        verify_type,
        work_code,
        terminal_sn,
        terminal_alias,
        area_alias,
        longitude,
        latitude,
        gps_location,
        mobile,
        source,
        purpose,
        crc,
        is_attendance,
        reserved,
        upload_time,
        sync_status,
        sync_time,
        emp_id,
        terminal_id,
        is_mask,
        temperature
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s
    )
"""

# Parámetros del registro de prueba
params = (
    emp_code_test,                          # emp_code
    punch_time_test,                        # punch_time
    '255',                                  # punch_state
    25,                                     # verify_type
    '',                                     # work_code
    terminal_sn_test,                       # terminal_sn
    'Edificio ACB',                         # terminal_alias
    'Minatitlan',                          # area_alias
    None,                                   # longitude
    None,                                   # latitude
    None,                                   # gps_location
    None,                                   # mobile
    1,                                      # source
    9,                                      # purpose
    'AAIAAACAAAIAAAFABAJA',                # crc
    None,                                   # is_attendance
    None,                                   # reserved
    datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),  # upload_time
    None,                                   # sync_status
    None,                                   # sync_time
    None,                                   # emp_id
    3,                                      # terminal_id
    255,                                    # is_mask
    255.0                                   # temperature
)

print(f"\nRegistro de prueba:")
print(f"  emp_code: {emp_code_test}")
print(f"  punch_time: {punch_time_test}")
print(f"  terminal_sn: {terminal_sn_test}")

# Primera inserción
print("\n[1] Primera inserción...")
params_list = [params]
insertadas, error = query_executor_sync.ejecutar_batch(
    insert_query,
    params_list,
    ignore_duplicates=True
)

if error:
    print(f"    ❌ Error: {error}")
else:
    print(f"    ✅ Insertadas: {insertadas}")
    print(f"    📊 Duplicadas: {len(params_list) - insertadas}")

# Segunda inserción (mismo registro)
print("\n[2] Segunda inserción (duplicado)...")
insertadas2, error2 = query_executor_sync.ejecutar_batch(
    insert_query,
    params_list,
    ignore_duplicates=True
)

if error2:
    print(f"    ❌ Error: {error2}")
else:
    print(f"    ✅ Insertadas: {insertadas2}")
    print(f"    📊 Duplicadas: {len(params_list) - insertadas2}")

# Tercera inserción (mismo registro de nuevo)
print("\n[3] Tercera inserción (duplicado)...")
insertadas3, error3 = query_executor_sync.ejecutar_batch(
    insert_query,
    params_list,
    ignore_duplicates=True
)

if error3:
    print(f"    ❌ Error: {error3}")
else:
    print(f"    ✅ Insertadas: {insertadas3}")
    print(f"    📊 Duplicadas: {len(params_list) - insertadas3}")

print("\n" + "=" * 60)
print("RESUMEN:")
print("=" * 60)
print(f"Total intentos de inserción: 3")
print(f"Primera vez - Insertadas: {insertadas if not error else 0}")
print(f"Segunda vez - Insertadas: {insertadas2 if not error2 else 0} (debería ser 0)")
print(f"Tercera vez - Insertadas: {insertadas3 if not error3 else 0} (debería ser 0)")
print("\n✅ Si la segunda y tercera son 0, el anti-duplicados funciona correctamente")

# Verificar que existe el registro
print("\n" + "=" * 60)
print("VERIFICACIÓN EN BASE DE DATOS:")
print("=" * 60)

query_verificar = """
    SELECT COUNT(*) as total 
    FROM iclock_transaction 
    WHERE emp_code = %s 
    AND punch_time = %s 
    AND terminal_sn = %s
"""

resultado, error_ver = query_executor_sync.ejecutar(
    query_verificar, 
    (emp_code_test, punch_time_test, terminal_sn_test)
)

if error_ver:
    print(f"❌ Error al verificar: {error_ver}")
else:
    total = resultado[0]['total'] if resultado else 0
    print(f"Registros en BD con estos datos: {total}")
    if total == 1:
        print("✅ PERFECTO: Solo hay 1 registro (no se duplicó)")
    elif total > 1:
        print("⚠️ ADVERTENCIA: Hay más de 1 registro (se duplicó)")
    else:
        print("❌ ERROR: No se encontró el registro")

print("\n" + "=" * 60)
