import requests

# URL base de tu API en Render
BASE_URL = "https://omnionia.onrender.com"

# Datos de prueba para guardar
payload = {
    "pregunta": "¿Qué es un agujero negro?",
    "respuesta": "Una región del espacio-tiempo con un campo gravitacional tan intenso que nada puede escapar."
}

# 1. Probar el endpoint POST /api/guardar
print("Enviando datos a la API...\n")
response = requests.post(f"{BASE_URL}/api/guardar", json=payload)
print("Respuesta del servidor:")
print(response.status_code, response.json())

# 2. Probar el endpoint GET /api/historial
print("\nConsultando historial...\n")
historial = requests.get(f"{BASE_URL}/api/historial")
print("Historial recibido:")
print(historial.status_code)
for fila in historial.json():
    print(fila)
