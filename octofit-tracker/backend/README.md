# Octofit Tracker - Django Backend

Backend para la aplicación Octofit Tracker con Oracle Database.

## Requisitos Previos

- Python 3.8+
- Oracle Database 11g+ (o Oracle Express Edition)
- Oracle Client Libraries

## Configuración Inicial

### 1. Crear Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 2. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar Variables de Entorno

Copiar `.env.example` a `.env` y configurar:

```bash
cp .env.example .env
```

Editar `.env` con tus credenciales de Oracle Database.

### 4. Crear Estructura de Base de Datos en Oracle

Ejecutar los scripts SQL en Oracle:

```bash
# Conectarse a Oracle SQL Developer o sqlplus
sqlplus usuario/contraseña@host:puerto/database

-- Ejecutar los scripts en orden:
@oracle_db/sql/01_create_tables.sql
@oracle_db/sql/02_create_procedures.sql
```

### 5. Ejecutar Migraciones de Django

```bash
python manage.py migrate
```

### 6. Crear Superusuario

```bash
python manage.py createsuperuser
```

Ingresa los datos del administrador.

### 7. Cargar Datos Iniciales (Opcional)

```bash
python manage.py loaddata fixtures/initial_data.json
```

## Ejecutar Servidor de Desarrollo

```bash
python manage.py runserver 0.0.0.0:8000
```

El servidor estará disponible en: http://localhost:8000

Para Codespaces: https://{CODESPACE_NAME}-8000.app.github.dev

## API Endpoints

- **Usuarios**: `/api/users/`
- **Actividades**: `/api/activities/`
- **Equipos**: `/api/teams/`
- **Clasificación**: `/api/leaderboard/`
- **Recomendaciones**: `/api/recommendations/`
- **Admin**: `/admin/`

## Comandos Útiles

### Crear aplicación nueva en Django

```bash
python manage.py startapp nombre_app octofit_tracker/apps/nombre_app
```

### Hacer migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### Recolectar archivos estáticos

```bash
python manage.py collectstatic
```

### Ejecutar shell de Python

```bash
python manage.py shell
```

### Tests

```bash
python manage.py test
```

## Estructura del Proyecto

```
octofit-tracker/backend/
├── manage.py
├── requirements.txt
├── .env.example
├── octofit_tracker/
│   ├── settings.py      # Configuración de Django
│   ├── urls.py          # URLs principales
│   ├── wsgi.py
│   ├── asgi.py
│   └── apps/
│       ├── users/       # Gestión de usuarios
│       ├── activities/  # Registro de actividades
│       ├── teams/       # Gestión de equipos
│       ├── leaderboard/ # Clasificación competitiva
│       └── recommendations/ # Recomendaciones personalizadas
└── venv/
```

## Documentación de Oracle Database

Ver `/oracle_db/` para:
- Scripts SQL de creación de tablas
- Procedimientos almacenados
- Guías de nomenclatura y estándares OracleSQL

## Seguridad

- Cambiar `SECRET_KEY` en settings.py para producción
- No compartir credenciales de Oracle
- Usar HTTPS en producción
- Implementar rate limiting
- Validar todas las entradas de usuario

## Solución de Problemas

### Conexión a Oracle rechazada

Verificar:
- Oracle está ejecutándose
- Credenciales en .env son correctas
- Host y puerto son accesibles
- Oracle Client está instalado

### Errores de migración

```bash
# Ver estado de migraciones
python manage.py showmigrations

# Revertir migraciones
python manage.py migrate app_name zero
```

### Puerto en uso

```bash
# Usar puerto diferente
python manage.py runserver 0.0.0.0:8001
```

## Contribución

1. Crear rama feature: `git checkout -b feature/mi-feature`
2. Commit cambios: `git commit -am 'Agregar feature'`
3. Push a la rama: `git push origin feature/mi-feature`
4. Abrir Pull Request

## Licencia

Ver LICENSE en la raíz del proyecto.
