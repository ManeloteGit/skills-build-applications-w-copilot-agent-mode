---
applyTo: "oracle_db/**"
---
# Script de Oracle
### nomenclarura de tablas y campos
    Las tablas deben tener un prefijo `T' para tablas
    Los campos de una tabla deben tener un acronimo de 3 letras segun nombre de la tabla seguido de un guion bajo y el nombre del campo, por ejemplo `EMP_ID' para el campo ID de la tabla EMPLOYEES
    Tabals y campos deben estar en mayusculas y tener un comentario que describa su función
    Para vistas empezar por `W'
    Para procedimientos almacenados empezar por `P'
    Para funciones empezar por `F'
    Para Paquetes empezar por `PKG'
    Para variables empezar por `V'
    Para Constantes empezar por `K'
### Estructura de un procedimiento almacenado 
    Un procedimiento almacenado debe tener la siguiente estructura:
    0. Preámbulo explicativo del procedimiento almacenado, incluyendo su propósito, parámetros de entrada y salida, y cualquier consideración special. Ejemplo:
    ```/*
    Usuario: MNG
    Fecha: 2024-06-01
    Propósito: Recuperar empleados de un departamento específico
    P_RECUERPA_EMPLEADOS(P_DEP_ID IN NUMBER, P_DEP_NAME IN VARCHAR2, P_EMPLOYEES OUT SYS_REFCURSOR) IS
    -- Parámetros:
    -- P_DEP_ID: ID del departamento (entrada)
    -- P_DEP_NAME: Nombre del departamento (entrada)  
    -- P_EMPLOYEES: Cursor de salida que contiene los empleados del departamento
    */`

    1. Declaración de variables
    2. Bloque de código principal
    3. Manejo de errores
    4. Comentarios explicativos para cada sección del código    
    
### seguridad del codigo
    Evitar el uso de SQL dinámico para prevenir inyecciones SQL
    Validar y sanitizar todas las entradas de usuario antes de usarlas en consultas SQL
    Utilizar procedimientos almacenados para encapsular la lógica de acceso a datos y limitar el acceso directo a las tablas
    Implementar controles de acceso adecuados para los procedimientos almacenados, asegurando que solo los usuarios autorizados puedan ejecutarlos
    Evitar el uso de privilegios excesivos para los usuarios de la base de datos, otorgando solo los permisos necesarios para realizar sus tareas