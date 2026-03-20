# 📚 Índice de Documentación - Oracle Database & SQL Developer

**Proyecto:** Octofit Tracker  
**Base de Datos:** Oracle 21C  
**Esquema:** GYM_APP  
**Última Actualización:** 20/03/2026

---

## 🚀 COMIENZA AQUÍ

### Para Usuarios Nuevos (Primera Vez)
👉 **[QUICKSTART.md](QUICKSTART.md)** ← **Comienza con esto**
- Checklist de 10 pasos
- Instrucciones claras y ordenadas
- ~20-25 minutos para completar

### Para Ver el Flujo Completo
👉 **[WORKFLOW.md](WORKFLOW.md)**
- Diagrama visual de 8 fases
- Timeline y data flow
- Checklist final

### Para Entender la Estructura
👉 **[STRUCTURE.md](STRUCTURE.md)**  
- Diagrama ASCII del proyecto
- Ubicación de cada archivo
- Tabla de troubleshooting

---

## 📖 DOCUMENTACIÓN DETALLADA

### 1. Instalación y Configuración SQL Developer

**Archivo:** [.github/instructions/ORACLE_SQLDEVELOPER.instructions.md](../../.github/instructions/ORACLE_SQLDEVELOPER.instructions.md)

**Temas:**
- ✅ Descargar SQL Developer (Linux, Windows, Docker)
- ✅ Crear conexión SYSDBA
- ✅ Crear esquema GYM_APP
- ✅ Crear conexión GYM_APP_USER
- ✅ Ejecutar scripts de creación
- ✅ Verificar objetos creados
- ✅ Troubleshooting y seguridad
- ✅ Integración con Django

**Usar cuando:** Necesitas instrucciones paso a paso detalladas

---

### 2. Estándares de Base de Datos

**Archivo:** [README.md](README.md)

**Temas:**
- 📋 Estándares de nomenclatura Oracle
  - Prefijos: T_ (tabla), P_ (procedimiento), W_ (vista), etc.
  - Acrónimos de 3 letras para columnas
  - Ejemplos: T_USERS, USR_ID, P_CALC_WEEKLY_POINTS
- 📊 Descripción de cada tabla
- 🔗 Relaciones entre tablas
- 📈 Performance y optimización
- 🔐 Seguridad y auditoría
- 🧹 Mantenimiento de BD

**Usar cuando:** Necesitas entender la estructura o añadir nuevas tablas

---

### 3. Scripts SQL

#### Script 00: Crear Esquema
**Archivo:** [sql/00_create_schema.sql](sql/00_create_schema.sql)

```sql
CREATE USER GYM_APP IDENTIFIED BY gym_app_password;
GRANT UNLIMITED TABLESPACE TO GYM_APP;
-- ... [12 GRANTs adicionales]
```

| Aspecto | Detalle |
|--------|---------|
| **Ejecutar como** | SYS (SYSDBA) |
| **Tiempo** | ~1 min |
| **Resultado** | Usuario GYM_APP con permisos |
| **Primero** | ✅ Sí |

---

#### Script 01: Crear Tablas
**Archivo:** [sql/01_create_tables.sql](sql/01_create_tables.sql)

**Crea:**
- ✅ 6 tablas (T_USERS, T_TEAMS, T_TEAM_MEMBERS, T_ACTIVITIES, T_LEADERBOARD, T_RECOMMENDATIONS)
- ✅ 6 secuencias (auto-increment)
- ✅ 10+ índices (para performance)
- ✅ Constraints (PK, FK, UNIQUE)
- ✅ Comentarios en todas las columnas

| Aspecto | Detalle |
|--------|---------|
| **Ejecutar como** | GYM_APP |
| **Tiempo** | ~2 min |
| **Líneas** | ~400+ SQL |
| **Orden** | 2º (después de 00) |

---

#### Script 02: Crear Procedimientos
**Archivo:** [sql/02_create_procedures.sql](sql/02_create_procedures.sql)

**Procedimientos:**
1. `P_CALC_WEEKLY_POINTS` - Calcula puntos semanales
2. `P_INSERT_ACTIVITY` - Inserta actividades
3. `P_GET_RECOMMENDATIONS` - Obtiene recomendaciones
4. `P_GET_USER_STATS` - Estadísticas de usuario

| Aspecto | Detalle |
|--------|---------|
| **Ejecutar como** | GYM_APP |
| **Tiempo** | ~1 min |
| **Parámetros** | IN/OUT documentados |
| **Orden** | 3º (después de 01) |

---

#### Script Ejemplos: Queries Útiles
**Archivo:** [sql/queries_example.sql](sql/queries_example.sql)

**11 Secciones:**
1. Verificar tablas → `SELECT table_name FROM user_tables`
2. Procedimientos → `SELECT object_name FROM user_objects`
3. Índices → `SELECT index_name FROM user_indexes`
4. Secuencias → `SELECT sequence_name FROM user_sequences`
5. Estadísticas → `SELECT num_rows FROM user_tables`
6. Constraints → `SELECT constraint_name FROM user_constraints`
7. Información usuario → `SHOW USER` y permisos
8. Sincronización → `EXEC DBMS_STATS.GATHER_TABLE_STATS`
9. Diagnósticos → `SHOW ERRORS`
10. Limpiar datos → DELETE, TRUNCATE (con precaución)
11. Ejemplos negocio → Top usuarios, leaderboard, etc.

**Usar cuando:** Necesitas consultar datos rápidamente

---

## 🗂️ ESTRUCTURA DE CARPETAS

```
octofit-tracker-oracle/
├── 📂 .github/
│   └── 📂 instructions/
│       ├── ORACLE_SQLDEVELOPER.instructions.md ⭐ Instalación
│       └── ORACLE_DB.instructions.md            ← Estándares
│
├── 📂 oracle_db/
│   ├── INDEX.md          ← TÚ ESTÁS AQUÍ
│   ├── QUICKSTART.md     ⭐ Empieza aquí
│   ├── WORKFLOW.md       ⭐ Diagrama visual
│   ├── STRUCTURE.md      ⭐ Estructura proyecto
│   ├── README.md         ← Documentación completa
│   │
│   └── 📂 sql/
│       ├── 00_create_schema.sql      (SYSDBA)
│       ├── 01_create_tables.sql      (GYM_APP)
│       ├── 02_create_procedures.sql  (GYM_APP)
│       └── queries_example.sql       (Ejemplos)
│
└── 📂 octofit-tracker/
    ├── 📂 backend/
    │   ├── .env
    │   ├── requirements.txt
    │   └── octofit_tracker/settings.py ← Actualizar DATABASES
    │
    └── 📂 frontend/
        ├── src/services/api.js ← Consume /api/... endpoints
```

---

## 🎯 MAPEO DE TAREAS A DOCUMENTOS

| Tarea | Archivo | Sección |
|-------|---------|---------|
| Instalar SQL Developer | ORACLE_SQLDEVELOPER.instructions.md | Paso 1 |
| Conectar a Oracle | ORACLE_SQLDEVELOPER.instructions.md | Paso 2 |
| Crear esquema GYM_APP | QUICKSTART.md | Paso 5 |
| Ejecutar script 00 | 00_create_schema.sql | Completo |
| Ejecutar script 01 | 01_create_tables.sql | Completo |
| Ejecutar script 02 | 02_create_procedures.sql | Completo |
| Verificar instalación | queries_example.sql | Secciones 1-5 |
| Configurar Django | QUICKSTART.md | Paso 8 |
| Troubleshoot conexión | STRUCTURE.md | Tabla TB |
| Entender flujo | WORKFLOW.md | Fases 1-8 |
| Ver estructura completa | STRUCTURE.md | Diagrama ASCII |

---

## ⏱️ TIMELINE RECOMENDADO

```
┌──────────────────────────────┬──────┐
│ Actividad                    │ Tiempo│
├──────────────────────────────┼──────┤
│ Leer QUICKSTART.md           │ 3 min│
│ Descargar SQL Developer      │ 3 min│
│ Crear conexiones (2)         │ 4 min│
│ Ejecutar script 00           │ 1 min│
│ Ejecutar script 01           │ 2 min│
│ Ejecutar script 02           │ 1 min│
│ Verificar con queries        │ 3 min│
│ Configurar Django            │ 5 min│
├──────────────────────────────┼──────┤
│ TOTAL                        │ 22min│
└──────────────────────────────┴──────┘
```

---

## 🔑 CREDENCIALES

```
╔════════════════════════════════════╗
║      ORACLE 21C - GYM_APP          ║
╠════════════════════════════════════╣
║ Host            │ localhost        ║
║ Port            │ 1521             ║
║ SID             │ ORCLCDB          ║
╠════════════════════════════════════╣
║ Admin User      │ sys              ║
║ Admin Password  │ <contraseña>     ║
║ Admin Role      │ SYSDBA           ║
╠════════════════════════════════════╣
║ App User        │ GYM_APP          ║
║ App Password    │ gym_app_password ║
║ App Role        │ (vacío)          ║
╚════════════════════════════════════╝
```

---

## 📊 OBJETOS CREADOS

### Tablas (6)
| Tabla | Propósito | Filas | Columnas |
|-------|-----------|-------|----------|
| T_USERS | Usuarios | 0 | 14 |
| T_TEAMS | Equipos | 0 | 8 |
| T_TEAM_MEMBERS | Miembros de equipo | 0 | 5 |
| T_ACTIVITIES | Actividades log | 0 | 11 |
| T_LEADERBOARD | Ranking semanal | 0 | 8 |
| T_RECOMMENDATIONS | Recomendaciones | 0 | 5 |

### Procedimientos (4)
| Procedimiento | Parámetros | Función |
|---------------|-----------|---------|
| P_CALC_WEEKLY_POINTS | IN week_id, OUT SYS_REFCURSOR | Calcular puntos |
| P_INSERT_ACTIVITY | IN activity_data, OUT result | Insertar actividad |
| P_GET_RECOMMENDATIONS | IN user_id, OUT recommendations | Obtener sugerencias |
| P_GET_USER_STATS | IN user_id, OUT stats | Estadísticas usuario |

### Índices (10+)
- IDX_USERS_EMAIL ✓
- IDX_ACTIVITIES_USER ✓
- IDX_ACTIVITIES_DATE ✓
- IDX_LEADERBOARD_WEEK ✓
- IDX_LEADERBOARD_RANK ✓
- IDX_RECOMMENDATIONS_USER ✓
- [+4 índices más]

### Secuencias (6)
- SEQ_USERS ✓
- SEQ_TEAMS ✓
- SEQ_TEAM_MEMBERS ✓
- SEQ_ACTIVITIES ✓
- SEQ_LEADERBOARD ✓
- SEQ_RECOMMENDATIONS ✓

---

## 🔗 RELACIONES (Entity-Relationship)

```
T_USERS (1) ──┬─→ (N) T_ACTIVITIES
              ├─→ (N) T_TEAMS            (como líder)
              ├─→ (N) T_TEAM_MEMBERS
              ├─→ (N) T_LEADERBOARD
              └─→ (N) T_RECOMMENDATIONS

T_TEAMS (1) ──┬─→ (N) T_TEAM_MEMBERS
              ├─→ (1) T_USERS            (líder)
              └─────→ LEADERBOARD        (opcional)
```

---

## ✅ POST-INSTALACIÓN

### Verificar Tablas
```sql
SELECT table_name FROM user_tables WHERE table_name LIKE 'T_%' ORDER BY table_name;
-- Resultado esperado: 6 filas (T_ACTIVITIES, T_LEADERBOARD, T_RECOMMENDATIONS, T_TEAM_MEMBERS, T_TEAMS, T_USERS)
```

### Verificar Procedimientos
```sql
SELECT object_name FROM user_objects WHERE object_type = 'PROCEDURE' ORDER BY object_name;
-- Resultado esperado: 4 filas (P_CALC_WEEKLY_POINTS, P_GET_RECOMMENDATIONS, P_GET_USER_STATS, P_INSERT_ACTIVITY)
```

### Verificar Índices
```sql
SELECT COUNT(*) FROM user_indexes;
-- Resultado esperado: 10+ índices
```

### Verificar Django Connection
```bash
cd octofit-tracker/backend
python manage.py dbshell
SQL> SELECT COUNT(*) FROM T_USERS;
-- Resultado esperado: 0 (tabla vacía)
```

---

## 🐛 TROUBLESHOOTING

| Problema | Solución | Documento |
|----------|----------|-----------|
| Conexión rechazada | Verificar listener Oracle | ORACLE_SQLDEVELOPER.instructions.md |
| Permisos insuficientes | Ejecutar como SYSDBA | QUICKSTART.md |
| Tablas no existen | Ejecutar 01_create_tables.sql | WORKFLOW.md |
| Django no conecta | Verificar .env y settings.py | QUICKSTART.md |
| Procedimiento no compila | Ver errores: `SHOW ERRORS` | queries_example.sql |

---

## 📞 SOPORTE

Para problemas o preguntas:

1. **Lectura rápida:** QUICKSTART.md
2. **Detalles:** ORACLE_SQLDEVELOPER.instructions.md
3. **Flujo visual:** WORKFLOW.md
4. **Troubleshooting:** STRUCTURE.md (tabla de problemas)
5. **Queries útiles:** queries_example.sql

---

## 📅 HISTORIAL DE CAMBIOS

| Fecha | Cambio | Versión |
|-------|--------|---------|
| 20/03/2026 | Creación completa SQL Developer + GYM_APP | 1.0 |
| 20/03/2026 | Documentación 100% completa | 1.0 |

---

**Estado:** ✅ **Listo para Usar**  
**Cobertura:** 100% del setup Oracle + SQL Developer  
**Últimas:** 20/03/2026  

---

## 🎓 Siguientes Pasos

Después de completar el setup:

1. ✅ Crear datos de prueba con Django fixtures
2. ✅ Implementar autenticación JWT
3. ✅ Crear endpoints REST de API
4. ✅ Conectar Frontend React a los endpoints
5. ✅ Testing automático de API
6. ✅ Deployment en producción

**Ver:** octofit_tracker_django_backend.instructions.md

---

**¡Listo para Empezar! 🚀**
