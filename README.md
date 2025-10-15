# Tarea 3 — Procesamiento de Datos con Apache Spark

## 👩‍💻 Estudiante
**Andrea Rodriguez Ospina - UNAD**

---

## 🧩 1. Definición del problema y conjunto de datos

### 📖 Problema a resolver
Netflix cuenta con un extenso catálogo de películas y series que varía constantemente según el país, la fecha de lanzamiento y la categoría.  
El objetivo de este proyecto es **analizar el catálogo de shows** para identificar:
- Qué tipo de contenido predomina (películas o series),
- Qué países tienen más producciones,
- Cuáles son los géneros más populares.

Este análisis permite extraer información relevante sobre las tendencias del contenido disponible en la plataforma, aplicando técnicas de procesamiento de datos.


### 📂 Conjunto de datos seleccionado
Se utilizó el dataset público **Netflix Movies and TV Shows**, disponible en [Kaggle](https://www.kaggle.com/datasets/shivamb/netflix-shows).

**Características del dataset:**
- Fuente: Kaggle (dataset público)
- Atributos: `show_id`, `type`, `title`, `director`, `cast`, `country`, `release_year`, `rating`, `duration`, `listed_in`, `description`
- Ruta local utilizada: /home/andrea-rodriguez/Downloads/netflix_titles.csv

## ⚙️ Overview de la actividad 

Durante el desarrollo de esta tarea se configuró un entorno completo para trabajar con **procesamiento de datos masivos** utilizando **Apache Hadoop** y **Apache Spark** en una máquina virtual con Ubuntu.

Primero, se validó el funcionamiento de **Hadoop** mediante los comandos `start-dfs.sh`, `start-yarn.sh` y `jps`.  
Esto permitió iniciar el sistema de archivos distribuido y acceder a las interfaces web de administración (NameNode y ResourceManager).

Posteriormente, se procedió a la **instalación de Spark 4.0.1** (compatible con Hadoop 3), por medio de la la función de carpetas compartidas de VirtualBox, configurando las variables de entorno en el archivo `~/.bashrc` y verificando la correcta inicialización de Spark con el comando `pyspark`.  
Desde este entorno se desarrollaron dos tipos de procesamiento:

### ⚙️ Procesamiento Batch

Se cargó el dataset público **Netflix Movies and TV Shows**, aplicando limpieza, transformaciones y un análisis exploratorio básico de datos (EDA) utilizando **Spark DataFrames**.

**Resultados principales:**
- Total de registros: **8,807**
- Películas (Movies): **6,131**
- Series (TV Shows): **2,676**
- Países con más producciones: **Estados Unidos, India y Reino Unido**
- Géneros más comunes: **International Movies, Dramas, Comedies, Documentaries**

Los resultados procesados fueron exportados en formato **CSV** a la ruta local `/home/andrea-rodriguez/Downloads/resultados_netflix`.

### 🔄 Procesamiento en Tiempo Real (Streaming)

Se implementó un flujo de **Spark Structured Streaming** para simular la llegada de datos en tiempo real, utilizando una carpeta local como fuente (`/home/andrea-rodriguez/stream_input`).

- Se procesaban los datos conforme eran añadidos a la carpeta.  
- Se contaban los registros por tipo de contenido (películas o series).  
- Los resultados se mostraban en consola en tiempo real.  
- No se utilizó **Kafka** debido a limitaciones de memoria de mi computador; pero el streaming local cumplió la misma función de demostración.

---
### 🔹 Problemas y Soluciones

| **Problema** | **Causa** | **Solución** |
|---------------|------------|---------------|
| Error 404 al descargar Spark | URL oficial no disponible | Descarga alternativa desde `archive.apache.org` y usar la opción de carpetas compartidas de virtualbox |
| Permiso denegado en `/usr/local/spark` | Carpeta de root | `sudo chown -R $USER:$USER /usr/local/spark` |
| Incompatibilidad con Java 11 | Spark 4.0 requiere Java 17 | Instalación de OpenJDK 17 |
| Fallo Spark + Kafka - Colapso de Virtualbox| Limitación de memoria RAM | Se reemplazó por una simulación local con carpeta de streaming |
| Interfaz Spark UI no abre | Spark detenido | Reiniciar PySpark y acceder nuevamente a http://localhost:4040 |

---
### 🌐 Verificación y Monitoreo

- Se comprobó el correcto funcionamiento de Spark mediante su interfaz web:  
  **http://bd-ubuntu:4040**
- Se validó la escritura de los resultados en el sistema local.
- Se detuvieron los servicios correctamente para conservar la configuración del entorno.
- El código que se ejecutó en consola esta en el repositorio como: `spark-andrea-rodriguez.py`
---

### 🎯 Conclusión

Este proyecto me permitió comprender como funcionan los ciclos de procesamiento de datos con **Apache Spark**, desde su instalación y configuración hasta la ejecución de tareas **batch** y **streaming** en un entorno distribuido. 

