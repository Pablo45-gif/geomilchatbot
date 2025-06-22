from flask import Flask, request, jsonify
from flask_cors import CORS
import socket
import logging
import requests

# Configuración básica de Flask
app = Flask(__name__)
CORS(app)  # Permitir CORS para todas las rutas

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración OpenRouter
API_KEY = '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'  # Cambia por tu clave válida
API_BASE = "https://openrouter.ai/api/v1"

# Base de conocimiento Geomil Group
GEOMIL_KNOWLEDGE = """
[Aquí va todo el texto largo de Geomil que tengas]
"""

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "active",
        "service": "Geomil Group AI",
        "host": socket.gethostname(),
        "ip": socket.gethostbyname(socket.gethostname()),
        "endpoints": {
            "ask": "POST /ask",
            "health": "GET /health"
        }
    })

@app.route('/ask', methods=['POST'])
def ask_ai():
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        if not user_message:
            return jsonify({"error": "El campo 'message' es requerido"}), 400

        logger.info(f"Procesando pregunta: {user_message}")

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "deepseek/deepseek-r1:free",
            "messages": [
                {
                    "role": "system",
                    "content": f"""Eres un asistente especializado en Geomil Group. Usa esta información para responder:
                    {GEOMIL_KNOWLEDGE}

                    INSTRUCCIONES:
                    1. Sé profesional pero amable (tono cercano pero formal)
                    2. Si no sabes la respuesta, pide aclaración
                    3. Da detalles concretos si existen
                    4. Para temas técnicos, remite a soporte oficial
                    5. Respuestas cortas, máximo 2 párrafos
                    6. No uses asteriscos
                    7. Usa emojis, pero sin saturar
                    8. Muestra sumas o multiplicaciones solo si te preguntan explícitamente"""
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            "temperature": 0.5,
            "max_tokens": 550
        }

        response = requests.post(f"{API_BASE}/chat/completions", headers=headers, json=payload)
        response_json = response.json()

        if response.status_code == 200:
            ai_response = response_json["choices"][0]["message"]["content"].replace('*', '')
            logger.info(f"Respuesta generada: {ai_response}")
            return jsonify({
                "response": ai_response,
                "model": response_json.get("model", ""),
                "tokens_used": response_json.get("usage", {}).get("total_tokens", 0)
            })
        else:
            logger.error(f"Error OpenRouter {response.status_code}: {response_json}")
            return jsonify({
                "error": "Error de API OpenRouter",
                "details": response_json
            }), response.status_code

    except Exception as e:
        logger.error(f"Error en /ask: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Error procesando la solicitud",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    from werkzeug.serving import run_simple

    host = '127.0.0.1'
    port = 5000

    logger.info(f"""
    🚀 Iniciando servidor Flask en {host}:{port}
    🔗 URL local: http://{host}:{port}/health
    🌐 URL red: http://{socket.gethostbyname(socket.gethostname())}:{port}/health
    """)

    run_simple(
        hostname=host,
        port=port,
        application=app,
        use_reloader=False,
        use_debugger=False,
        threaded=True
    )
