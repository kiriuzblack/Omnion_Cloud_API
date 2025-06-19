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
    # Leer credenciales desde la variable de entorno
    credenciales_json = os.environ.get("GOOGLE_CREDENTIALS")

    if not credenciales_json:
        raise Exception("Variable de entorno 'GOOGLE_CREDENTIALS' no está definida")

    creds_dict = json.loads(credenciales_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).sheet1
    return sheet

@app.route("/api/guardar", methods=["POST"])
def guardar():
    data = request.get_json()
    pregunta = data.get("pregunta")
    respuesta = data.get("respuesta")
    hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        sheet = conectar_google_sheets()
        sheet.append_row([hora, pregunta, respuesta])
        return jsonify({"mensaje": "Guardado con éxito"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/historial", methods=["GET"])
def historial():
    try:
        sheet = conectar_google_sheets()
        registros = sheet.get_all_records()
        return jsonify(registros)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
