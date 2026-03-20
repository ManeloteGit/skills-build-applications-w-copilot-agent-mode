/*
Usuario: ADMIN
Fecha: 2024-03-20
Propósito: Crear esquema GYM_APP para Octofit Tracker en Oracle Database
Descripción: Script para crear el usuario/esquema GYM_APP con permisos necesarios
Ejecución: Conectarse como SYS o DBA antes de ejecutar este script
*/

-- ============================================================
-- CREAR USUARIO GYM_APP
-- ============================================================

-- Crear usuario con contraseña
CREATE USER GYM_APP IDENTIFIED BY gym_app_password;

-- Otorgar permisos de tablespace ilimitado
GRANT UNLIMITED TABLESPACE TO GYM_APP;

-- Permisos básicos de sesión
GRANT CREATE SESSION TO GYM_APP;

-- Permisos para crear objetos de base de datos
GRANT CREATE TABLE TO GYM_APP;
GRANT CREATE SEQUENCE TO GYM_APP;
GRANT CREATE PROCEDURE TO GYM_APP;
GRANT CREATE TRIGGER TO GYM_APP;
GRANT CREATE VIEW TO GYM_APP;
GRANT CREATE INDEX TO GYM_APP;
GRANT CREATE FUNCTION TO GYM_APP;
GRANT CREATE PACKAGE TO GYM_APP;

-- Permisos para modificar sesiones (necesario para algunos triggers)
GRANT ALTER SESSION TO GYM_APP;

-- Permisos para crear sinónimos
GRANT CREATE SYNONYM TO GYM_APP;

-- Cambiar conexión a GYM_APP
CONNECT GYM_APP/gym_app_password;

-- Verificar que estamos conectados como GYM_APP
SHOW USER;

-- ============================================================
-- Crear tablespace temporal si es necesario
-- ============================================================
-- Nota: Comentado por defecto, descomentar si es necesario
/*
CREATE TEMPORARY TABLESPACE temp_gym_app 
TEMPFILE '/u01/oradata/ORCLCDB/temp_gym_app.dbf' 
SIZE 100M;

ALTER USER GYM_APP TEMPORARY TABLESPACE temp_gym_app;
*/

COMMIT;

-- ============================================================
-- Fin del script de creación de esquema
-- ============================================================
