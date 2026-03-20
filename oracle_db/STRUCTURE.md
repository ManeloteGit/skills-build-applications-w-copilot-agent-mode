# 📁 Estructura de Archivos - Oracle Database + SQL Developer

```
📦 skills-build-applications-w-copilot-agent-mode/
│
├── 📂 .github/
│   └── 📂 instructions/
│       ├── 📄 ORACLE_DB.instructions.md
│       │   └─ Estándares de nomenclatura Oracle
│       │   └─ Reglas de procedimientos almacenados
│       │   └─ Consideraciones de seguridad
│       │
│       ├── 📄 ORACLE_SQLDEVELOPER.instructions.md ⭐ NEW
│       │   └─ Instalación de SQL Developer
│       │   └─ Crear conexiones a Oracle 21C
│       │   └─ Crear esquema GYM_APP
│       │   └─ Ejecutar scripts en orden
│       │   └─ Troubleshooting
│       │
│       ├── 📄 octofit_tracker_django_backend.instructions.md
│       ├── 📄 octofit_tracker_react_frontend.instructions.md
│       └── 📄 octofit_tracker_setup_project.instructions.md
│
├── 📂 oracle_db/
│   ├── 📄 README.md
│   │   └─ Estándares de nomenclatura
│   │   └─ Descripción de scripts
│   │   └─ Instrucciones de instalación
│   │   └─ Relaciones de datos
│   │   └─ Mantenimiento
│   │
│   ├── 📄 QUICKSTART.md ⭐ NEW
│   │   └─ Resumen de 10 pasos
│   │   └─ Checklist de configuración
│   │   └─ Integración con Django
│   │   └─ Troubleshooting
│   │
│   ├── 📄 ARCHITECTURE.md
│   │   └─ Diagrama del sistema
│   │   └─ Componentes principales
│   │
│   └── 📂 sql/
│       ├── 📄 00_create_schema.sql ⭐ NEW
│       │   └─ Crear usuario GYM_APP
│       │   └─ Asignar permisos
│       │   └─ Preparar esquema
│       │   ⚠️  Ejecutar COMO SYSDBA
│       │
│       ├── 📄 01_create_tables.sql
│       │   ├─ CREATE TABLE T_USERS
│       │   ├─ CREATE TABLE T_TEAMS
│       │   ├─ CREATE TABLE T_TEAM_MEMBERS
│       │   ├─ CREATE TABLE T_ACTIVITIES
│       │   ├─ CREATE TABLE T_LEADERBOARD
│       │   ├─ CREATE TABLE T_RECOMMENDATIONS
│       │   ├─ CREATE SEQUENCE (auto-increment)
│       │   ├─ CREATE INDEX (10+ índices)
│       │   └─ COMMENTS
│       │   ✓ Ejecutar COMO GYM_APP
│       │
│       ├── 📄 02_create_procedures.sql
│       │   ├─ CREATE PROCEDURE P_CALC_WEEKLY_POINTS
│       │   ├─ CREATE PROCEDURE P_INSERT_ACTIVITY
│       │   ├─ CREATE PROCEDURE P_GET_RECOMMENDATIONS
│       │   └─ CREATE PROCEDURE P_GET_USER_STATS
│       │   ✓ Ejecutar COMO GYM_APP
│       │
│       └── 📄 queries_example.sql ⭐ NEW
│           ├─ Verificar tablas creadas
│           ├─ Verificar procedimientos
│           ├─ Verificar índices
│           ├─ Verificar secuencias
│           ├─ Estadísticas de tablas
│           ├─ Constraints y permisos
│           ├─ Sincronización
│           ├─ Diagnósticos
│           └─ Ejemplos de queries de negocio
│
├── 📂 octofit-tracker/
│   ├── 📂 backend/
│   │   ├── 📄 requirements.txt
│   │   │   └─ Django, DRF, cx_Oracle, etc.
│   │   │
│   │   ├── 📄 manage.py
│   │   ├── 📄 README.md
│   │   │
│   │   ├── 📂 octofit_tracker/
│   │   │   ├── 📄 settings.py
│   │   │   │   └─ DATABASES config para Oracle
│   │   │   │   └─ GYM_APP credentials
│   │   │   │
│   │   │   ├── 📄 urls.py
│   │   │   ├── 📄 asgi.py
│   │   │   ├── 📄 wsgi.py
│   │   │   │
│   │   │   └── 📂 apps/
│   │   │       ├── 📂 users/
│   │   │       ├── 📂 activities/
│   │   │       ├── 📂 teams/
│   │   │       ├── 📂 leaderboard/
│   │   │       └── 📂 recommendations/
│   │   │
│   │   └── 📄 .env.example
│   │       └─ ORACLE_DB_USER=GYM_APP
│   │       └─ ORACLE_DB_PASSWORD=gym_app_password
│   │
│   └── 📂 frontend/
│       ├── 📄 package.json
│       ├── 📄 README.md
│       └── 📂 src/
│           ├── 📂 components/
│           ├── 📂 pages/
│           ├── 📂 services/
│           │   └── api.js
│           │       └─ Conecta a /api/... endpoints
│           └── 📂 context/
└─
```

---

## 📋 Flujo de Setup Recomendado

### 1️⃣ PREREQUISITOS
```
✓ Oracle Database 21C ejecutándose
✓ Puerto 1521 abierto
✓ Usuario SYS accesible
```

### 2️⃣ SQL DEVELOPER
```
Descargar → Extraer → Ejecutar
→ Crear conexión SYSDBA
```

### 3️⃣ ESQUEMA GYM_APP
```
.github/instructions/ORACLE_SQLDEVELOPER.instructions.md
→ oracle_db/sql/00_create_schema.sql (Como SYSDBA)
→ Crear conexión GYM_APP_USER
```

### 4️⃣ OBJETOS DE BD
```
oracle_db/sql/01_create_tables.sql   (Como GYM_APP)
     ↓
oracle_db/sql/02_create_procedures.sql (Como GYM_APP)
     ✓ Verificar con queries_example.sql
```

### 5️⃣ DJANGO BACKEND
```
.env → ORACLE_DB_USER=GYM_APP
settings.py → DATABASES config
pip install cx_Oracle
python manage.py dbshell (Test)
```

### 6️⃣ FRONTEND REACT
```
Frontend se conecta a API /api/...
Que usa Django ORM → Oracle GYM_APP
```

---

## 🔑 Variables Clave

```
┌─────────────────────────┬──────────────────────┐
│ Variable                │ Valor                │
├─────────────────────────┼──────────────────────┤
│ Esquema                 │ GYM_APP              │
│ Usuario                 │ GYM_APP              │
│ Contraseña              │ gym_app_password     │
│ Host                    │ localhost            │
│ Puerto                  │ 1521                 │
│ SID                     │ ORCLCDB              │
│ Role (Usuario Regular)  │ (vacío/ninguno)      │
│ Role (Administrador)    │ SYSDBA               │
└─────────────────────────┴──────────────────────┘
```

---

## 📊 Tablas en GYM_APP

```
T_USERS
├─ USR_ID (PK)
├─ USR_USERNAME (UNIQUE)
├─ USR_EMAIL (UNIQUE)
├─ USR_PASSWORD
└─ [10 más campos]

T_TEAMS
├─ TEM_ID (PK)
├─ TEM_NAME (UNIQUE)
├─ TEM_LEADER_ID (FK → T_USERS)
└─ [5 más campos]

T_TEAM_MEMBERS
├─ TMB_ID (PK)
├─ TMB_TEAM_ID (FK → T_TEAMS)
├─ TMB_USER_ID (FK → T_USERS)
└─ [2 más campos]

T_ACTIVITIES
├─ ACT_ID (PK)
├─ ACT_USER_ID (FK → T_USERS)
├─ ACT_TYPE
├─ ACT_DURATION_MINUTES
└─ [7 más campos]

T_LEADERBOARD
├─ LDB_ID (PK)
├─ LDB_WEEK_ID
├─ LDB_USER_ID (FK → T_USERS)
├─ LDB_POINTS
└─ [3 más campos]

T_RECOMMENDATIONS
├─ REC_ID (PK)
├─ REC_USER_ID (FK → T_USERS)
└─ [4 más campos]
```

---

## 🔗 Relaciones de Integridad Referencial

```
T_USERS (1) ──┬─→ (N) T_ACTIVITIES
              ├─→ (1) T_TEAMS (como líder)
              ├─→ (N) T_TEAM_MEMBERS
              ├─→ (N) T_LEADERBOARD
              └─→ (N) T_RECOMMENDATIONS

T_TEAMS (1) ──┬─→ (N) T_TEAM_MEMBERS
              ├─→ (1) T_USERS (líder)
              └─→ (N) T_LEADERBOARD (opcional)

T_TEAM_MEMBERS (N) ──→ (1) T_TEAMS
                  └──→ (1) T_USERS
```

---

## 📁 Archivos Críticos para SQL Developer

### Para Ejecutar

| Archivo | Conectarse Como | Descripción |
|---------|-----------------|-------------|
| `00_create_schema.sql` | `SYS` (SYSDBA) | Crear GYM_APP |
| `01_create_tables.sql` | `GYM_APP` | Tablas y índices |
| `02_create_procedures.sql` | `GYM_APP` | Procedimientos |
| `queries_example.sql` | `GYM_APP` | Verificación |

### Para Leer

| Archivo | Propósito |
|---------|-----------|
| `QUICKSTART.md` | Guía rápida con checklist |
| `README.md` | Documentación completa |
| `.instructions/ORACLE_SQLDEVELOPER.instructions.md` | Instrucciones detalladas |

---

## 🔐 Estructura de Permisos

```
SYS (SYSDBA)
 └─ Crea usuario GYM_APP
     └─ GRANT CREATE TABLE
     └─ GRANT CREATE SEQUENCE  
     └─ GRANT CREATE PROCEDURE
     └─ GRANT UNLIMITED TABLESPACE
     └─ [8+ permisos adicionales]
```

---

## ⏱️ Tiempo de Ejecución Estimado

| Tarea | Tiempo |
|-------|--------|
| Descargar e instalar SQL Dev | 5 min |
| Crear conexión SYSDBA | 2 min |
| Ejecutar 00_create_schema.sql | 1 min |
| Crear conexión GYM_APP | 2 min |
| Ejecutar 01_create_tables.sql | 2 min |
| Ejecutar 02_create_procedures.sql | 1 min |
| Verificar con queries | 3 min |
| Configurar Django | 5 min |
| **TOTAL** | **≈ 20-25 min** |

---

## ✅ Verificación Post-Instalación

```bash
# En SQL Developer (conexión GYM_APP_USER):

SELECT table_name FROM user_tables ORDER BY table_name;
-- Esperado: T_ACTIVITIES, T_LEADERBOARD, T_RECOMMENDATIONS, 
--          T_TEAM_MEMBERS, T_TEAMS, T_USERS

SELECT object_name FROM user_objects WHERE object_type = 'PROCEDURE';
-- Esperado: P_CALC_WEEKLY_POINTS, P_GET_RECOMMENDATIONS, 
--          P_GET_USER_STATS, P_INSERT_ACTIVITY

SELECT sequence_name FROM user_sequences;
-- Esperado: SEQ_ACTIVITIES, SEQ_LEADERBOARD, SEQ_RECOMMENDATIONS,
--          SEQ_TEAM_MEMBERS, SEQ_TEAMS, SEQ_USERS

SELECT index_name FROM user_indexes;
-- Esperado: 10+ índices
```

---

## 🔥 Troubleshooting Rápido

| Error | Checklist |
|-------|-----------|
| Conexión rechazada | ✓ Oracle ejecutándose? `ps aux \| grep oracle` |
| | ✓ Puerto 1521 libre? `netstat -tlnp \| grep 1521` |
| Tabla no existe | ✓ Ejecutó 01_create_tables.sql? |
| | ✓ Como usuario GYM_APP? |
| Permisos insuficientes | ✓ Ejecutó 00_create_schema.sql como SYSDBA? |
| Django no conecta | ✓ Contraseña correcta en .env? |
| | ✓ cx_Oracle instalado? `pip list \| grep cx` |

---

**Documento generado:** 20/03/2026  
**Versión:** 1.0  
**Status:** ✅ Listo para Usar
