# Oracle Database - Octofit Tracker

Documentación y scripts SQL para la base de datos Oracle del proyecto Octofit Tracker.

## 🚀 Inicio Rápido con SQL Developer

### Esquema GYM_APP

El proyecto utiliza un esquema dedicado llamado **`GYM_APP`** en Oracle 21C local.

**Pasos rápidos:**

1. **Descargar SQL Developer:**
   ```bash
   wget https://download.oracle.com/otn/java/sqldeveloper/sqldeveloper-23.1.0.087.1900-no-jdk.zip
   unzip sqldeveloper-23.1.0.087.1900-no-jdk.zip
   /path/to/sqldeveloper/sqldeveloper.sh
   ```

2. **Crear conexión SYSDBA** en SQL Developer:
   - Host: `localhost`
   - Port: `1521`
   - SID: `ORCLCDB`
   - Username: `sys`
   - Password: `<tu-contraseña>`
   - Role: `SYSDBA`

3. **Ejecutar script de esquema:**
   ```
   Abrir: oracle_db/sql/00_create_schema.sql
   Ejecutar: Ctrl+Enter
   ```

4. **Crear conexión GYM_APP** en SQL Developer:
   - Host: `localhost`
   - Port: `1521`
   - SID: `ORCLCDB`
   - Username: `GYM_APP`
   - Password: `gym_app_password`

5. **Ejecutar scripts en orden:**
   ```
   1️⃣  oracle_db/sql/00_create_schema.sql   (ya ejecutado arriba)
   2️⃣  oracle_db/sql/01_create_tables.sql   (tablas)
   3️⃣  oracle_db/sql/02_create_procedures.sql (procedimientos)
   ```

📖 **Documentación completa:** Ver [ORACLE_SQLDEVELOPER.instructions.md](../../.github/instructions/ORACLE_SQLDEVELOPER.instructions.md)

---

## Estándares de Nomenclatura Oracle

Seguir estas convenciones para mantener consistencia:

### Tablas
- Prefijo: `T_`
- Ejemplo: `T_USERS`, `T_ACTIVITIES`
- Mayúsculas obligatorias
- Agregar comentario descriptivo

### Campos/Columnas
- Formato: `{Acrónimo Tabla}_{nombre_campo}`
- Acrónimo: 3 letras del nombre de la tabla
- Ejemplo: `USR_ID`, `ACT_TYPE`, `TEM_NAME`
- Mayúsculas obligatorias

### Vistas
- Prefijo: `W_`
- Ejemplo: `W_USER_STATS`

### Procedimientos Almacenados
- Prefijo: `P_`
- Ejemplo: `P_CALC_WEEKLY_POINTS`, `P_INSERT_ACTIVITY`

### Funciones
- Prefijo: `F_`
- Ejemplo: `F_CALCULATE_BMI`

### Paquetes
- Prefijo: `PKG_`
- Ejemplo: `PKG_USER_MANAGEMENT`

### Variables
- Prefijo: `V_`
- Ejemplo: `V_USER_ID`, `V_TOTAL_POINTS`

### Constantes
- Prefijo: `K_`
- Ejemplo: `K_MAX_PASSWORD_LENGTH`

## Scripts SQL (Orden de Ejecución)

### 0️⃣  00_create_schema.sql

**Propósito:** Crear el usuario/esquema `GYM_APP` con permisos necesarios

**Requisito:** Conectarse como `SYS` o usuario DBA

**Acciones:**
- Crear usuario `GYM_APP`
- Asignar permisos de tablespace ilimitado
- Otorgar permisos para crear tablas, procedimientos, índices, vistas, etc.
- Cambiar conexión a `GYM_APP`

**Ejecución en SQL Developer:**
```
Conexión: SYSDBA
Abrir: oracle_db/sql/00_create_schema.sql
Click: Run Script (Ctrl+Enter)
```

### 1️⃣  01_create_tables.sql

Crea la estructura base de todas las tablas:

- `T_USERS` - Información de usuarios
- `T_TEAMS` - Información de equipos
- `T_TEAM_MEMBERS` - Relación usuario-equipo
- `T_ACTIVITIES` - Registro de actividades
- `T_LEADERBOARD` - Clasificación semanal
- `T_RECOMMENDATIONS` - Recomendaciones personalizadas

Incluye:
- Constraints (PK, FK, UNIQUE)
- Índices para optimización
- Secuencias para auto-increment
- Comentarios descriptivos

**Ejecución en SQL Developer:**
```
Conexión: GYM_APP_USER
Abrir: oracle_db/sql/01_create_tables.sql
Click: Run Script (Ctrl+Enter)
```

### 2️⃣  02_create_procedures.sql

Procedimientos almacenados:

- `P_CALC_WEEKLY_POINTS` - Calcula puntos semanales
- `P_INSERT_ACTIVITY` - Inserta nueva actividad
- `P_GET_RECOMMENDATIONS` - Obtiene recomendaciones
- `P_GET_USER_STATS` - Obtiene estadísticas de usuario

**Ejecución en SQL Developer:**
```
Conexión: GYM_APP_USER
Abrir: oracle_db/sql/02_create_procedures.sql
Click: Run Script (Ctrl+Enter)
```

## Instalación de Scripts

### ✅ Opción 1: SQL Developer (RECOMENDADO)

1. Abrir SQL Developer
2. Crear conexiones (SYSDBA y GYM_APP_USER)
3. Ejecutar scripts en orden: 00 → 01 → 02
4. Verificar con consultas de verificación

**Pasos detallados:** Ver [ORACLE_SQLDEVELOPER.instructions.md](../../.github/instructions/ORACLE_SQLDEVELOPER.instructions.md)

### Opción 2: Command Line (sqlplus)

```bash
# Conectarse como DBA
sqlplus sys/contraseña@localhost:1521/ORCLCDB as sysdba

# Ejecutar esquema
SQL> @oracle_db/sql/00_create_schema.sql

# Conectarse como GYM_APP
sqlplus GYM_APP/gym_app_password@localhost:1521/ORCLCDB

# Ejecutar tablas y procedimientos
SQL> @oracle_db/sql/01_create_tables.sql
SQL> @oracle_db/sql/02_create_procedures.sql
SQL> EXIT;
```

### Opción 3: SQLcl (Oracle SQL Command Line)

```bash
# Ejecutar scripts en secuencia
sql sys/contraseña@localhost:1521/ORCLCDB as sysdba @oracle_db/sql/00_create_schema.sql
sql GYM_APP/gym_app_password@localhost:1521/ORCLCDB @oracle_db/sql/01_create_tables.sql
sql GYM_APP/gym_app_password@localhost:1521/ORCLCDB @oracle_db/sql/02_create_procedures.sql
```

## Estructura de Datos

### Relaciones

```
T_USERS (1) ──┬─→ (N) T_ACTIVITIES
              ├─→ (N) T_TEAMS (líder)
              ├─→ (N) T_TEAM_MEMBERS
              ├─→ (N) T_LEADERBOARD
              └─→ (N) T_RECOMMENDATIONS

T_TEAMS (1) ──┬─→ (N) T_TEAM_MEMBERS
              ├─→ (1) T_USERS (líder)
              └─→ (N) T_LEADERBOARD_TEAMS
```

### Tipos de Datos Principales

| Campo | Tipo | Tamaño | Descripción |
|-------|------|--------|-------------|
| IDs | NUMBER | - | Secuencias auto-increment |
| Nombres/Descripciones | VARCHAR2 | Variable | Texto variable |
| Fechas | TIMESTAMP | - | Con zona horaria |
| Números decimales | FLOAT | - | Distancia, peso, altura |
| Booleanos | NUMBER(1) | 1 byte | 0=false, 1=true |

## Mantenimiento

### Reorganizar Tablas

```sql
ALTER TABLE T_USERS SHRINK SPACE;
```

### Recompiler Índices

```sql
ALTER INDEX IDX_USERS_EMAIL REBUILD;
```

### Estadísticas

```sql
EXEC DBMS_STATS.GATHER_TABLE_STATS('owner', 'T_USERS');
```

### Backup

```bash
expdp usuario/contraseña@database DIRECTORY=exp_dir DUMPFILE=octofit_backup.dmp
```

## Seguridad

### Usuario de Base de Datos

Crear usuario solo para aplicación:

```sql
CREATE USER octofit IDENTIFIED BY contraseña_segura;
GRANT CONNECT, RESOURCE TO octofit;
GRANT SELECT, INSERT, UPDATE, DELETE ON T_USERS TO octofit;
-- Delegar permisos por tabla según necesidad
```

### Validación de Entrada

- Evitar SQL dinámico
- Usar procedimientos almacenados
- Validar tipos de datos
- Sanitizar entradas

### Auditoría

```sql
CREATE TABLE T_AUDIT_LOG (
    AUD_ID NUMBER PRIMARY KEY,
    AUD_TABLE_NAME VARCHAR2(30),
    AUD_ACTION VARCHAR2(1),
    AUD_USER VARCHAR2(30),
    AUD_TIMESTAMP TIMESTAMP,
    AUD_OLD_VALUES CLOB,
    AUD_NEW_VALUES CLOB
);
```

## Performance

### Índices

Ya creados en el script:
- `IDX_USERS_EMAIL` - Búsqueda de usuarios
- `IDX_ACTIVITIES_USER` - Actividades por usuario
- `IDX_LEADERBOARD_WEEK` - Leaderboard por semana
- Etc.

### Hints de Optimización

```sql
-- Usar índices forzadamente
SELECT /*+ INDEX(t IDX_USERS_EMAIL) */ * FROM T_USERS t;

-- Parallel query
SELECT /*+ PARALLEL(4) */ * FROM T_ACTIVITIES;
```

## Troubleshooting

### Tablas no existen

```sql
SELECT table_name FROM user_tables WHERE table_name LIKE 'T_%';
```

### Ver estructura de tabla

```sql
DESC T_USERS;
```

### Ver procedimientos

```sql
SELECT object_name FROM user_objects WHERE object_type = 'PROCEDURE';
```

### Ver errores de compilación

```sql
SHOW ERRORS;
```

## Importar/Exportar Datos

### Exportar datos

```sql
SPOOL datos_export.sql
SELECT 'INSERT INTO T_USERS VALUES(' || USR_ID || ',...)' FROM T_USERS;
SPOOL OFF;
```

### Importar datos

```sql
@datos_export.sql;
COMMIT;
```

## Recursos Adicionales

- [Oracle Documentation](https://docs.oracle.com/)
- [Oracle SQL Developer Download](https://www.oracle.com/database/sqldeveloper/download/)
- [Oracle 23c Features](https://www.oracle.com/database/23c/features/)

## Contacto y Soporte

Para preguntas sobre los scripts o estándares de la BD, contactar al equipo de desarrollo.
