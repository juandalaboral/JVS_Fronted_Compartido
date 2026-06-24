import os
import sys

from flask import Flask, jsonify

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from consultas.eventos import consultar_aforo, listar_eventos

app = Flask(__name__)
@app.after_request
def permitir_frontend_local(respuesta):
    respuesta.headers["Access-Control-Allow-Origin"] = "*"
    respuesta.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    respuesta.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return respuesta


def convertir_evento_a_json(evento):
    """Convierte la tupla de consultas/eventos.py en un objeto JSON claro."""
    evento_id, nombre, fecha, descripcion = evento
    return {
        "id": evento_id,
        "nombre": nombre,
        "fecha": fecha,
        "descripcion": descripcion,
        "Descripcion": descripcion,
        "funciones": []
    }


@app.get("/api/eventos")
def obtener_eventos():
    """Devuelve eventos reales leidos desde SQLite usando consultas/eventos.py."""
    try:
        eventos = [convertir_evento_a_json(evento) for evento in listar_eventos()]
        eventos_por_nombre = {evento["nombre"]: evento for evento in eventos}

        for nombre, fecha, hora, aforo_total in consultar_aforo():
            evento = eventos_por_nombre.get(nombre)
            if evento is None:
                continue

            evento["funciones"].append({
                "fecha": fecha,
                "hora": hora,
                "aforo_total": aforo_total
            })

        return jsonify({
            "ok": True,
            "total": len(eventos),
            "eventos": eventos
        })
    except Exception as error:
        return jsonify({
            "ok": False,
            "error": str(error)
        }), 500


@app.get("/")
def inicio():
    return jsonify({
        "ok": True,
        "mensaje": "API de boleteria activa",
        "endpoint_eventos": "/api/eventos"
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)