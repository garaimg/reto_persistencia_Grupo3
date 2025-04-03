import os
import sys
import pandas as pd
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Cargar variables de entorno
INFLUXDB_URL = os.getenv("INFLUXDB_URL")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET")

# Conectar con InfluxDB
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Cargar el dataset con fechas actualizadas a 2024
file_path = "dataset/T1.csv"
df = pd.read_csv(file_path)

# Mostrar las columnas originales
tmp_stderr = sys.stderr  # Redirigir stderr para debug
sys.stderr = sys.stdout  # Para ver el output en logs
print("Columnas originales:", df.columns.tolist(), file=sys.stderr)
print(df.head(), file=sys.stderr)
sys.stderr = tmp_stderr  # Restaurar stderr

# Convertir la columna de fecha a formato datetime y actualizar el año
df["timestamp"] = pd.to_datetime(df["Date/Time"], format="%d %m %Y %H:%M").apply(lambda x: x.replace(year=2024))

# Renombrar columnas correctamente
df = df.rename(columns={
    "LV ActivePower (kW)": "active_power_kw",
    "Wind Speed (m/s)": "wind_speed_mps",
    "Theoretical_Power_Curve (KWh)": "theoretical_power_kwh",
    "Wind Direction (°)": "wind_direction_deg"
})

# Seleccionar solo las columnas necesarias
columnas_finales = ["timestamp", "active_power_kw", "wind_speed_mps", "theoretical_power_kwh", "wind_direction_deg"]
df = df[columnas_finales]

# Mostrar la nueva estructura
tmp_stderr = sys.stderr
sys.stderr = sys.stdout
print("Columnas finales:", df.columns.tolist(), file=sys.stderr)
print(df.head(), file=sys.stderr)
sys.stderr = tmp_stderr

# Insertar datos en InfluxDB
for _, row in df.iterrows():
    point = (
        Point("wind_turbine_data")
        .time(row["timestamp"], WritePrecision.NS)
        .field("active_power_kw", row["active_power_kw"])
        .field("wind_speed_mps", row["wind_speed_mps"])
        .field("theoretical_power_kwh", row["theoretical_power_kwh"])
        .field("wind_direction_deg", row["wind_direction_deg"])
    )
    write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)

print("Datos insertados correctamente en InfluxDB")

