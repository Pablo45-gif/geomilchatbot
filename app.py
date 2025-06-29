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
## Información Corporativa
Geomil Group es una empresa líder en soluciones logísticas local e internacional con sede en las principales ciudades del Ecuador.

## Servicios Principales
1. **Envios Internacionales**:
   - Cobertura a España, EEUU, y Venezuela
   - Tiempos de entrega: 5-7 días hábiles para España y EEUU, y de 10-12 días hábiles a Venezuela
   - Seguridad y Eficiencia en cada envío

2. **Servicios Adicionales**:
   - Compras en línea mediante nuestro casillero en las principales tiendas virtuales de España y EEUU
   - Pedidos Temu
   - Manejo de aduanas
3. REGLA DE REDONDEO DE PESO PARA ENVÍOS DE ESPAÑA
   -Cuando se calcula el peso de un paquete, se aplica la siguiente regla:
   -Si el peso esta entre 1 kilo y 1.5 se cobra por 1.5 kilos
   -Si el peso esta entre 1.6 kilo y 2 se cobra por 2 kilos
   -Si el peso esta entre 2.1 kilo y 2.5 se cobra por 2.5 kilos
   -Si el peso esta entre 2.6 kilo y 3 se cobra por 3 kilos
   -Si el peso esta entre 3.1 kilo y 3.5 se cobra por 3.5 kilos
   -Si el peso esta entre 3.6 kilo y 4 se cobra por 4 kilos
   -Este patrón se repite sucesivamente

4. REGLA DE REDONDEO DE PESO PARA ENVÍOS DE EEUU
   -Cuando se calcula el peso de un paquete, se aplica la siguiente regla:
 -Si el peso esta entre 1.6 y 2.0 lb → se cobra por 2.0 lb
 -Si el peso esta entre2.1 y 2.5 lb → se cobra por 2.5 lb
 -Si el peso esta entre 2.6 y 3.0 lb → se cobra por 3.0 lb
 -Si el peso esta entre 3.1 y 3.5 lb → se cobra por 3.5 lb
 -Si el peso esta entre 3.6 y 4.0 lb → se cobra por 4.0 lb
 -Si el peso esta entre 4.1 y 4.5 lb → se cobra por 4.5 lb
 -Si el peso esta entre 4.6 y 5.0 lb → se cobra 5.0 lb
 -Si el peso esta entre 5.1 y 5.5 lb → se cobra 5.5 lb
 -Si el peso esta entre 5.6 y 6.0 lb → se cobra 6.0 lb
 -Si el peso esta entre 6.1 y 6.5 lb → se cobra 6.5 lb
 -Si el peso esta entre 6.6 y 7.0 lb → se cobra 7.0 lb
 -Si el peso esta entre 7.1 y 7.5 lb → se cobra 7.5 lb
 -Si el peso esta entre 7.6 y 8.0 lb → se cobra 8.0 lb
 -Si el peso esta entre 8.1 y 8.5 lb → se cobra 8.5 lb
 -Si el peso esta entre 8.6 y 9.0 lb → se cobra 9.0 lb
 -Si el peso esta entre 9.1 y 9.5 lb → se cobra 9.5 lb
 -Si el peso esta entre 9.6 y 10.0 lb → se cobra 10.0 lb
 -Si el peso esta entre 10.1 y 10.5 lb → se cobra 10.5 lb
 -Si el peso esta entre 10.6 y 11.0 lb → se cobra 11.0 lb
 -Si el peso esta entre 11.1 y 11.5 lb → se cobra 11.5 lb
 -Si el peso esta entre 11.6 y 12.0 lb → se cobra 12.0 lb
 -Si el peso esta entre 12.1 y 12.5 lb → se cobra 12.5 lb
 -Si el peso esta entre 12.6 y 13.0 lb → se cobra 13.0 lb
 -Si el peso esta entre 13.1 y 13.5 lb → se cobra 13.5 lb
 -Si el peso esta entre 13.6 y 14.0 lb → se cobra 14.0 lb
 -Si el peso esta entre 14.1 y 14.5 lb → se cobra 14.5 lb
 -Si el peso esta entre 14.6 y 15.0 lb → se cobra 15.0 lb
 -Si el peso esta entre 15.1 y 15.5 lb → se cobra 15.5 lb
 -Si el peso esta entre 15.6 y 16.0 lb → se cobra 16.0 lb
 -Si el peso esta entre 16.1 y 16.5 lb → se cobra 16.5 lb
 -Si el peso esta entre 16.6 y 17.0 lb → se cobra 17.0 lb
 -Si el peso esta entre 17.1 y 17.5 lb → se cobra 17.5 lb
 -Si el peso esta entre 17.6 y 18.0 lb → se cobra 18.0 lb
 -Si el peso esta entre 18.1 a 18.5 lb → se cobra 18.5 lb
 -Si el peso esta entre 18.6 a 19.0 lb → se cobra 19.0 lb
 -Si el peso esta entre 19.1 a 19.5 lb → se cobra 19.5 lb
 -Si el peso esta entre 19.6 a 20.0 lb → se cobra 20.0 lb
-Este patrón se repite sucesivamente
  

## Políticas Importantes
- Horario de atención: Lunes a Viernes 8:00 a 18:00 y Sabados de: 9:00 a 14:00, no cerramos a medio día
- Soporte: +593 997100350

## Preguntas Frecuentes
Q: ¿Qué documentación necesito para enviar un paquete a España?
A: Para enviar a 🇪🇸 España es obligatorio: DNI o NIE del beneficiario así como su dirección de domicilio, código postal y número de teléfono.

Q: ¿Qué documentación necesito para enviar un paquete a EEUU?
A: Para enviar a 🇺🇸 Estados Unidos se requiere la cédula de identidad ecuatoriana o la licencia de conducir del beneficiario así como su dirección de domicilio, código postal y número de teléfono.

Q: ¿Cómo rastreo mi envío?
A: Puede rastrearlo en nuestra web con el código que recibió al enviar su paquete.

Q: ¿Cuál es el costo del envío a España a agencia?
A: Primer kilo: *$15,98* (debido al valor de corte guía exigido por la aduana).
- Desde el segundo kilo en adelante: *$11,83* por kilo.,
- Puedes enviar hasta *4 kilos sin problema, si pasa deberiamos hacer otro paquete. Siempre se debe enviar en caja de cartón
- Documentos tienen un valor de envío de 20,58.
- Peso del medio kilo 5,92
- PESO MINIMO DE ENVIO ES 1 KILO

Q: ¿Cuál es el costo del envío a EEUU a agencia?
A: Tarifas de envío a las agencias GEOMIL en 🇺🇸 Estados Unidos (EE.UU.):
-primera libra: *$11,30* (debido al valor de corte guía exigido por la aduana).
-Desde la segunda libra en adelante : *$6,15* por libra.
-Se debe enviar un mínimo de 2 libras hasta *20 libras sin problema. Siempre se debe enviar en caja de cartón
- Documentos tienen un valor de envío de 25,68. No se pueden enviar paquetes con documentos 
- PESO DE LA MEDIA LIBRA 3,075
- PESO MINIMO DE ENVIO 2 LIBRAS

Q: ¿Cuál es el costo del envío a España a Domicilio?
A: Primer kilo: *$24,72* (debido al valor de corte guía exigido por la aduana).
- Desde el segundo kilo en adelante: *$20,57* por kilo.
- Puedes enviar hasta *4 kilos sin problema, si pasa deberiamos hacer otro paquete. Siempre se debe enviar en caja de cartón
- Documentos tienen un valor de envío de 25,76. No se pueden enviar paquetes con documentos.
-

Q: ¿Cuál es el costo del envío a EEUU a Domicilio?
A: Tarifas de envío a las agencias GEOMIL en 🇺🇸 Estados Unidos (EE.UU.):
-Primera libra: $15,95* (debido al valor de corte guía exigido por la aduana).
-Desde la Segunda libra en adelante : *$10,80* por libra.
-Debes enviar siempre un minimo 3 libras hasta 20 libras. Siempre se debe enviar en caja de cartón
- Documentos tienen un valor de envío de 30,85. No se pueden enviar paquetes con documentos 

Q: ¿Fechas de embarque o salida del país?
A: 'Para 🇪🇸 España: lunes, miércoles y viernes.
Para 🇺🇸 Estados Unidos: martes y jueves. Y Venezuela los días Viernes
✨ Trae tu paquete un día antes del embarque para que pueda salir sin contratiempos en los días programados. ¡Así garantizas un envío más rápido y eficiente!

Q: ¿Que agencias tienen disponibles en España?
A: 
ALCANTARILLA UBICADA EN CALLE MAYOR, 182
ALHAMA DE MURCIA UBICADA EN CALLE CAPITAN PORTOLA 25, BAJO IZQ.
ALICANTE UBICADA EN CALLE MUSICO ALFONSEA, 7 BJ D
ALMERIA  UBICADA EN CALLE Murcia #43, Bajo
ALQUERIA (MURCIA) UBICADA EN PLAZA NUESTRA SEÑORA DE LA OLIVA, 4 BAJO
BILBAO UBICADA EN CALLE SERANTES, 1 LOCAL 1F
BURLADA (NAVARRA) UBICADA EN CALLE DE LAS MAESTRAS 2 BAJO
CIEZA UBICADA EN CALLEDOÑA ADELA ,6 BAJO IZQ LOC. AL
COLLADO VILLALBA UBICADA EN TRAVESIA DE LA VENTA, 1-3 LOC. AL 5
FUENTE ALAMO UBICADA EN CALLE DR FLEMING, 3
GUADALAJARA UBICADA EN CALLE ALONSO NUÑEZ DE REINOSO #1
HOSPITALET DE LLOBREGAT UBICADA EN CARRETERA DE COLLBLANC 237 
BARCELONA UBICADA EN CALLE SARDENYA #163 - 167 LOCAL 10 BAJO 9
IBI UBICADA EN PLAZA MIGUEL SERVET Nº 4
JUMILLA UBICADA EN AV. MURCIA Nº 32
MAZARRON UBICADA EN CALLE CARMEN BAJO Nº 2
MOLINA DE SEGURA UBICADA EN CALLE TRES DE ABRIL, 6 BAJO-IZDA
MULA UBICADA EN CALLE BOTICAS Nº11
OVIEDO UBICADA EN CALLE LUIS BRAILE, 8
PALMA DE MALLORCA UBICADA EN CALLE FRANCESC SANCHO Nº 16
PAMPLONA UBICADA EN AV MARCELO CELAYETA, 131 BAJO FRENTE  SANITAS
PUERTO DE MAZARRÓN UBICADA EN CALLE FRANCISCO YUFERA, 9 BAJO
SAN PEDRO DE ALCANTARA UBICADA EN CALLE JUAN RAMON JIMENEZ, 11
TORRE PACHECO UBICADA EN CALLE CARTAGENA #57 LOCAL 1
SANTANDER UBICADA EN CALLEJERONIMO SAINZ DE LA MAZA, 1
VALENCIA UBICADA EN AVDA CONSTITUCION, 220 BAJO
VALLADOLID UBICADA EN CALLE PRÍNCIPE N.º 7 LOCAL 1
VERA UBICADA EN ALFREDO ALMUNIA  # 13 
VILLAFRANCA (NAVARRA) UBICADA EN CALLEPortillo 5, local
YECLA UBICADA EN CALLE CRUZ DE PIEDRA, 23
ZARAGOZA UBICADA EN CALLE CONDE DE ARANDA, 3
LORCA UBICADA EN CALLE JUAN XXIII Nº 4
MURCIA UBICADA EN CALLE BOLOS S/N( DENTRO ESTACION AUTOBUSES) LOCAL 26B
TOTANA UBICADA EN RAMBLA DE LA SANTA 21 BAJO 1 
CARTAGENA UBICADA EN CALLE CARLOS III Nº 46 BAJO

Q: ¿Que agencias tienen en Madrid?
A: GEOMIL Central ubicada en Calle Buen Gobernador,2
GEOMIL COSLADA ubicada en Av. Constitución 24, Naves 8 y 9
GEOMIL METRO TETUAN ubicada en EN Calle HIERBABUENA #15
GEOMIL METRO PALOS DE LA FRONTERA ubicada en EN Calle BATALLA DEL SALADO Nº 7
GEOMIL METRO  LEGAZPI ubicada EN Calle EMBAJADORES 176
GEOMIL METRO OPORTO ubicada EN Calle PELICANO 25 
GEOMIL METRO  CUATRO CAMINOS ubicada  EN Calle LOS ARTISTAS Nº 16 

Q: ¿Que agencias tienen en el Estado de NJ?
A: TENEMOS AGENCIAS EN:
HARRISON en 307 HARRISON AV.
BOGOTA en 191 OAKWOOD AVE
HACKENSACK en 53 MAIN ST.
NORTH BERG en 7215 BERGENLINE AVE
UNION CITY en 32-27 BERGENLINE AVE.
NEWARK en 94 FRANKLIN ST.
NEWARK en 352  BLOOMFIELD AVE.
NEWARK en 174 ADAMS ST 307 CHESNUT ST
NORTH PLAINFIELD en 262 SOMERSET ST
ELIZABETH en 655 ELIZABETH AVE
LAKEWOOD en 588 WOODBINE LN, LAKEWOOD, NJ 08701

Q: ¿Que agencias tienen en el estado de NY?
A: TENEMOS AGENCIAS EN:
CORONA QNNS en 111-15 ROOSEVELT AVE
BRONX en 1347 HOE AVE
OSSINING en 22 CROSTON AVE.

Q: ¿Que agencias tienen en el estado de CONNECTICUT?
A: TENEMOS AGENCIAS EN:
EAST HAVEN en 199 SALTONSTALL PKWAY
NORWALK en 72 West Ave 

Q: ¿Que agencias tienen en el estado de MD?
A: TENEMOS AGENCIAS EN:
WORCHESTER 5 DANNY ST ubicada en 5 DANNY ST
BELTSVILLE-MARYLAND ubicada en 13020 BELLEVUE ST. BELTSVILLE. MD  

Q: ¿Que agencias tienen en EEUU?
A: TENEMOS AGENCIAS EN LOS ESTADOS DE NEW JERSEY, NEW YORK , DAMBURY y Massachusetts

Q: ¿Cuál es la direccion de la agencia GEOMIL Loja Cuxibamba?
A: La agencia se encuentra ubicada en la calle Guaranda y Ancón,Loja

Q: ¿Manejan mercancía peligrosa?
A: No, por el momento.

Q: ¿DE QUE SE TRATA EL Nuevo Pago Arancelario por Compra DE 20 DOLARES?
A: Todas las compras realizadas desde el exterior, estarán sujetas a un pago adicional de $20.00 por paquete. Siempre y cuando el paquete sea declarado en Categoría B (4x4), es decir paquetes que tengan un peso de hasta 4Kg y un valor máximo de hasta $400.00.

Q: ¿QUE ALIEMENTOS PODEMOS ENVIAR?
A: Los perecibles y frutas deben ser enviados en cajas térmicas y las carnes no deben estar crudas. EL CUY EMBASADO AL VACÍO, prohibida la carne de chancho o cerdo como fritada
   No se permite el envío de más de 3 unidades del mismo producto por paquete.

Q: ¿Se puden enviar Tamales y Humas?
A: Si se puede enviar, pero deben estar empacadas al vacío, la agencia cuenta con empacadora al vacío así que no vas a tener ningún problema.
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
