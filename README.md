# Reto Persistencia Grupo3 - Desarrollo de aplicaciones IoT

## Proyecto: Inserción, Agregación y Visualización de Datos de una Turbina de Viento

Este proyecto tiene como objetivo la simulación de un sistema de adquisición, almacenamiento, análisis y visualización de datos reales de una turbina de viento. Para ello, se ha utilizado el [dataset de SCADA de turbina de viento de Kaggle](https://www.kaggle.com/datasets/berkerisen/wind-turbine-scada-dataset), que contiene medidas como potencia activa, velocidad del viento, dirección del viento y potencia teórica.

Se ha utilizado **InfluxDB** como base de datos de series temporales, junto con **Python** para la lectura e inserción de datos, **HTTPS** para la seguridad y un **dashboard en InfluxDB** para visualización avanzada. Todo el sistema se orquesta mediante **Docker Compose**.

---

## Justificación de la Elección de InfluxDB

La naturaleza del dataset utilizado es **una serie temporal**: mediciones periódicas de variables físicas de una turbina eólica. Por ello, InfluxDB es especialmente apropiada por las siguientes razones:

- Está optimizada para manejar datos de series temporales con marcas de tiempo precisas.
- Permite realizar **agregaciones complejas (media, mínimo, máximo, etc.)** sobre ventanas temporales.
- Integra visualización y consultas avanzadas desde su propia interfaz.
- Tiene una API potente y fácilmente integrable con Python.
- Evita sobrecarga innecesaria que podría suponer una base de datos relacional para este tipo de casos.

---

## Explicación de los Pasos Seguidos en el Proyecto

### 1. **Lectura e Inserción del Dataset**

- Se ha creado un script en Python que:
  - Lee el dataset `.csv`.
  - Recorre cada fila y genera puntos con la clase `Point` de InfluxDB.
  - Cambia el timestamp para que sea desde 2024 hasta 2025 (más reciente).
  - Renombra las columnas para que sean más descriptivas.
  - Inserta los puntos en InfluxDB.


### 2. **Agregaciones **

- Se han realizado agregaciones dentro del panel de InfluxDB con su sistema de consulta integrado (InfluxQL o Flux).
- Estas agregaciones se pueden realizar manualmente en influx o visualizarse automáticamente en el dashboard.

### 3. **Visualización con Dashboards**

- Se ha creado un **dashboard en InfluxDB** que incluye:
  - **5-day period Mean of all data points**
  - **Max Wind Speed of all data points**
  - **Wind Speed mean of all data points**
  - **Max Theoretical Power**
  - **Theoretical Power mean of all data points**
  - **Max Real Power**
  - **Real Power mean of all data points**
  - **Wind Direction mean of all data points**

- El dashboard se puede importar desde el archivo `wind_turbine_data.json` incluido en el repositorio.

### 4. **Seguridad HTTPS**

- El acceso a InfluxDB está configurado para requerir **HTTPS**.
- Se ha generado un certificado autofirmado para proteger las comunicaciones en el entorno de desarrollo.

### 5. **Despliegue con Docker Compose**

El sistema está preparado para ejecutarse con un único comando:

```bash
docker compose up --build
```

Esto levanta:

- Un contenedor con InfluxDB 2 con configuración inicial automatizada (usuario, bucket, organización y token).
- Un contenedor con el script de inserción de datos.

No es necesario registrarse manualmente en InfluxDB (solo iniciar sesión), todo está automatizado gracias a el .env y al setup que ofrece influxdb.

---

## Instrucciones de Uso

### 1. **Requisitos Previos**

- Tener instalado [Docker](https://www.docker.com/get-started) y [Docker Compose](https://docs.docker.com/compose/install/).

### 2. **Ejecución**

```bash
git clone <repositorio>
cd <repositorio>
docker compose up --build
```

- El script de inserción ejecutará automáticamente la carga de datos.
- Puedes ver el progreso de los servicios en los logs.

### 3. **Acceso a InfluxDB**

- Ir a [https://localhost:8086](https://localhost:8086) *(puede requerir aceptar certificado autofirmado)*.
- Poner el periodo de tiempo para consultas: **2024-01-01 00:00** a **2025-01-01 00:00**, ya que es donde se encuentran todos los datos.
- Visualizar datos y realizar consultas varias.
- Importar el dashboard desde `wind_turbine_data.json`:
  - En InfluxDB → Dashboards → Import JSON → Pegar contenido del archivo o subirlo directamente.
  - Poner el periodo de tiempo para consultas: **2024-01-01 00:00** a **2025-01-01 00:00**
  - Visualizar dashboard.

---

## Alternativas Posibles

### 1. Otras Bases de Datos

- **PostgreSQL:** buena opción relacional, pero menos eficiente para series temporales.
- **TimescaleDB:** extensión de PostgreSQL que añade funcionalidad de series temporales, pero requiere configuración adicional.
- **MongoDB Time Series:** opción válida pero menos optimizada que InfluxDB para datos de IoT.

### 2. Otros Métodos de Comunicación

- **MQTT o Kafka:** aplicables si hubiera generación continua en tiempo real. No necesario en este caso de carga histórica.

### 3. Orquestación con Kubernetes

- En contextos de mayor escala, Kubernetes permitiría escalado y recuperación automática, aunque innecesario en esta prueba de concepto.

---

## Posibles Vías de Mejora

- Automatizar aún más la generación de dashboards.
- Añadir autenticación OAuth2 para mayor seguridad.
- Configurar alertas automáticas si ciertas métricas superan umbrales.
- Incorporar una API externa que genere nuevos datos en tiempo real.

---

## Problemas / Retos Encontrados

- **Precisión temporal:** adaptar correctamente las marcas de tiempo a nanosegundos para InfluxDB.
- **Carga masiva de datos:** evitar cuellos de botella en la inserción masiva.
- **Certificados HTTPS:** generación, configuración y aceptación por parte del navegador.
- **Diseño del dashboard:** elección de visualizaciones útiles y claras.

---

## Extras y Mejoras Implementadas

- ✅ Visualización avanzada con dashboard en InfluxDB.
- ✅ Demostrar mediante una visualización la inserción de datos correcta, mediante linea temporal de influxdb. 
- ✅ HTTPS habilitado en el entorno.
- ✅ Argumentar la elección de la base de datos. 
- ✅ Despliegue completamente automatizado sin pasos manuales.
- ✅ Inicialización de influxdb sin necesidad de registrarse manualmente.

