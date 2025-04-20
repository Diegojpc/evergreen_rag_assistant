# Asistente para la Producción Agrícola en Evergreen

<div align="center">
  <img src="./assets/image.jpg" alt="evergreen" style="max-width: 600;">
  <p><em>Figura 1: Evergreen. Elaboración Propia usando <a href="https://gemini.google.com/">Gemini.</a></em></p>
</div>

##  Misión:

Este asistente tiene como objetivo ayudar a los agricultores de Evergreen a tomar decisiones informadas sobre la producción de cultivos a partir de recomendaciones generadas basadas en el historial de producción de las parcelas, las condiciones climáticas, las características del suelo, la fase lunar y los parámetros de producción, información que es consolidada por el aplicativo y procesada por un LLM para generar recomendaciones precisas.

##  Alcance:

Este es un proyecto académico, por lo cual se simula las conexiones con servicios externos mediante datos de ejemplo. Estas conexiones simuladas son:

- Obtener información del clima de la región donde está ubicada la parcela.
- Obtener información satelital de la parcela para determinar anomalías en el suelo y en la vegetación.
- Obtener información histórica de la producción de la parcela e información técnica de los cultivos.
- Obtener información de proyectos y parcelas de Evergreen.
- Obtener información de los parámetros de producción del cultivo en curso.
- Obtener información de la fase lunar.

La conexión con los LLM no es simulada y se realiza mediante las APIs de consumo de cada uno de ellos.

##  Servicios:

### 1. Servidor:

#### 1.1. Verificar el estado del servidor:

Usado para verificar si el servidor está funcionando correctamente y está habilitado para recibir peticiones.

- **Endpoint:** `/evergreen/pro/server/status`
- **Método:** `GET`
- **Parámetros tipo query:** `Ninguno`
- **Parámetros tipo path:** `Ninguno`
- **Cuerpo de la petición:** `No aplica`
- **Cuerpo de la Respuesta:** JSON con el estado del servidor.

```json
    {
        "status": "string",
        "message": "string",
        "timestamp": "2025-04-19T13:10:05.082Z"
    }
```

### 2. Proyectos de agricultura:

#### 2.1. Obtener información de los proyectos de agricultura:

Usado para obtener información de todos los proyectos de agricultura.

- **Endpoint:** `/evergreen/pro/projects/`
- **Método:** `GET`
- **Parámetros tipo query:** `Ninguno`
- **Parámetros tipo path:** `Ninguno`
- **Cuerpo de la petición:** `No aplica`
- **Cuerpo de la Respuesta:** JSON con la información de los proyectos de agricultura.

```json
    [
        {
            "project_id": "string",
            "parcel_id": "string",
            "location": "string",
            "crop_type": "string",
            "variety": "string",
            "planting_date": "string",
            "current_phase": "string"
        }
    ]
```

####    2.2. Obtener información de un proyecto específico:

Usado para obtener información de un proyecto específico mediante su identificador único.

- **Endpoint:** `/evergreen/pro/projects/{project_id}`
- **Método:** `GET`
- **Parámetros tipo query:** `Ninguno`
- **Parámetros tipo path:**
    - `project_id`: Identificador único del proyecto.
- **Cuerpo de la petición:** `No aplica`
- **Cuerpo de la Respuesta:** JSON con la información del proyecto.

```json
    {
        "project_id": "string",
        "parcel_id": "string",
        "location": "string",
        "crop_type": "string",
        "variety": "string",
        "planting_date": "string",
        "current_phase": "string"
    }
```

####    2.3. Obtener información de un proyecto específico mediante el identificador de la parcela asociada:

Usado para obtener información de un proyecto específico mediante el identificador de la parcela asociada.

- **Endpoint:** `/evergreen/pro/projects/parcel/{parcel_id}`
- **Método:** `GET`
- **Parámetros tipo query:** `Ninguno`
- **Parámetros tipo path:**
    - `parcel_id`: Identificador único de la parcela.
- **Cuerpo de la petición:** `No aplica`
- **Cuerpo de la Respuesta:** JSON con la información de la parcela.

```json 
    {
        "parcel_id": "string",
        "location": "string",
        "crop_type": "string",
        "variety": "string"
    }
```

### 3. Recomendaciones de producción:

#### 3.1. Obtener recomendaciones de producción para un proyecto específico:

Usado para obtener recomendaciones de producción para un proyecto específico a partir de una pregunta particular realizada por el usuario.

- **Endpoint:** `/evergreen/pro/recommendations/`
- **Método:** `POST`
- **Parámetros tipo query:** `Ninguno`
- **Parámetros tipo path:** `Ninguno`
- **Cuerpo de la petición:** JSON con la pregunta del usuario.

```json
    {
        "model": "google/flan-t5-large",
        "parcel_id": "string",
        "user_question": "What actions should I take on my crop over the next 5-7 days?"
    }
```

- **Cuerpo de la Respuesta:** JSON con la información de la parcela.

```json
    {
        "model": "google/flan-t5-large",
        "project_id": "string",
        "parcel_id": "string",
        "user_question": "string",
        "details": "string"
    }
```
##  Arquitectura:

Esta API está construida en [Python](https://www.python.org/) a partir del framework [FastAPI](https://fastapi.tiangolo.com/) y tiene la siguiente distribución de directorios:

```
app/
├── api/ # Capa de API - maneja las peticiones HTTP y las rutas
│ ├── routes/ # Capa de definición de las rutas de la API
│   ├── health.py # Rutas para la salud del servidor
│   ├── projects.py # Rutas para la información de los proyectos
│   └── recommendations.py # Rutas para la recomendación de producción
│ └── router.py # Configuración principal de las rutas de la API
│
├── config/ # Capa de configuración de la aplicación
│ └── config.py # Configuración de la aplicación
│
├── domain/ # Lógica de negocio y modelos de dominio
│ ├── projects.py # Lógica de negocio para la información de los proyectos
│ └── recommendations.py # Lógica de negocio para la recomendación de producción
│
├── models/ # Capa de modelos de datos y esquemas
│ ├── best_practices.py # Modelo de datos para las mejores prácticas de producción
│ ├── llms.py # Modelo de datos para la conexión con los diferentes LLM
│ ├── lunar.py # Modelo de datos para la información de la fase lunar
│ ├── process.py # Modelo de datos para la información de los procesos
│ ├── project.py # Modelo de datos para la información de los proyectos
│ ├── recommendation.py # Modelo de datos para la recomendación de producción
│ ├── satellite.py # Modelo de datos para la información satelital
│ ├── server.py # Modelo de datos para los endpoints de salud del servidor
│ └── weather.py # Modelo de datos para la información del clima
│
├── services/ # Capa de integración con servicios externos
│ ├── llms.py # Conexión con los diferentes LLM
│ ├── lunar_info.py # Simula la conexión con el servicio de información de la fase lunar
│ ├── process_info.py # Simula la conexión con el servicio de información de los procesos
│ ├── projects_info.py # Simula la conexión con el servicio de información de los proyectos
│ ├── retrieval_info.py # Simula la conexión con el servicio de recuperación de información histórica
│ ├── satellite_info.py # Simula la conexión con el servicio de información satelital
│ └── weather_info.py # Simula la conexión con el servicio de información del clima
│
└── main.py # Punto de entrada de la aplicación
```

Este servicio simula el *Servicio RAG* que orquesta las peticiones a los diferentes servicios externos y la respuesta del LLM. El diagrama de la arquitectura se muestra en la figura 2.

<div align="center">
  <img src="./assets/arq.png" alt="Arquitectura" style="max-width: 600;">
  <p><em>Figura 2: Arquitectura del proyecto. Elaboración Propia.</em></p>
</div>

##  Instalación:

### 1. Crear entorno virtual:

```bash
    python3 -m venv .venv
```

### 2. Activar entorno virtual:

```bash
    source .venv/bin/activate
```

### 3. Actualizar version de pip:

```bash
    python3 -m pip install --upgrade pip
```

### 4. Instalar dependencias:

```bash
    python3 -mpip install -r requirements.txt
```

## Ejecución:

### 1. Definir variables de entorno:

Crear un archivo `.env` en la raíz del proyecto con las variables de entorno necesarias:

```
    SERVER_HOST="0.0.0.0"
    SERVER_PORT="8000"

    HF_TOKEN="hf_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    OPENAI_API_KEY="sk-proj-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

### 2. Ejecutar servidor:

```bash
    bash run.sh
```

### 3. Acceder a la documentación:

La documentación se obtiene accediendo a la ruta */docs* de la api siguiendo la URL:

```
    http://localhost:8000/docs
```

Para probar el servicio de generación de recomendaciones con diferentes modelos LLM, puede buscar en la sección de *Schemas* el modelo **ImplementedModels** y seleccionar el modelo que desea utilizar.
