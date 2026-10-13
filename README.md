# Vivero Hojas Verdes - API RESTful con Django REST Framework y JWT

Sistema web backend para la gestión de catálogo e inventario de plantas ornamentales desarrollado para **Vivero Hojas Verdes**. Implementa una arquitectura API RESTful construida con Django, Django REST Framework (DRF), persistencia en MariaDB/MySQL, autenticación basada en tokens JWT y soporte para carga de archivos multimedia.

---

## Información del Proyecto

* **Institución:** INACAP Sede Maipú
* **Carrera:** Ingeniería en Informática
* **Asignatura:** Backend con Framework Django
* **Evaluación:** Tercera Evaluación - API RESTful (Ponderación: 35%)
* **Estudiante:** Eleazar Rojas
* **Docente:** Jorge Saavedra Rubilar

---

## 1. Descripción de la Empresa y Problemática

**Vivero Hojas Verdes** es un negocio dedicado a la comercialización de plantas de interior y exterior. Para modernizar sus canales de distribución y permitir la integración con aplicaciones clientes (móviles y web), se requirió desacoplar la capa de presentación de la capa de datos.

La solución implementada provee una **API RESTful** que:
1. Permite la consulta pública de productos en inventario (`GET`).
2. Centraliza y protege las operaciones de escritura, edición y baja de productos mediante tokens criptográficos JWT (`POST`, `PUT`, `DELETE`).
3. Administra el almacenamiento persistente de imágenes asociadas a cada espécimen en el catálogo.
4. Aplica reglas de validación de negocio estrictas antes de persistir los datos en el motor relacional.

---

## 2. Tecnologías Utilizadas

* **Lenguaje:** Python 3.10+
* **Framework:** Django 5.x
* **Toolkit REST:** Django REST Framework (DRF)
* **Autenticación:** JSON Web Tokens (`djangorestframework-simplejwt`)
* **Base de Datos:** MariaDB / MySQL (mediante conector `PyMySQL`)
* **Procesamiento de Imágenes:** Pillow
* **Pruebas y Documentación HTTP:** Thunder Client / Postman

---

## 3. Instrucciones de Instalación y Ejecución

### Prerrequisitos
* Tener instalado Python 3.10 o superior.
* Servidor MariaDB / MySQL activo con la base de datos `vivero` previamente creada.

### Paso 1: Clonar el repositorio
```bash
git clone [https://github.com/TU_USUARIO/TU_REPOSITORIO.git](https://github.com/TU_USUARIO/TU_REPOSITORIO.git)
cd TU_REPOSITORIO
```

### Paso 2: Instalar dependencias
```bash
pip install django pymysql pillow djangorestframework djangorestframework-simplejwt
```

### Paso 3: Configurar y aplicar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### Paso 4: Crear Superusuario (para autenticación)
```bash
python manage.py createsuperuser
```
*(Ingresar usuario, correo y contraseña administrativa).*

### Paso 5: Iniciar el servidor de desarrollo
```bash
python manage.py runserver
```
La API quedará operativa y escuchando en: `http://127.0.0.1:8000/`

---

## 4. Documentación de Endpoints

### 4.1. Módulo de Autenticación (JWT)

| Método | Endpoint | Cabeceras | Parámetros (Body JSON) | Códigos HTTP | Descripción |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **POST** | `/api/token/` | `Content-Type: application/json` | `{"username": "...", "password": "..."}` | `200`, `401` | Genera el par de tokens: `access` y `refresh`. |
| **POST** | `/api/token/refresh/` | `Content-Type: application/json` | `{"refresh": "<refresh_token>"}` | `200`, `401` | Genera un nuevo `access` token a partir de un refresh válido. |

### 4.2. Módulo de Catálogo de Plantas

| Método | Endpoint | Autenticación | Formato Entrada | Códigos HTTP | Descripción |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **GET** | `/api/plantas/` | Pública | Query Params | `200 OK` | Retorna listado completo en JSON. Admite filtro: `?buscar=<texto>`. |
| **POST** | `/api/plantas/` | `Bearer <token>` | `multipart/form-data` | `201`, `400`, `401` | Registra una nueva planta con imagen binaria adjunta. |
| **GET** | `/api/plantas/<id>/` | Pública | Ninguno | `200`, `404` | Obtiene el detalle de una planta específica por ID. |
| **PUT** | `/api/plantas/<id>/` | `Bearer <token>` | JSON o Form-data | `200`, `400`, `401`, `404` | Modifica los datos de una planta existente. |
| **DELETE**| `/api/plantas/<id>/` | `Bearer <token>` | Ninguno | `204`, `401`, `404` | Elimina el registro en MariaDB y remueve el archivo físico de imagen. |

---

## 5. Reglas de Validación de Negocio

La API cuenta con validadores personalizados implementados en `PlantaSerializer`:
* **Nombre:** Debe poseer un largo mínimo de 3 caracteres.
* **Precio:** Debe ser estrictamente superior a $0 y menor a $1.000.000.
* **Stock:** Valor entero mayor o igual a 0 y no superior a 9.999 unidades.
* **Imagen:** Campo obligatorio al momento del registro inicial.

---

## 6. Evidencias y Códigos de Respuesta HTTP

Durante la verificación con el cliente HTTP (Thunder Client / Postman) se demostraron los siguientes estados:

* **`200 OK`**: Autenticación exitosa, lectura de listados y consulta de detalle.
* **`201 Created`**: Inserción exitosa de recurso con carga de imagen.
* **`204 No Content`**: Eliminación física del registro sin contenido retornado.
* **`400 Bad Request`**: Infracción en reglas de validación (precios negativos, nombres cortos).
* **`401 Unauthorized`**: Petición de escritura rechazada por ausencia de cabecera `Authorization: Bearer <token>`.
* **`404 Not Found`**: Búsqueda de identificador primario inexistente en la base de datos.# Tercera-evaluacion-Back-end