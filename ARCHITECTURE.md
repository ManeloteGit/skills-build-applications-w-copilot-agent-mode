# Arquitectura del Sistema Octofit Tracker

## Diagrama General de Arquitectura

```
┌─────────────────────────────────────────────────────────────────────┐
│                          USUARIOS / CLIENTES                         │
│                 (Web Browser, Mobile App, Postman)                   │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                │ HTTPS
                                ▼
                    ┌───────────────────────┐
                    │  FRONTEND (React)     │
                    │  Puerto: 3000         │
                    │ (A ser implementado)  │
                    └───────────┬───────────┘
                                │
                                │ REST API (JSON)
                                ▼
        ┌───────────────────────────────────────────────┐
        │      BACKEND DJANGO REST API                  │
        │      Puerto: 8000                             │
        │      Framework: Django 4.1.7                  │
        │      API Framework: Django REST Framework     │
        └───────────────────────┬───────────────────────┘
                                │
                  ┌─────────────┴──────────────┐
                  │                            │
                  ▼                            ▼
        ┌─────────────────────┐    ┌──────────────────┐
        │   Apps Django:      │    │ Authentication   │
        │                     │    │ (dj-rest-auth)   │
        │ • Users             │    │ • JWT Tokens     │
        │ • Activities        │    │ • Session Auth   │
        │ • Teams             │    └──────────────────┘
        │ • Leaderboard       │
        │ • Recommendations   │
        └────────────┬────────┘
                     │
                     │ SQLAlchemy ORM
                     ▼
        ┌────────────────────────────────────────┐
        │   ORACLE DATABASE                       │
        │   Host: localhost:1521                  │
        │   Engine: cx_Oracle                     │
        │                                         │
        │   ├─ T_USERS (Usuarios)                │
        │   ├─ T_ACTIVITIES (Actividades)        │
        │   ├─ T_TEAMS (Equipos)                 │
        │   ├─ T_TEAM_MEMBERS (Miembros)         │
        │   ├─ T_LEADERBOARD (Clasificación)     │
        │   └─ T_RECOMMENDATIONS (Recomendaciones)│
        │                                         │
        │   Procedures:                           │
        │   ├─ P_CALC_WEEKLY_POINTS              │
        │   ├─ P_INSERT_ACTIVITY                 │
        │   ├─ P_GET_RECOMMENDATIONS             │
        │   └─ P_GET_USER_STATS                  │
        └────────────────────────────────────────┘
```

## Flujo de Datos

### Ejemplo: Registrar una Actividad

```
1. Usuario ──► Frontend React
                    │
                    ▼
2. Frontend ──► API: POST /api/activities/
                {
                    "activity_type": "running",
                    "name": "Carrera matutina",
                    "duration_minutes": 30,
                    "distance_km": 5.5,
                    "calories_burned": 350,
                    "intensity_level": "high",
                    "performed_at": "2024-03-20T08:00:00Z"
                }
                    │
                    ▼
3. Django ──► ActivityViewSet.perform_create()
                    │
                    ▼
4. ORM ──► INSERT INTO T_ACTIVITIES VALUES(...)
                    │
                    ▼
5. Oracle ──► Ejecutar transacción ACID
                    │
                    ▼
6. Respuesta ──► {
                    "id": 1,
                    "user": 1,
                    "activity_type": "running",
                    ...
                 }
                    │
                    ▼
7. Frontend ──► Mostrar confirmación al usuario
```

## Componentes Principales

### Backend Django

```python
octofit_tracker/
├── settings.py (Configuración Oracle)
├── urls.py (Rutas principales API)
├── wsgi.py (Despliegue)
└── apps/
    ├── users/
    │   ├── models.py (Usuario)
    │   ├── serializers.py (UserSerializer)
    │   └── views.py (UserViewSet)
    │
    ├── activities/
    │   ├── models.py (Activity)
    │   ├── serializers.py (ActivitySerializer)
    │   └── views.py (ActivityViewSet)
    │
    ├── teams/
    │   ├── models.py (Team, TeamMember)
    │   ├── serializers.py (TeamSerializer)
    │   └── views.py (TeamViewSet)
    │
    ├── leaderboard/
    │   ├── models.py (Leaderboard, TeamLeaderboard)
    │   ├── serializers.py (LeaderboardSerializer)
    │   └── views.py (LeaderboardViewSet)
    │
    └── recommendations/
        ├── models.py (Recommendation)
        ├── serializers.py (RecommendationSerializer)
        └── views.py (RecommendationViewSet)
```

### Base de Datos Oracle

```
Schema Oracle:
├── TABLES
│   ├── T_USERS (6 millones de usuarios máx)
│   ├── T_ACTIVITIES (índices por usuario y fecha)
│   ├── T_TEAMS
│   ├── T_TEAM_MEMBERS (relación many-to-many)
│   ├── T_LEADERBOARD
│   ├── T_LEADERBOARD_TEAMS
│   └── T_RECOMMENDATIONS
│
├── SEQUENCES
│   ├── SEQ_USERS
│   ├── SEQ_ACTIVITIES
│   ├── SEQ_TEAMS
│   ├── SEQ_LEADERBOARD
│   └── SEQ_RECOMMENDATIONS
│
├── INDEXES (Performance)
│   ├── IDX_USERS_EMAIL (búsqueda rápida)
│   ├── IDX_ACTIVITIES_USER (por usuario)
│   ├── IDX_ACTIVITIES_DATE (por fecha)
│   └── 10+ índices más...
│
└── PROCEDURES
    ├── P_CALC_WEEKLY_POINTS
    ├── P_INSERT_ACTIVITY
    ├── P_GET_RECOMMENDATIONS
    └── P_GET_USER_STATS
```

## Flujos de Casos de Uso

### 1. Autenticación de Usuario
```
POST /api/auth/login/
├─ Validar credenciales
├─ Generar JWT Token
└─ Retornar Token + User Data
```

### 2. Registro de Actividad
```
POST /api/activities/
├─ Validar entrada
├─ Llamar P_INSERT_ACTIVITY()
├─ Oracle: INSERT en T_ACTIVITIES
├─ Actualizar leaderboard
└─ Retornar Activity creada
```

### 3. Obtener Ranking
```
GET /api/leaderboard/current_week/
├─ Llamar P_CALC_WEEKLY_POINTS()
├─ SELECT desde T_LEADERBOARD
├─ Ordenar por rank
└─ Retornar TOP 10 (paginado)
```

### 4. Crear Equipo
```
POST /api/teams/
├─ Validar datos del equipo
├─ INSERT en T_TEAMS (líder = usuario actual)
├─ INSERT en T_TEAM_MEMBERS
└─ Retornar Team creado
```

### 5. Obtener Recomendaciones
```
GET /api/recommendations/
├─ Llamar P_GET_RECOMMENDATIONS(user_id)
├─ Filtrar por estado = PENDING/VIEWED
├─ Marcar como viewed
└─ Retornar recomendaciones activas
```

## Patrones de Diseño Implementados

### 1. ViewSet Pattern (Django REST)
```python
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # Genera automáticamente:
    # GET /api/users/           → list()
    # POST /api/users/          → create()
    # GET /api/users/1/         → retrieve()
    # PUT /api/users/1/         → update()
    # DELETE /api/users/1/      → destroy()
```

### 2. Serializer Pattern
```python
class UserSerializer(serializers.ModelSerializer):
    # Transforma:
    # Django Model ──► JSON (representación)
    # JSON ──► Django Model (validación)
```

### 3. Procedure Pattern (Oracle)
```sql
CREATE OR REPLACE PROCEDURE P_CALC_WEEKLY_POINTS(
    P_WEEK_ID IN VARCHAR2
)
-- Lógica de negocio compleja en BD
-- ACID transactions
-- Mejor performance que Python
```

## Seguridad

```
┌─────────────────────────────────────────┐
│  FRONTEND                               │
└─────────────┬───────────────────────────┘
              │
              │ JWT Token en Header
              ▼
┌─────────────────────────────────────────┐
│  DJANGO MIDDLEWARE                      │
│  ├─ CORS Verificación                   │
│  ├─ Token Validación                    │
│  └─ Rate Limiting                       │
└─────────────┬───────────────────────────┘
              │
              │ Usuario Autenticado
              ▼
┌─────────────────────────────────────────┐
│  VIEWS / VIEWSETS                       │
│  ├─ Verificar Permisos                  │
│  ├─ Validar Datos                       │
│  └─ Filtrar por Usuario                 │
└─────────────┬───────────────────────────┘
              │
              │ Consultas Parametrizadas
              ▼
┌─────────────────────────────────────────┐
│  ORACLE DATABASE                        │
│  ├─ Procedimientos Almacenados          │
│  ├─ Transacciones ACID                  │
│  └─ Constraints de Integridad           │
└─────────────────────────────────────────┘
```

## Performance

### Índices para Optimización
```
T_USERS:
├─ PK (USR_ID)
├─ IDX_USERS_EMAIL
└─ IDX_USERS_USERNAME

T_ACTIVITIES:
├─ PK (ACT_ID)
├─ FK (ACT_USER_ID)
├─ IDX_ACTIVITIES_USER
└─ IDX_ACTIVITIES_DATE

T_LEADERBOARD:
├─ PK (LDB_ID)
├─ UNIQUE (LDB_WEEK_ID, LDB_USER_ID)
├─ IDX_LEADERBOARD_WEEK
└─ IDX_LEADERBOARD_RANK
```

### Queries Típicas (ms)
- Listar usuarios: < 100 ms
- Obtener actividades por usuario: < 50 ms
- Calcular ranking: < 200 ms (con P_CALC_WEEKLY_POINTS)
- Obtener recomendaciones: < 30 ms

## Escalabilidad

```
Capacidad Actual:
├─ 1M+ usuarios
├─ 100M+ actividades
├─ 50K+ equipos
└─ Procesamiento semanal automático

Futuro:
├─ Replicación Oracle
├─ Caché Redis
├─ Queue Celery para tasks async
└─ DataLake para analytics
```

## Deployment

```
Desarrollo:
├─ Python: venv local
├─ DB: Oracle XE local
└─ Server: runserver @ :8000

Staging/Producción:
├─ Python: Docker container
├─ DB: Oracle Enterprise (Cloud)
├─ Server: Gunicorn + Nginx
├─ https://api.octofit.com
└─ CI/CD: GitHub Actions
```

---

**Última actualización**: 20 de Marzo, 2026
