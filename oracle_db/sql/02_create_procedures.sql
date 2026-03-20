/*
Usuario: ADMIN
Fecha: 2024-03-20
Propósito: Crear procedimientos almacenados para Octofit Tracker
Descripción: Procedimientos para operaciones comunes en la aplicación
*/

-- Procedimiento para calcular puntos de rankings
CREATE OR REPLACE PROCEDURE P_CALC_WEEKLY_POINTS (
    P_WEEK_ID IN VARCHAR2
)
IS
    /*
    Propósito: Calcular los puntos semanales para cada usuario basado en sus actividades
    P_WEEK_ID: Semana en formato YYYY-WW
    */
    V_START_DATE DATE;
    V_END_DATE DATE;
    V_USER_ID NUMBER;
BEGIN
    -- Validar parámetros de entrada
    IF P_WEEK_ID IS NULL THEN
        RAISE_APPLICATION_ERROR(-20001, 'P_WEEK_ID no puede ser NULL');
    END IF;

    -- Obtener rango de fechas de la semana
    V_START_DATE := TRUNC(SYSDATE - TO_NUMBER(TO_CHAR(SYSDATE, 'D')) + 2, 'IW');
    V_END_DATE := V_START_DATE + 6;

    -- Loop a través de todos los usuarios activos
    FOR user_rec IN (SELECT USR_ID FROM T_USERS WHERE USR_IS_ACTIVE = 1)
    LOOP
        V_USER_ID := user_rec.USR_ID;
        
        -- Actualizar o insertar registro en leaderboard
        MERGE INTO T_LEADERBOARD tgt
        USING (
            SELECT 
                P_WEEK_ID AS week_id,
                V_USER_ID AS user_id,
                COUNT(*) AS activities_count,
                SUM(NVL(ACT_DURATION_MINUTES, 0)) AS total_duration,
                SUM(NVL(ACT_CALORIES_BURNED, 0)) AS total_calories,
                COUNT(*) * 10 + SUM(NVL(ACT_DURATION_MINUTES, 0)) / 10 AS points
            FROM T_ACTIVITIES
            WHERE ACT_USER_ID = V_USER_ID
            AND ACT_PERFORMED_AT BETWEEN V_START_DATE AND V_END_DATE
        ) src
        ON (tgt.LDB_WEEK_ID = src.week_id AND tgt.LDB_USER_ID = src.user_id)
        WHEN MATCHED THEN
            UPDATE SET 
                LDB_ACTIVITIES_COUNT = src.activities_count,
                LDB_TOTAL_DURATION_MINUTES = src.total_duration,
                LDB_TOTAL_CALORIES = src.total_calories,
                LDB_POINTS = src.points,
                LDB_UPDATED_AT = SYSTIMESTAMP
        WHEN NOT MATCHED THEN
            INSERT (LDB_ID, LDB_WEEK_ID, LDB_USER_ID, LDB_ACTIVITIES_COUNT, 
                   LDB_TOTAL_DURATION_MINUTES, LDB_TOTAL_CALORIES, LDB_POINTS)
            VALUES (SEQ_LEADERBOARD.NEXTVAL, src.week_id, src.user_id, 
                   src.activities_count, src.total_duration, src.total_calories, src.points);
    END LOOP;

    -- Actualizar rankings
    UPDATE T_LEADERBOARD
    SET LDB_RANK = (
        SELECT COUNT(*) + 1
        FROM T_LEADERBOARD ldb2
        WHERE ldb2.LDB_WEEK_ID = T_LEADERBOARD.LDB_WEEK_ID
        AND ldb2.LDB_POINTS > T_LEADERBOARD.LDB_POINTS
    ),
    LDB_UPDATED_AT = SYSTIMESTAMP
    WHERE LDB_WEEK_ID = P_WEEK_ID;

    COMMIT;
    DBMS_OUTPUT.PUT_LINE('Puntos calculados exitosamente para la semana: ' || P_WEEK_ID);

EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        DBMS_OUTPUT.PUT_LINE('Error en P_CALC_WEEKLY_POINTS: ' || SQLCODE || ' - ' || SQLERRM);
        RAISE;
END P_CALC_WEEKLY_POINTS;
/

-- Procedimiento para registrar una nueva actividad
CREATE OR REPLACE PROCEDURE P_INSERT_ACTIVITY (
    P_USER_ID IN NUMBER,
    P_TYPE IN VARCHAR2,
    P_NAME IN VARCHAR2,
    P_DURATION_MINUTES IN NUMBER,
    P_DISTANCE_KM IN NUMBER,
    P_CALORIES IN NUMBER,
    P_INTENSITY IN VARCHAR2,
    P_NOTES IN VARCHAR2,
    P_ACTIVITY_ID OUT NUMBER
)
IS
    /*
    Propósito: Insertar una nueva actividad de usuario
    P_USER_ID: ID del usuario
    P_TYPE: Tipo de actividad (Running, Cycling, etc)
    P_NAME: Nombre de la actividad
    Parámetros de salida: P_ACTIVITY_ID con el ID de la actividad creada
    */
    V_ACTIVITY_ID NUMBER;
BEGIN
    -- Validar parámetros
    IF P_USER_ID IS NULL THEN
        RAISE_APPLICATION_ERROR(-20002, 'P_USER_ID no puede ser NULL');
    END IF;
    
    IF P_TYPE IS NULL THEN
        RAISE_APPLICATION_ERROR(-20003, 'P_TYPE no puede ser NULL');
    END IF;
    
    -- Verificar que el usuario existe
    IF NOT EXISTS (SELECT 1 FROM T_USERS WHERE USR_ID = P_USER_ID) THEN
        RAISE_APPLICATION_ERROR(-20004, 'Usuario no encontrado');
    END IF;

    -- Generar nuevo ID
    V_ACTIVITY_ID := SEQ_ACTIVITIES.NEXTVAL;

    -- Insertar actividad
    INSERT INTO T_ACTIVITIES (
        ACT_ID, ACT_USER_ID, ACT_TYPE, ACT_NAME,
        ACT_DURATION_MINUTES, ACT_DISTANCE_KM, ACT_CALORIES_BURNED,
        ACT_INTENSITY_LEVEL, ACT_NOTES, ACT_PERFORMED_AT
    ) VALUES (
        V_ACTIVITY_ID, P_USER_ID, P_TYPE, P_NAME,
        P_DURATION_MINUTES, P_DISTANCE_KM, P_CALORIES,
        P_INTENSITY, P_NOTES, SYSDATE
    );

    P_ACTIVITY_ID := V_ACTIVITY_ID;
    COMMIT;

EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        DBMS_OUTPUT.PUT_LINE('Error en P_INSERT_ACTIVITY: ' || SQLCODE || ' - ' || SQLERRM);
        RAISE;
END P_INSERT_ACTIVITY;
/

-- Procedimiento para obtener recomendaciones personalizadas
CREATE OR REPLACE PROCEDURE P_GET_RECOMMENDATIONS (
    P_USER_ID IN NUMBER,
    P_CURSOR OUT SYS_REFCURSOR
)
IS
    /*
    Propósito: Obtener recomendaciones personalizadas para un usuario
    P_USER_ID: ID del usuario
    P_CURSOR: Cursor de salida con las recomendaciones
    */
BEGIN
    -- Validar parámetros
    IF P_USER_ID IS NULL THEN
        RAISE_APPLICATION_ERROR(-20005, 'P_USER_ID no puede ser NULL');
    END IF;

    -- Abrir cursor con recomendaciones
    OPEN P_CURSOR FOR
        SELECT 
            REC_ID,
            REC_TYPE,
            REC_TITLE,
            REC_DESCRIPTION,
            REC_INTENSITY,
            REC_ESTIMATED_DURATION_MINUTES,
            REC_REASON,
            REC_STATUS
        FROM T_RECOMMENDATIONS
        WHERE REC_USER_ID = P_USER_ID
        AND REC_STATUS IN ('PENDING', 'VIEWED')
        ORDER BY REC_CREATED_AT DESC;

EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error en P_GET_RECOMMENDATIONS: ' || SQLCODE || ' - ' || SQLERRM);
        RAISE;
END P_GET_RECOMMENDATIONS;
/

-- Procedimiento para obtener estadísticas de usuario
CREATE OR REPLACE PROCEDURE P_GET_USER_STATS (
    P_USER_ID IN NUMBER,
    P_STATS_CURSOR OUT SYS_REFCURSOR
)
IS
    /*
    Propósito: Obtener estadísticas de actividades del usuario
    P_USER_ID: ID del usuario
    P_STATS_CURSOR: Cursor de salida con estadísticas
    */
BEGIN
    -- Validar parámetros
    IF P_USER_ID IS NULL THEN
        RAISE_APPLICATION_ERROR(-20006, 'P_USER_ID no puede ser NULL');
    END IF;

    -- Abrir cursor con estadísticas
    OPEN P_STATS_CURSOR FOR
        SELECT 
            COUNT(*) AS total_activities,
            SUM(ACT_DURATION_MINUTES) AS total_minutes,
            SUM(ACT_DISTANCE_KM) AS total_distance,
            SUM(ACT_CALORIES_BURNED) AS total_calories,
            AVG(ACT_CALORIES_BURNED) AS avg_calories_per_session,
            MAX(ACT_PERFORMED_AT) AS last_activity
        FROM T_ACTIVITIES
        WHERE ACT_USER_ID = P_USER_ID;

EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error en P_GET_USER_STATS: ' || SQLCODE || ' - ' || SQLERRM);
        RAISE;
END P_GET_USER_STATS;
/

COMMIT;
