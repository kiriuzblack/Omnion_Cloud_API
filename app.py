from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
import json

app = Flask(__name__)

SHEET_NAME = "Historial Omnion"

def conectar_google_sheets():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    credenciales_json = os.environ.get("GOOGLE_CREDENTIALS")
    if not credenciales_json:
        raise Exception("❌ Variable de entorno 'GOOGLE_CREDENTIALS' no está definida")

    # Depuración: mostrar parte del contenido para asegurar que llegó bien
    print("🛠️ DEBUG: Recibida GOOGLE_CREDENTIALS (parcial):")
    print(credenciales_json[:300])

    try:
        credenciales_json = credenciales_json.replace("\\n", "\n")
        creds_dict = json.loads(credenciales_json)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        sheet = client.open(SHEET_NAME).sheet1
        return sheet
    except Exception as err:
        print("❌ Error al conectar con Google Sheets:", err)
        raise err

@app.route("/", methods=["GET"])
def index():
    return "🚀 Omnion API está activa y conectada con Google Sheets."

@app.route("/api/guardar", methods=["POST"])
def guardar():
    try:
        data = request.get_json(force=True)
        pregunta = data.get("pregunta")
        respuesta = data.get("respuesta")
        hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print("📝 Guardando pregunta:", pregunta)
        print("📘 Guardando respuesta:", respuesta)

        sheet = conectar_google_sheets()
        sheet.append_row([hora, pregunta, respuesta])
        return jsonify({"mensaje": "✅ Guardado con éxito"})
    except Exception as e:
        print("❌ ERROR EN /api/guardar:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route("/api/historial", methods=["GET"])
def historial():
    try:
        sheet = conectar_google_sheets()
        registros = sheet.get_all_records()
        print(f"📚 {len(registros)} registros obtenidos del historial")
        return jsonify(registros)
    except Exception as e:
        print("❌ ERROR EN /api/historial:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
