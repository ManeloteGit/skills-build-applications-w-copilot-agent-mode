-- ============================================================
-- GUÍA RÁPIDA DE CONSULTAS - Esquema GYM_APP
-- ============================================================
-- Comandos SQL comunes para inspeccionar y trabajar con 
-- el esquema GYM_APP en Oracle Database
-- ============================================================

-- ============================================================
-- 1. VERIFICAR TABLAS CREADAS
-- ============================================================

-- Ver todas las tablas del esquema actual
SELECT table_name FROM user_tables ORDER BY table_name;

-- Ver estructura de una tabla específica
DESC T_USERS;
DESC T_ACTIVITIES;
DESC T_TEAMS;
DESC T_TEAM_MEMBERS;
DESC T_LEADERBOARD;
DESC T_RECOMMENDATIONS;

-- Ver todas las tablas con sus propietarios
SELECT owner, table_name FROM dba_tables 
WHERE owner = 'GYM_APP' 
ORDER BY owner, table_name;

-- ============================================================
-- 2. VERIFICAR PROCEDIMIENTOS Y FUNCIONES
-- ============================================================

-- Ver procedimientos almacenados
SELECT object_name, object_type 
FROM user_objects 
WHERE object_type = 'PROCEDURE' 
ORDER BY object_name;

-- Ver todas las funciones
SELECT object_name, object_type 
FROM user_objects 
WHERE object_type = 'FUNCTION' 
ORDER BY object_name;

-- Ver código fuente de un procedimiento
SELECT text FROM user_source 
WHERE name = 'P_CALC_WEEKLY_POINTS' 
ORDER BY line;

-- ============================================================
-- 3. VERIFICAR ÍNDICES
-- ============================================================

-- Ver todos los índices del esquema
SELECT index_name, table_name, uniqueness 
FROM user_indexes 
WHERE table_owner = 'GYM_APP' 
ORDER BY table_name, index_name;

-- Ver columnas de un índice
SELECT index_name, column_name, column_position 
FROM user_ind_columns 
WHERE index_owner = 'GYM_APP' 
ORDER BY index_name, column_position;

-- ============================================================
-- 4. VERIFICAR SECUENCIAS
-- ============================================================

-- Ver todas las secuencias
SELECT sequence_name, min_value, max_value, increment_by, cycle_flag 
FROM user_sequences 
ORDER BY sequence_name;

-- Obtener el siguiente valor de una secuencia
SELECT SEQ_USERS.NEXTVAL FROM dual;
SELECT SEQ_ACTIVITIES.NEXTVAL FROM dual;
SELECT SEQ_TEAMS.NEXTVAL FROM dual;

-- ============================================================
-- 5. ESTADÍSTICAS DE TABLAS
-- ============================================================

-- Contar registros por tabla
SELECT 
    table_name, 
    num_rows 
FROM user_tables 
WHERE table_name LIKE 'T_%' 
ORDER BY table_name;

-- Ver espacio utilizado por tablas
SELECT 
    segment_name as table_name,
    segment_type,
    bytes / 1024 / 1024 as size_mb
FROM user_segments 
WHERE segment_type = 'TABLE' 
ORDER BY bytes DESC;

-- ============================================================
-- 6. CONSTRAINTS
-- ============================================================

-- Ver primary keys
SELECT constraint_name, table_name, constraint_type 
FROM user_constraints 
WHERE constraint_type = 'P' 
ORDER BY table_name;

-- Ver foreign keys
SELECT constraint_name, table_name, r_owner, r_constraint_name 
FROM user_constraints 
WHERE constraint_type = 'R' 
ORDER BY table_name;

-- Ver unique constraints
SELECT constraint_name, table_name 
FROM user_constraints 
WHERE constraint_type = 'U' 
ORDER BY table_name;

-- ============================================================
-- 7. INFORMACIÓN DE USUARIO/ESQUEMA
-- ============================================================

-- Ver usuario actual y detalles
SHOW USER;
SELECT username, account_status, created FROM dba_users 
WHERE username = 'GYM_APP';

-- Ver permisos del usuario actual
SELECT privilege FROM user_sys_privs ORDER BY privilege;

-- Ver permisos de sistema
SELECT privilege FROM dba_sys_privs 
WHERE grantee = 'GYM_APP' 
ORDER BY privilege;

-- Ver roles asignados
SELECT granted_role FROM dba_role_privs 
WHERE grantee = 'GYM_APP';

-- ============================================================
-- 8. SINCRONIZACIÓN Y MANTENIMIENTO
-- ============================================================

-- Recopilar estadísticas para optimización
EXEC DBMS_STATS.GATHER_TABLE_STATS('GYM_APP', 'T_USERS');
EXEC DBMS_STATS.GATHER_TABLE_STATS('GYM_APP', 'T_ACTIVITIES');
EXEC DBMS_STATS.GATHER_TABLE_STATS('GYM_APP', 'T_TEAMS');

-- Recopilar estadísticas de todo el esquema
BEGIN
  DBMS_STATS.GATHER_SCHEMA_STATS('GYM_APP');
END;
/

-- Ver últimas recopilaciones de estadísticas
SELECT 
    table_name, 
    last_analyzed, 
    num_rows 
FROM user_tables 
ORDER BY last_analyzed DESC NULLS LAST;

-- ============================================================
-- 9. DIAGNÓSTICOS
-- ============================================================

-- Ver errores de compilación
SHOW ERRORS;

-- Ver errores de un procedimiento específico
SHOW ERRORS PROCEDURE P_CALC_WEEKLY_POINTS;

-- Ver columnas no utilizadas
SELECT 
    table_name, 
    column_name, 
    data_type 
FROM user_tab_columns 
WHERE table_name LIKE 'T_%' 
ORDER BY table_name, column_id;

-- Ver espacios en disco disponible
SELECT tablespace_name, sum(bytes)/1024/1024 as free_mb 
FROM user_free_space 
GROUP BY tablespace_name;

-- ============================================================
-- 10. LIMPIAR Y RESETEAR (CUIDADO!)
-- ============================================================

-- Eliminar todos los registros de una tabla (pero se mantiene la estructura)
-- DELETE FROM T_USERS;
-- COMMIT;

-- Truncar una tabla (más eficiente, pero no se puede hacer rollback)
-- TRUNCATE TABLE T_USERS;

-- Respaldar datos antes de eliminar
/*
CREATE TABLE T_USERS_BACKUP AS SELECT * FROM T_USERS;
DELETE FROM T_USERS;
COMMIT;
*/

-- Reconstruir índice
ALTER INDEX IDX_USERS_EMAIL REBUILD;

-- Reorganizar tabla (liberar espacio no utilizado)
ALTER TABLE T_USERS SHRINK SPACE;

-- ============================================================
-- 11. EJEMPLOS DE CONSULTAS DE NEGOCIO
-- ============================================================

-- Top 10 usuarios más activos
SELECT 
    u.USR_ID, 
    u.USR_USERNAME, 
    COUNT(a.ACT_ID) as activity_count,
    SUM(a.ACT_CALORIES_BURNED) as total_calories
FROM T_USERS u
LEFT JOIN T_ACTIVITIES a ON u.USR_ID = a.ACT_USER_ID
GROUP BY u.USR_ID, u.USR_USERNAME
ORDER BY activity_count DESC
FETCH FIRST 10 ROWS ONLY;

-- Actividades por tipo
SELECT 
    ACT_TYPE, 
    COUNT(*) as total,
    AVG(ACT_DURATION_MINUTES) as avg_duration,
    SUM(ACT_CALORIES_BURNED) as total_calories
FROM T_ACTIVITIES
GROUP BY ACT_TYPE
ORDER BY total DESC;

-- Miembros por equipo
SELECT 
    t.TEM_ID,
    t.TEM_NAME, 
    COUNT(tm.TMB_ID) as member_count,
    u.USR_USERNAME as leader
FROM T_TEAMS t
LEFT JOIN T_TEAM_MEMBERS tm ON t.TEM_ID = tm.TMB_TEAM_ID
LEFT JOIN T_USERS u ON t.TEM_LEADER_ID = u.USR_ID
GROUP BY t.TEM_ID, t.TEM_NAME, u.USR_USERNAME
ORDER BY member_count DESC;

-- Leaderboard actual
SELECT 
    LDB_RANK,
    u.USR_USERNAME,
    LDB_POINTS,
    LDB_ACTIVITIES_COUNT,
    LDB_TOTAL_CALORIES
FROM T_LEADERBOARD lb
JOIN T_USERS u ON lb.LDB_USER_ID = u.USR_ID
WHERE LDB_WEEK_ID = TO_CHAR(TRUNC(SYSDATE, 'IW'), 'YYYYWW')
ORDER BY LDB_RANK
FETCH FIRST 20 ROWS ONLY;

-- ============================================================
-- FIN DE GUÍA RÁPIDA
-- ============================================================
