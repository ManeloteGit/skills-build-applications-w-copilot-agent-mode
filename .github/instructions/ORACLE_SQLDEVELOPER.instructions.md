---
applyTo: "oracle_db/**"
---
# SQL Developer - Configuración y Conexión Oracle 21C

## 1. Instalación de SQL Developer

### Requerimientos
- Java JDK 11 o superior instalado
- Oracle Database 21C ejecutándose localmente
- 500 MB de espacio disponible

### Descarga e Instalación

#### En Linux (Ubuntu/Debian):
```bash
# Descargar SQL Developer
wget https://download.oracle.com/otn/java/sqldeveloper/sqldeveloper-23.1.0.087.1900-no-jdk.zip

# Descomprimir
unzip sqldeveloper-23.1.0.087.1900-no-jdk.zip

# Mover a ubicación apropiada
sudo mv sqldeveloper /opt/

# Dar permisos de ejecución
chmod +x /opt/sqldeveloper/sqldeveloper.sh

# Crear acceso directo
sudo ln -s /opt/sqldeveloper/sqldeveloper.sh /usr/local/bin/sqldeveloper
```

#### Con Docker (Alternativa):
```bash
docker pull gvenzl/sqldeveloper:latest
docker run -d --name sqldeveloper \
  -p 5900:5900 \
  -e DISPLAY=host.docker.internal:0 \
  gvenzl/sqldeveloper:latest
```

### Iniciar SQL Developer
```bash
/opt/sqldeveloper/sqldeveloper.sh
```

---

## 2. Crear Conexión a Oracle 21C Local

### Paso 1: Abrir SQL Developer
Ejecutar: `sqldeveloper`

### Paso 2: Nueva Conexión
1. Ir a: **Connections → New Connection**
2. Completar datos:

```
Connection Name:      GYM_APP_LOCAL
Username:             sys
Password:             <tu-contraseña-oracle>
Connection Type:      Basic
Hostname:             localhost
Port:                 1521
SID:                  ORCLCDB
Role:                 SYSDBA
```

### Paso 3: Testear Conexión
- Click en botón: **Test**
- Debe mostrar: "Success"
- Click: **Save**
- Click: **Connect**

---

## 3. Crear Esquema GYM_APP

### Opción A: Usar SQL Developer (GUI)

1. **Con la conexión SYSDBA abierta**, ejecutar script:
```sql
-- Crear esquema GYM_APP
CREATE USER GYM_APP IDENTIFIED BY gym_app_password;

-- Otorgar permisos
GRANT UNLIMITED TABLESPACE TO GYM_APP;
GRANT CREATE SESSION TO GYM_APP;
GRANT CREATE TABLE TO GYM_APP;
GRANT CREATE SEQUENCE TO GYM_APP;
GRANT CREATE PROCEDURE TO GYM_APP;
GRANT CREATE TRIGGER TO GYM_APP;
GRANT CREATE VIEW TO GYM_APP;
GRANT CREATE INDEX TO GYM_APP;
GRANT ALTER SESSION TO GYM_APP;
```

2. **Crear nueva conexión para GYM_APP**:
```
Connection Name:      GYM_APP_USER
Username:             GYM_APP
Password:             gym_app_password
Connection Type:      Basic
Hostname:             localhost
Port:                 1521
SID:                  ORCLCDB
Role:                 (dejar vacío)
```

### Opción B: Usar Terminal SQLPlus

```bash
# Conectarse como SYSDBA
sqlplus sys as sysdba
# Ingresar contraseña

# En SQLPlus, ejecutar:
CREATE USER GYM_APP IDENTIFIED BY gym_app_password;
GRANT UNLIMITED TABLESPACE TO GYM_APP;
GRANT CREATE SESSION TO GYM_APP;
GRANT CREATE TABLE TO GYM_APP;
GRANT CREATE SEQUENCE TO GYM_APP;
GRANT CREATE PROCEDURE TO GYM_APP;
GRANT CREATE TRIGGER TO GYM_APP;
GRANT CREATE VIEW TO GYM_APP;
GRANT CREATE INDEX TO GYM_APP;
GRANT ALTER SESSION TO GYM_APP;

exit;
```

---

## 4. Ejecutar Scripts de Creación en GYM_APP

### En SQL Developer:

#### Paso 1: Conectarse como GYM_APP
- Seleccionar conexión: **GYM_APP_USER**
- Click en **Connect**

#### Paso 2: Abrir Script de Tablas
1. **File → Open**
2. Navegar a: `oracle_db/sql/00_create_schema.sql`
3. Click: **Open**
4. Click: **Run Script** (o Ctrl+Enter)

#### Paso 3: Abrir Script de Procedimientos
1. **File → Open**
2. Navegar a: `oracle_db/sql/01_create_tables.sql`
3. Click: **Open**
4. Click: **Run Script**

#### Paso 4: Crear Procedimientos
1. **File → Open**
2. Navegar a: `oracle_db/sql/02_create_procedures.sql`
3. Click: **Open**
4. Click: **Run Script**

---

## 5. Verificar Creación de Objetos

### En SQL Developer, ejecutar:

```sql
-- Ver tablas creadas
SELECT table_name FROM user_tables ORDER BY table_name;

-- Ver procedimientos
SELECT object_name FROM user_objects 
WHERE object_type = 'PROCEDURE' ORDER BY object_name;

-- Ver secuencias
SELECT sequence_name FROM user_sequences ORDER BY sequence_name;

-- Contar registros por tabla
SELECT 
    table_name, 
    num_rows 
FROM user_tables 
ORDER BY table_name;
```

---

## 6. Exportar/Importar Datos (Opcional)

### Exportar esquema completo:
```sql
-- En SQL Developer
-- Right-click en conexión GYM_APP_USER
-- Seleccionar: Tools → Export
-- Elegir formato: SQL Script
-- Guardar como: gym_app_export.sql
```

### Importar en otra instancia:
```sql
-- En SQL Developer
-- File → Open → gym_app_export.sql
-- Run Script
```

---

## 7. Troubleshooting

### Conexión rechazada
```
Error: ORA-12514: TNS:listener does not currently know of service requested
```

**Solución**:
```bash
# Verificar Oracle listener
ps aux | grep -i oracle

# Verificar puerto 1521
netstat -tlnp | grep 1521

# Reiniciar Oracle (si es necesario)
sudo systemctl restart oracle-database
```

### Permisos insuficientes
```
Error: ORA-01031: insufficient privileges
```

**Solución**: Conectarse como SYSDBA y ejecutar GRANTs nuevamente

### SQL Developer no inicia
```bash
# Limpiar caché
rm -rf ~/.sqldeveloper

# Ejecutar con logs
/opt/sqldeveloper/sqldeveloper.sh &> sqldeveloper.log

# Ver logs
tail -f sqldeveloper.log
```

---

## 8. Variables de Entorno (Opcional)

Para facilitar conexiones desde terminal:

```bash
# Agregar a ~/.bashrc
export ORACLE_HOME=/u01/app/oracle/product/21c/dbhome_1
export ORACLE_SID=ORCLCDB
export PATH=$ORACLE_HOME/bin:$PATH
export LD_LIBRARY_PATH=$ORACLE_HOME/lib:$LD_LIBRARY_PATH

# Recargar
source ~/.bashrc

# Verificar
sqlplus -v
```

---

## 9. Consideraciones de Seguridad

### NO usar en Producción:
- Las credenciales en texto plano son solo para desarrollo local
- Cambiar contraseña predeterminada: `gym_app_password`

### Para Producción:
```sql
-- Usar hash de contraseña
ALTER USER GYM_APP IDENTIFIED BY VALUES 'hash_de_contraseña';

-- Limitar sesiones
ALTER PROFILE DEFAULT LIMIT SESSIONS_PER_USER 3;

-- Auditoría
AUDIT CREATE TABLE BY GYM_APP;
AUDIT DML ON GYM_APP.T_USERS;
```

---

## 10. Integración con Django

Una vez creado el esquema GYM_APP, actualizar en Django:

```python
# octofit-tracker/backend/.env
ORACLE_DB_NAME=ORCLCDB
ORACLE_DB_USER=GYM_APP
ORACLE_DB_PASSWORD=gym_app_password
ORACLE_DB_HOST=localhost
ORACLE_DB_PORT=1521
```

```python
# octofit-tracker/backend/octofit_tracker/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'localhost:1521/ORCLCDB',
        'USER': 'GYM_APP',
        'PASSWORD': 'gym_app_password',
        'ATOMIC_REQUESTS': True,
    }
}
```
