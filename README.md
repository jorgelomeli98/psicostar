# API para puntuar y catalogar psicologos

API REST para catalogar psicólogos por enfoques, ubicaciones y experiencia, permitiendo puntuarlos y filtrarlos según criterios específicos.

## Descripción

Esta API permite gestionar un catálogo de psicólogos, organizado por sus enfoques terapéuticos, años de experiencia y ubicación. Los usuarios pueden realizar búsquedas filtradas según estos criterios, además de tener la opción de puntuar y dejar comentarios sobre los psicólogos, facilitando la elección y evaluación de los profesionales más adecuados a sus necesidades.

## Tecnologías

- **FastAPI** - Framework para construir APIs en Python.
- **MySQL** - Base de datos relacional para almacenar la información.
- **JWT** - Autenticación segura mediante tokens.
- **SQLAlchemy** - ORM para manejar la base de datos.
- **Pytest** - Pruebas automatizadas para la API.
- **Alembic** - Migracion de bases de datos

## Instalación y Configuración

### Clonar el repositorio

```bash
git clone https://github.com/tuusuario/tu-api.git
cd tu-api
```

### Crear y activar un entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En macOS/Linux
venv\Scripts\activate  # En Windows
```

### Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Configurar variables de entorno

Crea un archivo .env con la siguiente configuracion:

```bash
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

DATABASE_URL="mysql+pymysql://usuario:contraseña@localhost:3306/nombre_base_datos"
```

### Ejecutar migraciones

```bash
alembic upgrade head
```

## Endpoints

### Usuarios

#### Obtener todos los usuarios

**Descripción:** Recupera una lista de todos los usuarios registrados.  
**Método:** `GET`  
**Ruta:** `/users/`  
**Respuesta exitosa:**

- Código de estado: `200 OK`
- Modelo de respuesta: Lista de objetos `UserResponse`.

---

#### Obtener usuario por ID

**Descripción:** Recupera un usuario específico por su ID.  
**Método:** `GET`  
**Ruta:** `/users/{id}`  
**Respuesta exitosa:**

- Código de estado: `200 OK`
- Modelo de respuesta: `UserResponse`.

---

#### Iniciar sesión

**Descripción:** Inicia sesión con un usuario registrado y genera un token de autenticación.  
**Método:** `POST`  
**Ruta:** `/users/login`  
**Body:**

```json
{
  "username": "email@example.com",
  "password": "tucontraseña"
}
```

**Respuesta exitosa:**

- Código de estado: `202 ACCEPTED`
- Modelo de respuesta: Un objeto que contiene el `access_token`.

---

#### Registrar usuario

**Descripción:** Registra un nuevo usuario en el sistema.  
**Método:** `POST`  
**Ruta:** `/users/`  
**Body:**

```json
{
  "email": "email@example.com",
  "password": "tucontraseña",
  "nombre": "Nombre Usuario"
}
```

**Respuesta exitosa:**

- Código de estado: `201 CREATED`
- Modelo de respuesta: `UserResponse`.

---

#### Actualizar usuario

**Descripción:** Actualiza los datos de un usuario registrado.  
**Método:** `PATCH`  
**Ruta:** `/users/`  
**Body:** (solo enviar los campos a actualizar)

```json
{
  "nombre": "Nuevo Nombre"
}
```

**Respuesta exitosa:**

- Código de estado: `200 OK`
- Modelo de respuesta: `UserResponse`.

---

#### Eliminar usuario

**Descripción:** Elimina un usuario registrado.  
**Método:** `DELETE`  
**Ruta:** `/users/`  
**Respuesta exitosa:**

- Código de estado: `200 OK`
- Modelo de respuesta: `{ "message": "Usuario eliminado" }`.

---

### Psicólogos

#### Registrar psicólogo

**Descripción:** Registra un nuevo psicólogo en el sistema.  
**Método:** `POST`  
**Ruta:** `/users/psychologist`  
**Body:**

```json
{
  "cedula": "12345678",
  "experiencia": "5 años",
  "ubicacion": "Ciudad Ejemplo",
  "approach_id": 1
}
```

**Respuesta exitosa:**

- Código de estado: `201 CREATED`
- Modelo de respuesta: `PsychologistResponse`.

---

#### Actualizar psicólogo

**Descripción:** Actualiza los datos de un psicólogo registrado.  
**Método:** `PATCH`  
**Ruta:** `/users/psychologist`  
**Body:**

```json
{
  "experiencia": "6 años"
}
```

**Respuesta exitosa:**

- Código de estado: `200 OK`
- Modelo de respuesta: `PsychologistResponse`.

---

### Enfoques

#### Obtener un enfoque por ID

**Descripción:** Recupera un enfoque específico por su ID.  
**Método:** `GET`  
**Ruta:** `/approachs/{approach_id}`  
**Respuesta exitosa:**

- Código de estado: `200 OK`
- Modelo de respuesta: `ApproachResponse`.

---

#### Obtener todos los enfoques

**Descripción:** Recupera una lista de todos los enfoques registrados.  
**Método:** `GET`  
**Ruta:** `/approachs`  
**Respuesta exitosa:**

- Código de estado: `200 OK`
- Modelo de respuesta: Lista de objetos `ApproachResponse`.

---

#### Crear un nuevo enfoque

**Descripción:** Crea un nuevo enfoque terapéutico.  
**Método:** `POST`  
**Ruta:** `/approachs`  
**Body:**

```json
{
  "name": "Cognitivo Conductual"
}
```

**Respuesta exitosa:**

- Código de estado: `201 CREATED`
- Modelo de respuesta: `ApproachResponse`.

---

#### Actualizar un enfoque

**Descripción:** Actualiza un enfoque existente.  
**Método:** `PUT`  
**Ruta:** `/approachs/{approach_id}`  
**Body:**

```json
{
  "name": "Nuevo nombre del enfoque"
}
```

**Respuesta exitosa:**

- Código de estado: `200 OK`
- Modelo de respuesta: `ApproachResponse`.

---

#### Eliminar un enfoque

**Descripción:** Elimina un enfoque por su ID.  
**Método:** `DELETE`  
**Ruta:** `/approachs/{approach_id}`  
**Respuesta exitosa:**

- Código de estado: `204 NO CONTENT`

---

#### Asignar un enfoque a un psicólogo

**Descripción:** Asigna un enfoque terapéutico a un psicólogo.  
**Método:** `POST`  
**Ruta:** `/approachs/psychologist/{approach_id}`  
**Respuesta exitosa:**

- Código de estado: `201 CREATED`
- Modelo de respuesta: `ConexionApproachResponse`.

---

## Autenticación

Todos los endpoints protegidos requieren un token de autenticación Bearer en el header `Authorization`.

Ejemplo:

```http
Authorization: Bearer <token>
```

## Psicologos

### Obtener todos los psicólogos

**Descripción:** Recupera una lista de todos los psicólogos registrados.  
**Método:** `GET`  
**Ruta:** `/psychologists/`  
**Respuesta exitosa:**

- Código de estado: `200 OK`
- Modelo de respuesta: Lista de objetos `PsychologistResponse`.

### Obtener psicólogo por ID

**Descripción:** Recupera los datos de un psicólogo específico mediante su ID.  
**Método:** `GET`  
**Ruta:** `/psychologists/{id}`  
**Parámetros:**

- `id` (string): El ID del psicólogo.

**Respuesta exitosa:**

- Código de estado: `200 OK`
- Modelo de respuesta: Objeto `PsychologistResponse`.

**Errores:**

- Código de estado: `404 NOT FOUND`
- Detalle: "Psychologist not found".

### Obtener psicólogos por enfoque (approach ID)

**Descripción:** Recupera una lista de psicólogos asociados a un enfoque específico.  
**Método:** `GET`  
**Ruta:** `/psychologists/by-approach/{approach_id}`  
**Parámetros:**

- `approach_id` (integer): El ID del enfoque.

**Respuesta exitosa:**

- Código de estado: `200 OK`
- Modelo de respuesta: Lista de objetos `PsychologistResponse`.

**Errores:**

- Código de estado: `404 NOT FOUND`
- Detalle: "Psychologists not found".

## Modelos de Respuesta

### PsychologistResponse

Un modelo que representa los datos de un psicólogo. (Aquí se pueden detallar los atributos específicos del modelo si es necesario).

## Manejo de Errores

Los errores están representados en formato JSON con un mensaje detallado. Ejemplo:

```json
{
  "detail": "Psychologist not found"
}
```
