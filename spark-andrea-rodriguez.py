"""
Tarea 3 - Procesamiento de Datos con Apache Spark
Autora: Andrea Rodriguez
Universidad Nacional Abierta y a Distancia (UNAD)
"""

# ============================================================
# CONFIGURACIÓN DEL ENTORNO HADOOP Y SPARK - VIRTUALBOX
# ============================================================

# --- 1. Verificar procesos de Hadoop (desde terminal) ---
# start-dfs.sh
# start-yarn.sh
# jps
# (Salida esperada: NameNode, DataNode, ResourceManager, NodeManager)

# --- 2. Verificar variables del entorno ---
# echo $JAVA_HOME
# echo $SPARK_HOME

# ============================================================
# INICIO DE SPARK DESDE PYTHON (PySpark)
# ============================================================

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, explode, trim

# Crear una sesión Spark (modo local)
spark = SparkSession.builder.appName("Tarea3_Spark_Netflix").getOrCreate()

# ============================================================
# PROCESAMIENTO BATCH - NETFLIX DATASET
# ============================================================

# Ruta del dataset
csv_path = "/home/andrea-rodriguez/Downloads/netflix_titles.csv"

# 1. Cargar el dataset desde CSV
df = spark.read.csv(csv_path, header=True, inferSchema=True)

print("=== Primeras 5 filas ===")
df.show(5)
print("=== Esquema del DataFrame ===")
df.printSchema()

# 2. Limpieza básica de datos
df = df.dropDuplicates()
df = df.filter(col("title").isNotNull())

# 3. Análisis exploratorio de datos (EDA)
print("=== Total de registros ===")
print(df.count())

print("=== Conteo por tipo (Movie / TV Show) ===")
df.groupBy("type").count().show()

print("=== Top 5 países con más títulos ===")
df.groupBy("country").count().orderBy("count", ascending=False).show(5, truncate=False)

print("=== Top 5 géneros más frecuentes ===")
genres = df.select(explode(split(col("listed_in"), ",\s*")).alias("genre")).filter(col("genre").isNotNull())
genres = genres.withColumn("genre", trim(col("genre")))
genres.groupBy("genre").count().orderBy("count", ascending=False).show(5, truncate=False)

# 4. Guardar los resultados procesados
output_path = "/home/andrea-rodriguez/Downloads/resultados_netflix"
df.write.mode("overwrite").csv(output_path, header=True)

print(f"Resultados del procesamiento batch guardados en: {output_path}")

# ============================================================
# PROCESAMIENTO EN TIEMPO REAL (STREAMING)
# ============================================================

# Nota: esta parte requirió crear la carpeta:
# mkdir /home/andrea-rodriguez/stream_input
# y luego agregar manualmente archivos CSV mientras Spark está corriendo.

print("=== Iniciando simulación de procesamiento en tiempo real ===")

schema = (
    "show_id STRING, type STRING, title STRING, director STRING, cast STRING, "
    "country STRING, date_added STRING, release_year INT, rating STRING, "
    "duration STRING, listed_in STRING, description STRING"
)

# Lectura continua (simulación de streaming)
stream_df = (
    spark.readStream
    .option("sep", ",")
    .option("header", "true")
    .schema(schema)
    .csv("/home/andrea-rodriguez/stream_input")
)

# Conteo dinámico de títulos por tipo (Movie / TV Show)
counts = stream_df.groupBy("type").count()

# Salida en consola
query = (
    counts.writeStream
    .outputMode("complete")
    .format("console")
    .start()
)

print("Esperando llegada de nuevos datos al directorio /stream_input ...")
print("Ctrl + C para detener el streaming.")

# Esperar a que termine el streaming
query.awaitTermination()

# ============================================================
# FINALIZAR SESIÓN SPARK
# ============================================================

spark.stop()
print("Sesión Spark finalizada correctamente.")
