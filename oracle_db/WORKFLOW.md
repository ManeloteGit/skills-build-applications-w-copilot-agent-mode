# 🔄 FLUJO DE CONFIGURACIÓN - Octofit Tracker con Oracle 21C

## Diagrama General

```
┌────────────────────────────────────────────────────────────────────┐
│                    OCTOFIT TRACKER - ARQUITECTURA                  │
└────────────────────────────────────────────────────────────────────┘

                          ┌─────────────────┐
                          │  Frontend React │
                          │    (Port 3000)  │
                          └────────┬────────┘
                                   │ HTTP/REST
                                   ▼
                    ┌──────────────────────────────┐
                    │   Django Backend API         │
                    │   (Port 8000)                │
                    │  octofit-tracker/backend/    │
                    └──────────────┬───────────────┘
                                   │ SQL
                                   ▼
                    ┌──────────────────────────────┐
                    │   Oracle Database 21C        │
                    │   (Port 1521, SID: ORCLCDB)  │
                    │   ┌───────────────────────┐  │
                    │   │  Esquema: GYM_APP     │  │
                    │   │  - 6 Tablas (T_*)     │  │
                    │   │  - 4 Procedimientos   │  │
                    │   │  - 10+ Índices        │  │
                    │   │  - 6 Secuencias       │  │
                    │   └───────────────────────┘  │
                    └──────────────────────────────┘
```

---

## 1️⃣ FASE INICIAL: Descargar SQL Developer

```
┌────────────────────────────────────────┐
│  1. Descargar SQL Developer            │
├────────────────────────────────────────┤
│ URL: oracle.com/sqldeveloper           │
│ Archivo: sqldeveloper-23.1.0-no-jdk.zip│
│ Tamaño: ~350 MB                         │
│ Tiempo: ~2-3 min                        │
└────────────┬───────────────────────────┘
             │
             ▼
┌────────────────────────────────────────┐
│  2. Extraer y Ejecutar                 │
├────────────────────────────────────────┤
│ $ unzip sqldeveloper-*.zip              │
│ $ ./sqldeveloper/sqldeveloper.sh        │
│ Tiempo: ~5 min                          │
└────────────┬───────────────────────────┘
             │
             ▼ Se abre SQL Developer GUI
```

---

## 2️⃣ FASE DE CONEXIÓN: Crear Conexiones Oracle

```
┌──────────────────────────────────────────────────────┐
│  PASO A: Crear Conexión SYSDBA                      │
├──────────────────────────────────────────────────────┤
│ Connections → New Connection                         │
│                                                      │
│ Connection Name: SYS_ADMIN                          │
│ Username: sys                                        │
│ Password: <tu-pwd-oracle>                           │
│ Host: localhost                                      │
│ Port: 1521                                           │
│ SID: ORCLCDB                                         │
│ Role: SYSDBA                                         │
│                                                      │
│ Click: Test → OK → Connect                          │
└──────────┬───────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────┐
│  PASO B: Crear Conexión GYM_APP (Después FASE 3)    │
├──────────────────────────────────────────────────────┤
│ Connections → New Connection                         │
│                                                      │
│ Connection Name: GYM_APP_USER                       │
│ Username: GYM_APP                                    │
│ Password: gym_app_password                          │
│ Host: localhost                                      │
│ Port: 1521                                           │
│ SID: ORCLCDB                                         │
│ Role: (vacío)                                        │
│                                                      │
│ Click: Test → OK → Connect                          │
└──────────────────────────────────────────────────────┘
```

---

## 3️⃣ FASE DE ESQUEMA: Crear GYM_APP

```
┌────────────────────────────────────────────────────────────┐
│  Archivo: oracle_db/sql/00_create_schema.sql              │
├────────────────────────────────────────────────────────────┤
│  Acciones:                                                 │
│  1. CREATE USER GYM_APP IDENTIFIED BY gym_app_password     │
│  2. GRANT UNLIMITED TABLESPACE TO GYM_APP                  │
│  3. GRANT CREATE SESSION TO GYM_APP                        │
│  4. GRANT CREATE TABLE TO GYM_APP                          │
│  5. GRANT CREATE SEQUENCE TO GYM_APP                       │
│  6. GRANT CREATE PROCEDURE TO GYM_APP                      │
│  7. GRANT CREATE VIEW TO GYM_APP                           │
│  8. GRANT CREATE INDEX TO GYM_APP                          │
│  ... [4 GRANT adicionales]                                 │
│  9. CONNECT GYM_APP/gym_app_password                       │
│                                                            │
│  Requisito: Ejecutar como SYS (conexión SYSDBA)           │
│  Tiempo: ~1 min                                            │
│  Resultado: ✓ Usuario GYM_APP creado y listo              │
└────────────┬─────────────────────────────────────────────┘
             │
             ▼
     [Crear conexión GYM_APP_USER]
```

---

## 4️⃣ FASE DE TABLAS: Crear Estructura

```
┌────────────────────────────────────────────────────────────┐
│  Archivo: oracle_db/sql/01_create_tables.sql              │
├────────────────────────────────────────────────────────────┤
│  Tablas a crear (6 total):                                │
│                                                            │
│  ┌─ T_USERS                                              │
│  │   Columnas: 14, PK: USR_ID, UNIQUE: USR_EMAIL, etc.   │
│  │   Índices: IDX_USERS_EMAIL                             │
│  │                                                         │
│  ├─ T_TEAMS                                               │
│  │   Columnas: 8, PK: TEM_ID, FK: TEM_LEADER_ID          │
│  │   Índices: IDX_TEAMS_LEADER                            │
│  │                                                         │
│  ├─ T_TEAM_MEMBERS                                        │
│  │   Columnas: 5, PK: TMB_ID, FK: TMB_TEAM_ID, etc.      │
│  │   UNIQUE: (TMB_TEAM_ID, TMB_USER_ID)                   │
│  │                                                         │
│  ├─ T_ACTIVITIES                                          │
│  │   Columnas: 11, PK: ACT_ID, FK: ACT_USER_ID           │
│  │   Índices: IDX_ACTIVITIES_USER, IDX_ACTIVITIES_DATE   │
│  │                                                         │
│  ├─ T_LEADERBOARD                                         │
│  │   Columnas: 8, PK: LDB_ID, FK: LDB_USER_ID            │
│  │   Índices: IDX_LEADERBOARD_WEEK, IDX_LEADERBOARD_RANK │
│  │                                                         │
│  └─ T_RECOMMENDATIONS                                     │
│      Columnas: 5, PK: REC_ID, FK: REC_USER_ID            │
│      Índices: IDX_RECOMMENDATIONS_USER                     │
│                                                            │
│  Secuencias (6 total):                                     │
│  - SEQ_USERS → T_USERS.USR_ID                             │
│  - SEQ_TEAMS → T_TEAMS.TEM_ID                             │
│  - SEQ_TEAM_MEMBERS → T_TEAM_MEMBERS.TMB_ID              │
│  - SEQ_ACTIVITIES → T_ACTIVITIES.ACT_ID                   │
│  - SEQ_LEADERBOARD → T_LEADERBOARD.LDB_ID                │
│  - SEQ_RECOMMENDATIONS → T_RECOMMENDATIONS.REC_ID         │
│                                                            │
│  Requisito: Ejecutar como GYM_APP                         │
│  Tiempo: ~2 min                                            │
│  Resultado: ✓ 6 tablas + 10+ índices + 6 secuencias       │
└────────────┬─────────────────────────────────────────────┘
             │
             ▼ Verificar con: SELECT table_name FROM user_tables
```

---

## 5️⃣ FASE DE PROCEDIMIENTOS: Crear Lógica BD

```
┌────────────────────────────────────────────────────────────┐
│  Archivo: oracle_db/sql/02_create_procedures.sql          │
├────────────────────────────────────────────────────────────┤
│  Procedimientos almacenados (4 total):                    │
│                                                            │
│  ┌─ P_CALC_WEEKLY_POINTS                                 │
│  │   Usa: T_LEADERBOARD, T_ACTIVITIES                    │
│  │   Función: Calcular puntos semanales por usuario       │
│  │                                                         │
│  ├─ P_INSERT_ACTIVITY                                     │
│  │   Usa: T_ACTIVITIES, T_LEADERBOARD                     │
│  │   Función: Insertar actividad y actualizar leaderbd   │
│  │                                                         │
│  ├─ P_GET_RECOMMENDATIONS                                 │
│  │   Usa: T_USERS, T_ACTIVITIES, T_RECOMMENDATIONS       │
│  │   Función: Obtener recomendaciones personalizadas      │
│  │                                                         │
│  └─ P_GET_USER_STATS                                      │
│      Usa: T_USERS, T_ACTIVITIES, T_LEADERBOARD           │
│      Función: Obtener estadísticas del usuario            │
│                                                            │
│  Requisito: Ejecutar como GYM_APP                         │
│  Tiempo: ~1 min                                            │
│  Resultado: ✓ 4 procedimientos compilados y listos        │
└────────────┬─────────────────────────────────────────────┘
             │
             ▼ Verificar con: SELECT object_name FROM user_objects...
```

---

## 6️⃣ FASE DE VERIFICACIÓN: Comprobar Instalación

```
┌────────────────────────────────────────────────────────────┐
│  Archivo: oracle_db/sql/queries_example.sql               │
├────────────────────────────────────────────────────────────┤
│  Secciones de verificación:                                │
│                                                            │
│  ✓ VERIFICAR TABLAS CREADAS                               │
│    SELECT table_name FROM user_tables;                     │
│    Resultado esperado: 6 tablas (T_*)                     │
│                                                            │
│  ✓ VERIFICAR PROCEDIMIENTOS                               │
│    SELECT object_name FROM user_objects                   │
│    WHERE object_type = 'PROCEDURE';                        │
│    Resultado esperado: 4 procedimientos (P_*)             │
│                                                            │
│  ✓ VERIFICAR ÍNDICES                                      │
│    SELECT index_name FROM user_indexes;                    │
│    Resultado esperado: 10+ índices                         │
│                                                            │
│  ✓ VERIFICAR SECUENCIAS                                   │
│    SELECT sequence_name FROM user_sequences;               │
│    Resultado esperado: 6 secuencias (SEQ_*)              │
│                                                            │
│  ✓ ESTADÍSTICAS                                            │
│    SELECT table_name, num_rows FROM user_tables;          │
│    Resultado esperado: Todas vacías (num_rows = NULL)     │
│                                                            │
│  ✓ EJEMPLOS DE NEGOCIO                                    │
│    Queries de top usuarios, leaderboard, etc.             │
│                                                            │
│  Tiempo: ~3 min                                            │
│  Resultado: ✓ BD lista para usar con Django               │
└────────────┬─────────────────────────────────────────────┘
             │
             ▼ Pasar a fase Django
```

---

## 7️⃣ FASE DJANGO: Integrar Backend

```
┌────────────────────────────────────────────────────────────┐
│  Archivo: octofit-tracker/backend/.env                    │
├────────────────────────────────────────────────────────────┤
│  ORACLE_DB_HOST=localhost                                 │
│  ORACLE_DB_PORT=1521                                      │
│  ORACLE_DB_NAME=ORCLCDB                                   │
│  ORACLE_DB_USER=GYM_APP                                   │
│  ORACLE_DB_PASSWORD=gym_app_password                      │
└────────────┬─────────────────────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────────────────────┐
│  Archivo: octofit-tracker/backend/octofit_tracker/        │
│            settings.py                                     │
├────────────────────────────────────────────────────────────┤
│  DATABASES = {                                             │
│      'default': {                                          │
│          'ENGINE': 'django.db.backends.oracle',            │
│          'NAME': 'localhost:1521/ORCLCDB',                │
│          'USER': 'GYM_APP',                                │
│          'PASSWORD': 'gym_app_password',                   │
│          'ATOMIC_REQUESTS': True,                          │
│      }                                                     │
│  }                                                         │
└────────────┬─────────────────────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────────────────────┐
│  Terminal: Instalar cx_Oracle                             │
├────────────────────────────────────────────────────────────┤
│  $ cd octofit-tracker/backend                             │
│  $ source venv/bin/activate                               │
│  $ pip install cx-Oracle==8.3.0                           │
│  $ pip install -r requirements.txt                         │
│                                                            │
│  Tiempo: ~2 min                                            │
└────────────┬─────────────────────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────────────────────┐
│  Terminal: Probar Conexión                                │
├────────────────────────────────────────────────────────────┤
│  $ python manage.py dbshell                               │
│  SQL> SELECT COUNT(*) FROM T_USERS;                        │
│  0 rows returned ✓                                         │
│  SQL> EXIT;                                                │
│                                                            │
│  Resultado: ✓ Django conectado a GYM_APP                  │
└────────────┬─────────────────────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────────────────────┐
│  Terminal: Iniciar Django Server                          │
├────────────────────────────────────────────────────────────┤
│  $ python manage.py runserver 0.0.0.0:8000               │
│  http://localhost:8000/api/users/                          │
│                                                            │
│  Resultado: ✓ API funcionando                              │
└────────────────────────────────────────────────────────────┘
```

---

## 8️⃣ FASE REACT: Frontend (Opcional)

```
┌────────────────────────────────────────────────────────────┐
│  Terminal: Iniciar React                                  │
├────────────────────────────────────────────────────────────┤
│  $ cd octofit-tracker/frontend                            │
│  $ npm install                                             │
│  $ npm start                                               │
│                                                            │
│  http://localhost:3000                                     │
│                                                            │
│  Frontend conecta → API Django → Oracle GYM_APP            │
│                                                            │
│  Resultado: ✓ Aplicación completa ejecutándose            │
└────────────────────────────────────────────────────────────┘
```

---

## ⏱️ TIMELINE TOTAL

```
┌─────────────────────────────────────────┐
│ Fase                          │ Tiempo   │
├─────────────────────────────────────────┤
│ 1. Download SQL Developer     │ 3 min    │
│ 2. Create Connections         │ 4 min    │
│ 3. Create Schema GYM_APP      │ 2 min    │
│ 4. Create Tables              │ 3 min    │
│ 5. Create Procedures          │ 2 min    │
│ 6. Verification               │ 3 min    │
│ 7. Django Integration         │ 5 min    │
│ 8. React Frontend (Opt)       │ 3 min    │
├─────────────────────────────────────────┤
│ TOTAL                         │ 25 min   │
└─────────────────────────────────────────┘
```

---

## 📊 DATA FLOW

```
Usuario                  Frontend React              Django Backend              Oracle GYM_APP
  │                      (localhost:3000)            (localhost:8000)            (localhost:1521)
  │                            │                            │                           │
  │─ Register/Login ───────→   │                            │                           │
  │                            │─ POST /api/users/auth ──→  │                           │
  │                            │                            │─ CALL P_INSERT_USER ──→  │
  │                            │                            │                    T_USERS
  │                            │← Jwt Token ────────────────│← Success  ─────────────  │
  │← Auth Token ────────────   │                            │                           │
  │                            │                            │                           │
  │─ Log Activity  ─────────→  │                            │                           │
  │                            │─ POST /api/activities/ ──→ │                           │
  │                            │                            │─ CALL P_INSERT_ACTIVITY →│
  │                            │                            │                    T_ACTIVITIES
  │                            │                            │└─ UPDATE T_LEADERBOARD  │
  │← Activity Created ────────  │← 201 Created ────────────  │                           │
  │                            │                            │                           │
  │─ View Leaderboard ───────→ │                            │                           │
  │                            │─ GET /api/leaderboard/ ──→ │                           │
  │                            │                            │─ SELECT * T_LEADERBOARD→│
  │                            │← JSON Data ────────────────│← Results ─────────────── │
  │                            │                            │                           │
  │← Leaderboard Ranking ────  │                            │                           │
```

---

## ✅ CHECKLIST FINAL

```
PRE-SETUP
□ Oracle 21C ejecutándose
□ Puerto 1521 abierto
□ Usuario sys accesible

SQL DEVELOPER
□ Descargado e instalado
□ Ejecutándose sin errores
□ Conexión SYSDBA testada

ORACLE DATABASE
□ Esquema GYM_APP creado
□ 6 tablas creadas
□ 10+ índices creados
□ 6 secuencias creadas
□ 4 procedimientos compilados

DJANGO
□ cx_Oracle instalado
□ settings.py configurado
□ .env con credenciales
□ Conexión testada dbshell

REACT (OPCIONAL)
□ npm dependencies instaladas
□ Frontend ejecutándose

INTEGRACIÓN
□ API endpoints respondiend
□ Frontend conectado a API
□ Oracle recibiendo datos
```

---

**Última actualización:** 20/03/2026  
**Estado:** ✅ Listo para Producción  
**Documentación:** Completa y Actualizada
