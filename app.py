import os
import sys

from flask import Flask, jsonify, request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from consultas.eventos import actualizar_evento_desde_booking, consultar_aforo, listar_eventos
from consultas.usuarios import crear_usuario
from consultas.asientos import consultar_asientos_ocupados, registrar_asientos_ocupados

app = Flask(__name__)


@app.after_request
def permitir_frontend_local(respuesta):
    respuesta.headers["Access-Control-Allow-Origin"] = "*"
    respuesta.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, OPTIONS"
    respuesta.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return respuesta


def convertir_evento_a_json(evento):
    """Convierte la tupla de consultas/eventos.py en un objeto JSON claro."""
    evento_id, nombre, fecha, descripcion, hora, lugar, imagen = evento
    return {
        "id": evento_id,
        "nombre": nombre,
        "fecha": fecha,
        "hora": hora,
        "lugar": lugar,
        "ubicacion": lugar,
        "imagen": imagen,
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

        for nombre, fecha, hora, aforo_total, lugar in consultar_aforo():
            evento = eventos_por_nombre.get(nombre)
            if evento is None:
                continue

            evento["funciones"].append({
                "fecha": fecha,
                "hora": hora,
                "aforo_total": aforo_total,
                "lugar": lugar
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


@app.put("/api/eventos/<int:evento_id>")
def actualizar_evento_api(evento_id):
    """Actualiza un evento real de SQLite desde Booking."""
    try:
        datos = request.get_json(silent=True) or {}
        evento = actualizar_evento_desde_booking(evento_id, datos)
        return jsonify({
            "ok": True,
            "mensaje": "Evento actualizado correctamente",
            "evento": convertir_evento_a_json(evento)
        })
    except ValueError as error:
        return jsonify({
            "ok": False,
            "error": str(error)
        }), 400
    except Exception as error:
        return jsonify({
            "ok": False,
            "error": str(error)
        }), 500



@app.get("/api/asientos-ocupados")
def obtener_asientos_ocupados_api():
    """Consulta asientos ocupados desde SQLite por evento/funcion o evento/fecha."""
    try:
        datos = {
            "evento_id": request.args.get("evento_id"),
            "funcion_id": request.args.get("funcion_id"),
            "evento": request.args.get("evento"),
            "fecha": request.args.get("fecha")
        }
        resultado = consultar_asientos_ocupados(datos)
        return jsonify({
            "ok": True,
            **resultado
        })
    except Exception as error:
        return jsonify({
            "ok": False,
            "error": str(error)
        }), 500


@app.post("/api/asientos-ocupados")
def registrar_asientos_ocupados_api():
    """Registra en SQLite los asientos comprados al confirmar una compra."""
    try:
        datos = request.get_json(silent=True) or {}
        resultado = registrar_asientos_ocupados(datos)
        return jsonify({
            "ok": True,
            "mensaje": "Asientos registrados correctamente",
            **resultado
        }), 201
    except ValueError as error:
        return jsonify({
            "ok": False,
            "error": str(error)
        }), 400
    except Exception as error:
        return jsonify({
            "ok": False,
            "error": str(error)
        }), 500

@app.post("/api/usuarios")
def registrar_usuario():
    """Registra usuarios desde la Vista Usuario y los guarda en SQLite."""
    try:
        datos = request.get_json(silent=True) or {}
        usuario = crear_usuario(datos)
        return jsonify({
            "ok": True,
            "mensaje": "Usuario registrado correctamente",
            "usuario": usuario
        }), 201
    except ValueError as error:
        return jsonify({
            "ok": False,
            "error": str(error)
        }), 400
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