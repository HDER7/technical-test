# Technical Test - Backend API

API REST desarrollada con FastAPI para gestión de tareas con autenticación JWT.

## Tecnologías

- **Python 3.11.9**
- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para base de datos
- **PostgreSQL** - Base de datos relacional
- **Alembic** - Migraciones de base de datos
- **JWT** - Autenticación basada en tokens
- **Bcrypt** - Hash seguro de contraseñas
- **Pydantic** - Validación de datos

## Arquitectura

El proyecto sigue una arquitectura modular y escalable:

```
technical-test/
├── app/
│   ├── api/           # Endpoints y routers
│   ├── core/          # Configuración, seguridad y JWT
│   ├── db/            # Sesión y conexión a BD
│   ├── models/        # Modelos SQLAlchemy
│   ├── schemas/       # Esquemas Pydantic
│   └── services/      # Lógica de negocio
├── alembic/           # Migraciones de base de datos
├── main.py            # Punto de entrada de la aplicación
├── init_db.py         # Script para inicializar datos
└── docker-compose.yml # PostgreSQL en Docker
```

## Requisitos Previos

- Python 3.11.8 o superior
- Docker y Docker Compose
- Git

## Configuración e Instalación

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd technical-test
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
```

### 3. Activar entorno virtual

Windows:
```bash
.venv\Scripts\activate
```

Linux/Mac:
```bash
source .venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar variables de entorno

El archivo `.env` ya está configurado con valores por defecto. Verificar que contenga:

```env
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=technical_test
DB_USER=postgres
DB_PASSWORD=postgres

# JWT
SECRET_KEY=clave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
API_V1_STR=/api/v1
PROJECT_NAME=Technical Test

# Initial User
INITIAL_USER_EMAIL=admin@correo.com
INITIAL_USER_PASSWORD=Admin123!
```

**Importante**: En producción, cambiar `SECRET_KEY` por una clave segura generada aleatoriamente.

### 6. Levantar PostgreSQL con Docker

```bash
docker-compose up -d
```

Verificar que el contenedor esté corriendo:
```bash
docker ps
```

### 7. Ejecutar migraciones

```bash
alembic upgrade head
```

### 8. Inicializar usuario y datos de prueba

```bash
python init_db.py
```

Esto creará:
- Usuario inicial con credenciales del .env
- 5 tareas de ejemplo

### 9. Ejecutar la aplicación

```bash
uvicorn main:app --reload
```

La aplicación estará disponible en: http://localhost:8000

Documentación interactiva: http://localhost:8000/api/v1/docs

## Credenciales de Usuario Inicial

```
Email: admin@correo.com
Password: Admin123!
```

## Endpoints Disponibles

### Autenticación

#### POST /api/v1/auth/login
Autenticar usuario y obtener token JWT.

**Request:**
```json
{
  "email": "admin@correo.com",
  "password": "Admin123!"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Tareas (requieren autenticación)

Todas las peticiones a endpoints de tareas deben incluir el header:
```
Authorization: Bearer <access_token>
```

#### POST /api/v1/tasks
Crear una nueva tarea.

**Request:**
```json
{
  "title": "Nueva tarea",
  "description": "Descripción opcional",
  "status": "pending"
}
```

**Response:** Objeto Task con id generado.

#### GET /api/v1/tasks
Listar tareas con paginación.

**Query Parameters:**
- `page` (opcional): Número de página (default: 1)
- `page_size` (opcional): Tamaño de página (default: 10, max: 100)
- `status` (opcional): Filtrar por estado (pending, in_progress, done)

**Response:**
```json
{
  "total": 5,
  "page": 1,
  "page_size": 10,
  "items": [...]
}
```

#### GET /api/v1/tasks/{task_id}
Obtener una tarea específica.

**Response:** Objeto Task.

#### PUT /api/v1/tasks/{task_id}
Actualizar una tarea.

**Request:**
```json
{
  "title": "Título actualizado",
  "description": "Nueva descripción",
  "status": "in_progress"
}
```

Todos los campos son opcionales.

**Response:** Objeto Task actualizado.

#### DELETE /api/v1/tasks/{task_id}
Eliminar una tarea.

**Response:** 204 No Content

## Ejemplos de Uso

### Con cURL

**Login:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@correo.com","password":"Admin123!"}'
```

**Crear tarea:**
```bash
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"title":"Mi tarea","description":"Descripción","status":"pending"}'
```

**Listar tareas:**
```bash
curl -X GET "http://localhost:8000/api/v1/tasks?page=1&page_size=10" \
  -H "Authorization: Bearer <token>"
```

**Actualizar tarea:**
```bash
curl -X PUT "http://localhost:8000/api/v1/tasks/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"status":"done"}'
```

**Eliminar tarea:**
```bash
curl -X DELETE "http://localhost:8000/api/v1/tasks/1" \
  -H "Authorization: Bearer <token>"
```

## Modelo de Datos

### User
- `id`: Integer (PK)
- `email`: String (unique, indexed)
- `hashed_password`: String
- `is_active`: Boolean
- `created_at`: DateTime

### Task
- `id`: Integer (PK)
- `title`: String(255) (required, indexed)
- `description`: Text (optional)
- `status`: Enum (pending, in_progress, done) (indexed)
- `created_at`: DateTime (indexed)
- `updated_at`: DateTime
- `user_id`: Integer (FK, indexed)

## Índices de Base de Datos

Se crearon índices en los siguientes campos para optimizar el rendimiento:

### Tabla users
- `email`: Búsquedas de usuario por email (autenticación)
- `id`: Primary key lookup

### Tabla tasks
- `title`: Búsquedas de tareas por título
- `status`: Filtrado de tareas por estado
- `created_at`: Ordenamiento por fecha de creación
- `user_id`: Búsquedas de tareas por usuario

**Justificación:**
- `email` y `user_id`: Son campos usados frecuentemente en WHERE clauses
- `status`: Se usa para filtrado en listados
- `created_at`: Se usa para ordenamiento en paginación
- `title`: Permite búsquedas rápidas por título (para funcionalidad futura de búsqueda)

## Manejo de Errores

La API devuelve códigos HTTP estándar:

- `200 OK`: Operación exitosa
- `201 Created`: Recurso creado exitosamente
- `204 No Content`: Eliminación exitosa
- `400 Bad Request`: Datos inválidos o usuario inactivo
- `401 Unauthorized`: No autenticado o token inválido
- `404 Not Found`: Recurso no encontrado
- `422 Unprocessable Entity`: Error de validación de datos

## Decisiones Técnicas

### 1. Autenticación
- Se usa JWT con expiración configurable
- Las contraseñas se hashean con bcrypt (10 rounds por defecto)
- El usuario se identifica por email
- Bearer token en header Authorization

### 2. Paginación
- Implementación basada en page/page_size
- Límite máximo de 100 items por página
- Respuesta incluye total de items, página actual y page_size

### 3. Base de Datos
- PostgreSQL en Docker para facilitar setup local
- Migraciones con Alembic para control de versiones del schema
- Usuario inicial creado mediante script separado (no en migración)

### 4. Estructura
- Arquitectura de capas: API -> Services -> Models
- Separación clara de responsabilidades
- Inyección de dependencias con FastAPI

### 5. Validación
- Pydantic para validación automática de entrada/salida
- Mensajes de error descriptivos

## Tests

Para ejecutar en el futuro:
```bash
pytest
```

## Detener la Aplicación

Detener FastAPI: `Ctrl+C`

Detener PostgreSQL:
```bash
docker-compose down
```

Para eliminar también los datos:
```bash
docker-compose down -v
```

## Notas

- El archivo `.env` está incluido para facilitar la evaluación. En un proyecto real estaría en `.gitignore`
- El SECRET_KEY debe ser cambiado en producción
- La aplicación está configurada para CORS permisivo (allow_origins=["*"]). En producción debe restringirse
- El script init_db.py es idempotente: no recrea el usuario si ya existe

## Próximas Mejoras

- Tests unitarios e integración
- Logging estructurado
- Rate limiting
- Búsqueda full-text en tareas
- Soft delete para tareas
- Filtros adicionales (fecha, ordenamiento personalizado)
