# Cambio a Oracle Database - Resumen

**Fecha**: 20 de Marzo, 2026  
**Cambio**: MongoDB → Oracle Database  
**Estado**: ✅ Completado

## Descripción del Cambio

La base de datos del proyecto Octofit Tracker ha sido **migrada de MongoDB a Oracle Database**. Esta es una base de datos relacional empresarial más robusta y con mejor soporte para aplicaciones de producción.

## Por qué Oracle Database

✅ **Estabilidad**: Probada en entornos empresariales  
✅ **Escalabilidad**: Maneja millones de registros eficientemente  
✅ **Seguridad**: Características avanzadas de seguridad y auditoría  
✅ **Rendimiento**: Índices y optimizaciones potentes  
✅ **ACID**: Transacciones garantizadas  
✅ **Procedimientos Almacenados**: Lógica de negocio en la BD  

## Cambios Realizados

### 1. Backend Django
- ✅ Configuración actualizada para Oracle (`cx_Oracle`)
- ✅ Modelos ORM compatibles con relaciones SQL
- ✅ 5 aplicaciones principales creadas
- ✅ Serializers para API REST
- ✅ Vistas y ViewSets listos

### 2. Estructura de Base de Datos
- ✅ 6 tablas principales creadas
- ✅ Secuencias para auto-increment
- ✅ 10+ índices para optimización
- ✅ 4 procedimientos almacenados

### 3. Modelos de Datos

#### Usuarios (T_USERS)
- Authenticación y perfil
- Información física (altura, peso, edad)
- Nivel de aptitud física
- Foto de perfil

#### Actividades (T_ACTIVITIES)
- Registro de ejercicios
- Tipo de actividad
- Duración, distancia, calorías
- Intensidad del ejercicio

#### Equipos (T_TEAMS + T_TEAM_MEMBERS)
- Creación de equipos
- Gestión de miembros
- Roles (miembro, entrenador, gerente)
- Liderazgo de equipos

#### Leaderboard (T_LEADERBOARD)
- Clasificación competitiva semanal
- Ranking por puntos
- Estadísticas agregadas
- Historial de desempeño

#### Recomendaciones (T_RECOMMENDATIONS)
- Sugerencias personalizadas
- Tipos: Entrenamiento, Descanso, Recuperación
- Seguimiento de aceptación/rechazo
- Historial de completadas

## Estructura de Archivos

```
project/
├── octofit-tracker/
│   └── backend/
│       ├── manage.py
│       ├── requirements.txt          ← cx_Oracle agregado
│       ├── .env.example
│       ├── README.md
│       ├── octofit_tracker/
│       │   ├── settings.py           ← Oracle Database configurado
│       │   ├── urls.py
│       │   ├── wsgi.py
│       │   └── apps/
│       │       ├── users/            ← Gestión de usuarios
│       │       ├── activities/       ← Registro de actividades
│       │       ├── teams/            ← Gestión de equipos
│       │       ├── leaderboard/      ← Clasificación competitiva
│       │       └── recommendations/  ← Sugerencias personalizadas
│       └── venv/
│
└── oracle_db/
    ├── README.md
    └── sql/
        ├── 01_create_tables.sql      ← Tablas y secuencias
        └── 02_create_procedures.sql  ← Procedimientos almacenados
```

## Requisitos de Instalación

### Dependencias Python
```bash
pip install -r octofit-tracker/backend/requirements.txt
```

**Nuevos paquetes agregados:**
- `cx-Oracle==8.3.0` - Driver Oracle Python
- `psycopg2-binary==2.9.9` - Driver PostgreSQL (compatible)

### Oracle Database
- Oracle Database 11g+ 
- O Oracle Express Edition (XE) gratis
- Oracle Client Libraries (para conexiones remotas)

## Configuración

### 1. Variables de Entorno
```bash
cd octofit-tracker/backend
cp .env.example .env
# Editar .env con credenciales Oracle
```

### 2. Crear esquema en Oracle
```bash
# Ejecutar scripts SQL
sqlplus usuario/password@host:1521/database @oracle_db/sql/01_create_tables.sql
sqlplus usuario/password@host:1521/database @oracle_db/sql/02_create_procedures.sql
```

### 3. Ejecutar servidor Django
```bash
cd octofit-tracker/backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

## API Endpoints

```
GET  /api/users/                    # Listar usuarios
POST /api/users/                    # Crear usuario
GET  /api/activities/               # Listar actividades
POST /api/activities/               # Registrar actividad
GET  /api/teams/                    # Listar equipos
POST /api/teams/                    # Crear equipo
GET  /api/leaderboard/              # Ver clasificación
GET  /api/recommendations/          # Obtener sugerencias
```

## Características Nuevas

✨ **Procedimientos Almacenados**
- Cálculo automático de puntos semanales
- Obtención de estadísticas de usuario
- Inserción validada de actividades

✨ **Índices Optimizados**
- Búsquedas rápidas por usuario
- Acceso eficiente a actividades
- Queries de leaderboard ultrarrápidas

✨ **Validación en Base de Datos**
- Constraints de integridad
- Transacciones ACID garantizadas
- Auditoría integrada

## Documentación

📖 **Backend**: Ver [octofit-tracker/backend/README.md](octofit-tracker/backend/README.md)  
📖 **Oracle DB**: Ver [oracle_db/README.md](oracle_db/README.md)  

## Próximos Pasos

1. ✅ Backend con Oracle Database **[COMPLETADO]**
2. ⏳ Frontend React (usando los endpoints del API)
3. ⏳ Deployment en producción
4. ⏳ Monitoreo y optimización

## Compatibilidad

| Componente | Versión |
|-----------|---------|
| Python | 3.8+ |
| Django | 4.1.7 |
| Oracle | 11g+ |
| Django REST Framework | 3.14.0 |

## Migración desde MongoDB

Si tenías datos en MongoDB anteriormente:

1. Exportar datos de MongoDB a JSON
2. Transformar formato según modelos Django
3. Importar con fixtures de Django
4. Validar integridad de datos

```bash
python manage.py loaddata fixtures/usuarios.json
```

## Soporte y Troubleshooting

### Conexión a Oracle rechazada
- Verificar Oracle está ejecutándose
- Confirmar credenciales en .env
- Verificar puerto 1521 está abierto

### ImportError: No module named 'cx_Oracle'
```bash
pip install cx-Oracle==8.3.0
```

### Migraciones fallan
```bash
python manage.py showmigrations
python manage.py migrate --run-syncdb
```

## Estándares y Mejores Prácticas

- Nomenclatura Oracle: Prefijos T_, P_, W_, etc.
- Comentarios en todas las tablas y procedimientos
- Índices en claves foráneas
- Transacciones ACID
- Validación en múltiples capas

## Licencia

Ver archivo LICENSE en la raíz del proyecto.

---

**¿Preguntas?** Revisa la documentación completa en [README.md](README.md)
