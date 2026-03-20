# 🚀 GUÍA RÁPIDA: Configurar GYM_APP en Oracle 21C

## Resumen de Pasos

```
┌─────────────────────────────────────────────────────┐
│  CONFIGURACIÓN INICIAL - Esquema GYM_APP            │
└─────────────────────────────────────────────────────┘

1. Verificar Oracle 21C | ✓ Instalado y ejecutándose
2. Descargar SQL Dev   | ✓ Extraer archivo ZIP
3. Iniciar SQL Dev     | ✓ Crear acceso directo
4. Conexión SYSDBA     | ✓ Test conexión
5. Crear esquema       | ✓ Ejecutar 00_create_schema.sql
6. Conexión GYM_APP    | ✓ Test conexión
7. Crear tablas        | ✓ Ejecutar 01_create_tables.sql
8. Crear procedimientos| ✓ Ejecutar 02_create_procedures.sql
9. Verificar objetos   | ✓ Ejecutar queries_example.sql
10. Actualizar Django  | ✓ Configurar settings.py
```

---

## Pre-requisitos

- [ ] Oracle Database 21C instalado y ejecutándose
- [ ] Puerto 1521 disponible (listener Oracle)
- [ ] Java JDK 11+ instalado
- [ ] 500 MB espacio libre
- [ ] Usuario SYS con contraseña conocida

**Verificar Oracle activo:**
```bash
ps aux | grep -i oracle
# Debe mostrar procesos de Oracle ejecutándose

netstat -tlnp | grep 1521
# Debe mostrar listener en puerto 1521
```

---

## 📋 CHECKLIST DE CONFIGURACIÓN

### PASO 1: Descargar SQL Developer

- [ ] Ir a: https://www.oracle.com/database/sqldeveloper/download/
- [ ] Descargar: `sqldeveloper-23.1.0-no-jdk.zip`
- [ ] Extraer archivo ZIP
- [ ] Ir a carpeta extraída
- [ ] Ejecutar: `./sqldeveloper/sqldeveloper.sh`

```bash
# Comando rápido:
cd ~ && \
wget https://download.oracle.com/otn/java/sqldeveloper/sqldeveloper-23.1.0.087.1900-no-jdk.zip && \
unzip sqldeveloper-23.1.0.087.1900-no-jdk.zip && \
./sqldeveloper/sqldeveloper.sh &
```

---

### PASO 2: Crear Conexión SYSDBA

En SQL Developer:

**1. Ir a:** Connections → New Connection

**2. Completar formulario:**
```
Connection Name:      SYS_ADMIN
Username:             sys
Password:             <tu-contraseña-oracle>
Connection Type:      Basic
Hostname:             localhost
Port:                 1521
SID:                  ORCLCDB
Role:                 SYSDBA
Save Password:        ✓ (opcional, solo desarrollo)
```

**3. Probar:**
- [ ] Click "Test"
- [ ] Debe mostrar: "Status: Success"
- [ ] [ ] Click "Save"
- [ ] Click "Connect"

---

### PASO 3: Crear Esquema GYM_APP

**Con conexión SYS_ADMIN activa:**

1. [ ] Abrir: `oracle_db/sql/00_create_schema.sql`
2. [ ] **Copy contenido** del script
3. [ ] En SQL Developer, pegar en editor
4. [ ] Click: **Run Script** (o Ctrl+Enter)
5. [ ] Verificar: Sin errores en output
6. [ ] Comprobar creación:
   ```sql
   SELECT username FROM dba_users WHERE username = 'GYM_APP';
   -- Debe retornar: GYM_APP
   ```

---

### PASO 4: Crear Conexión GYM_APP_USER

En SQL Developer:

**1. Ir a:** Connections → New Connection

**2. Completar formulario:**
```
Connection Name:      GYM_APP_USER
Username:             GYM_APP
Password:             gym_app_password
Connection Type:      Basic
Hostname:             localhost
Port:                 1521
SID:                  ORCLCDB
Role:                 (dejar vacío)
Save Password:        ✓
```

**3. Probar:**
- [ ] Click "Test"
- [ ] Debe mostrar: "Status: Success"
- [ ] Click "Save"
- [ ] Click "Connect"

---

### PASO 5: Crear Tablas

**Con conexión GYM_APP_USER activa:**

1. [ ] Abrir: `oracle_db/sql/01_create_tables.sql`
2. [ ] Copy contenido del script
3. [ ] En SQL Developer, pegar en editor
4. [ ] Click: **Run Script**
5. [ ] Verificar: Sin errores
6. [ ] Comprobar tablas:
   ```sql
   SELECT table_name FROM user_tables ORDER BY table_name;
   -- Debe retornar: T_ACTIVITIES, T_LEADERBOARD, T_RECOMMENDATIONS, 
   --                T_TEAM_MEMBERS, T_TEAMS, T_USERS
   ```

---

### PASO 6: Crear Procedimientos

**Con conexión GYM_APP_USER activa:**

1. [ ] Abrir: `oracle_db/sql/02_create_procedures.sql`
2. [ ] Copy contenido del script
3. [ ] En SQL Developer, pegar en editor
4. [ ] Click: **Run Script**
5. [ ] Verificar: Sin errores
6. [ ] Comprobar procedimientos:
   ```sql
   SELECT object_name FROM user_objects 
   WHERE object_type = 'PROCEDURE' 
   ORDER BY object_name;
   -- Debe retornar: P_CALC_WEEKLY_POINTS, P_GET_RECOMMENDATIONS, 
   --                P_GET_USER_STATS, P_INSERT_ACTIVITY
   ```

---

### PASO 7: Verificar Instalación

**Con conexión GYM_APP_USER activa:**

1. [ ] Abrir: `oracle_db/sql/queries_example.sql`
2. [ ] Ejecutar "VERIFICAR TABLAS CREADAS" (líneas ~10-30)
3. [ ] Ejecutar "VERIFICAR PROCEDIMIENTOS" (líneas ~35-50)
4. [ ] Ejecutar "VERIFICAR ÍNDICES" (líneas ~55-70)
5. [ ] Ejecutar "VERIFICAR SECUENCIAS" (líneas ~75-85)

**Resultado esperado:**
- ✓ 6 tablas (T_USERS, T_TEAMS, etc.)
- ✓ 4 procedimientos (P_*)
- ✓ 10+ índices
- ✓ 6 secuencias

---

## 🐍 PASO 8: Integrar con Django

### Configurar Variables de Entorno

**Crear/actualizar:** `octofit-tracker/backend/.env`

```ini
# Oracle Database Configuration
ORACLE_DB_HOST=localhost
ORACLE_DB_PORT=1521
ORACLE_DB_NAME=ORCLCDB
ORACLE_DB_USER=GYM_APP
ORACLE_DB_PASSWORD=gym_app_password
ORACLE_DB_TYPE=oracle

# Otros
DEBUG=True
SECRET_KEY=tu-clave-secreta-aqui
```

### Configurar Django Settings

**En:** `octofit-tracker/backend/octofit_tracker/settings.py`

```python
# DATABASES
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'localhost:1521/ORCLCDB',
        'USER': 'GYM_APP',
        'PASSWORD': 'gym_app_password',
        'ATOMIC_REQUESTS': True,
        'OPTIONS': {
            'threaded': True,
        },
    }
}
```

### Instalar cx_Oracle

```bash
cd octofit-tracker/backend

# Activar virtual environment
source venv/bin/activate

# Instalar/actualizar cx_Oracle
pip install cx-Oracle==8.3.0

# Probar conexión
python manage.py dbshell
```

---

## ✅ CHECKLIST FINAL

- [ ] Oracle 21C ejecutándose y accesible
- [ ] SQL Developer instalado e iniciado
- [ ] Conexión SYSDBA creada y testada
- [ ] Esquema GYM_APP creado
- [ ] Conexión GYM_APP_USER creada y testada
- [ ] 6 tablas creadas (verificadas)
- [ ] 4 procedimientos creados (verificados)
- [ ] 10+ índices creados (verificados)
- [ ] Django configurado con credenciales GYM_APP
- [ ] cx_Oracle instalado en backend
- [ ] Conexión de Django testada con `python manage.py dbshell`

---

## 🔧 Troubleshooting Rápido

| Problema | Solución |
|----------|----------|
| SQL Dev no inicia | Verificar Java: `java -version` |
| Conexión rechazada | Verificar listener: `ps aux \| grep -i oracle` |
| Error: "ORA-00903" | Sobrequotes en nombres Oracle. Usar MAYÚSCULAS |
| Permisos insuficientes | Reconectarse como SYSDBA y reejecutar GRANTs |
| GYM_APP no existe | Verificar que 00_create_schema.sql se ejecutó |
| Django no conecta | Verificar credenciales en .env y settings.py |

---

## 📚 Documentación Adicional

- [ORACLE_SQLDEVELOPER.instructions.md](../../.github/instructions/ORACLE_SQLDEVELOPER.instructions.md) - Guía detallada
- [oracle_db/README.md](./README.md) - Estándares y estructura
- [oracle_db/sql/queries_example.sql](./sql/queries_example.sql) - Queries útiles
- [Oracle Official Docs](https://docs.oracle.com/) - Referencia oficial

---

## 💾 Backup de Esquema

Hacer backup del esquema GYM_APP regularmente:

```bash
# Exportar esquema completo
expdp GYM_APP/gym_app_password@localhost:1521/ORCLCDB \
  DIRECTORY=exp_dir \
  DUMPFILE=gym_app_backup_$(date +%Y%m%d).dmp \
  LOGFILE=gym_app_backup.log

# O usando SQL Developer:
# Right-click en conexión → Tools → Export → SQL Script
```

---

## 🎯 Próximos Pasos

Una vez completado este checklist:

1. [ ] Ejecutar tests de Django: `python manage.py test`
2. [ ] Crear fixtures de datos: `python manage.py dumpdata`
3. [ ] Configurar frontend React con API
4. [ ] Implementar autenticación
5. [ ] Crear dashboard con leaderboard

---

**¡Listo para empezar! 🚀**
