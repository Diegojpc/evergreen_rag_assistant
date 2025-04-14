# data_adapters.py
import datetime
import random

# --- Simuladores de APIs Externas ---

def get_weather_forecast(location: str) -> dict:
    """Simula la obtención del pronóstico del tiempo."""
    print(f"ADAPTER: Obteniendo pronóstico para {location} (simulado)")
    # En una implementación real, llamarías a una API de clima aquí
    # usando location (lat/lon o nombre) y la WEATHER_API_KEY
    today = datetime.date.today()
    forecast = {
        "location": location,
        "date_generated": today.isoformat(),
        "daily": []
    }
    for i in range(5): # Pronóstico para 5 días
        day = today + datetime.timedelta(days=i)
        forecast["daily"].append({
            "date": day.isoformat(),
            "temp_max_c": random.uniform(22.0, 32.0),
            "temp_min_c": random.uniform(10.0, 18.0),
            "precipitation_prob": random.random(), # Probabilidad de 0 a 1
            "precipitation_mm": random.uniform(0.0, 15.0) if random.random() < 0.4 else 0.0, # Lluvia si prob > 0.4
            "humidity_relative_avg": random.uniform(50.0, 90.0),
            "wind_speed_kmh": random.uniform(5.0, 25.0)
        })
    # Simular un riesgo específico basado en el pronóstico
    if any(d['humidity_relative_avg'] > 85 and d['temp_min_c'] > 15 for d in forecast['daily']):
         forecast["potential_risk"] = "Condiciones favorables para Mildiu detectadas en el pronóstico."
    else:
         forecast["potential_risk"] = "Sin riesgos climáticos mayores inmediatos en pronóstico."

    return forecast

def get_sensor_data(parcela_id: str) -> dict | None:
    """Simula la obtención de datos de sensores de una parcela."""
    print(f"ADAPTER: Obteniendo datos de sensores para {parcela_id} (simulado)")
    # Simular que no todas las parcelas tienen sensores
    if parcela_id != "PARCELA_123":
         print(f"ADAPTER: Parcela {parcela_id} no tiene sensores activos.")
         return None

    # Datos simulados
    return {
        "parcela_id": parcela_id,
        "timestamp": datetime.datetime.now().isoformat(),
        "soil_moisture_percent": random.uniform(35.0, 65.0), # Humedad volumétrica %
        "soil_temperature_c": random.uniform(18.0, 26.0),
        "air_temperature_c": random.uniform(20.0, 30.0),
        "conductivity_ms_cm": random.uniform(1.0, 2.5) # Conductividad eléctrica
    }

def get_recent_images_analysis(parcela_id: str) -> dict | None:
    """Simula el análisis de imágenes recientes."""
    print(f"ADAPTER: Obteniendo análisis de imagen para {parcela_id} (simulado)")
     # Simular que no hay imágenes recientes o análisis disponible
    if random.random() > 0.7: # 30% de las veces no hay análisis
         print(f"ADAPTER: No hay análisis de imagen reciente disponible para {parcela_id}.")
         return None

    # Simular resultado de un análisis (podría ser mucho más complejo)
    possible_issues = ["Coloración pálida (posible deficiencia N)", "Manchas sospechosas en hojas inferiores", "Estrés hídrico visible"]
    return {
        "parcela_id": parcela_id,
        "analysis_date": (datetime.date.today() - datetime.timedelta(days=random.randint(1,3))).isoformat(),
        "status": "Normal" if random.random() > 0.3 else "Anomalía Detectada", # 70% normal
        "detected_issue": random.choice(possible_issues) if random.random() > 0.3 else None,
        "coverage_percent": random.uniform(70.0, 95.0)
    }

def get_lunar_phase() -> dict:
    """Simula obtener la fase lunar actual."""
    print("ADAPTER: Obteniendo fase lunar (simulado)")
    phases = ["Nueva", "Creciente", "Llena", "Menguante"]
    # En una implementación real, usarías una librería o API astronómica
    return {
        "phase": random.choice(phases),
        "illumination_percent": random.uniform(0.0, 100.0)
    }

def get_project_details(project_id: str) -> dict | None:
    """Simula obtener detalles básicos del proyecto/cultivo."""
    print(f"ADAPTER: Obteniendo detalles del proyecto {project_id} (simulado)")
    # Aquí conectarías a tu base de datos de Evergreen
    if project_id == "PROJ_TOMATE_2024_P123":
        return {
            "project_id": project_id,
            "parcela_id": "PARCELA_123",
            "crop_type": "Tomate",
            "variety": "Daniela",
            "planting_date": "2024-03-20", # Fecha de siembra
            "current_phase": "Floración / Inicio Cuajado" # Determinado por fecha siembra o input manual
        }
    else:
        print(f"ADAPTER: Proyecto {project_id} no encontrado.")
        return None


if __name__ == "__main__":
    # Ejemplo de uso
    print("\n--- Probando Adaptadores ---")
    proj_id = "PROJ_TOMATE_2024_P123"
    parcela_id = "PARCELA_123"
    location = "Parcela 123 Finca Test"

    project_info = get_project_details(proj_id)
    print("\nDetalles Proyecto:", project_info)

    weather = get_weather_forecast(location)
    print("\nPronóstico Clima:", weather)

    sensors = get_sensor_data(parcela_id)
    print("\nDatos Sensores:", sensors)

    images = get_recent_images_analysis(parcela_id)
    print("\nAnálisis Imágenes:", images)

    lunar = get_lunar_phase()
    print("\nFase Lunar:", lunar)