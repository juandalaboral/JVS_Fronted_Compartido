import os
import sys
from datetime import datetime

ruta_consultas = os.path.dirname(os.path.abspath(__file__))
ruta_raiz = os.path.dirname(ruta_consultas)
if ruta_raiz not in sys.path:
    sys.path.append(ruta_raiz)

from utilidades.conexion import conectar


def asegurar_tabla_asientos(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Asiento_Ocupado (
            Asiento_Ocupado_Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Evento_Id INTEGER NOT NULL,
            Funcion_Id INTEGER NOT NULL,
            Asiento TEXT NOT NULL,
            Estado TEXT NOT NULL DEFAULT 'Ocupado',
            Fecha_Compra TEXT NOT NULL,
            Evento_Nombre TEXT,
            Fecha_Evento TEXT,
            UNIQUE(Evento_Id, Funcion_Id, Asiento)
        )
    """)


def normalizar_texto(valor):
    return (valor or "").strip().lower()


def resolver_evento_id(cursor, datos):
    evento_id = datos.get("evento_id") or datos.get("Evento_Id")
    if evento_id is not None:
        try:
            return int(evento_id)
        except (TypeError, ValueError):
            pass

    evento_nombre = (datos.get("evento") or datos.get("nombre_evento") or "").strip()
    if not evento_nombre:
        return 0

    cursor.execute("SELECT Evento_Id FROM Evento WHERE LOWER(Nombre) = LOWER(?) LIMIT 1", (evento_nombre,))
    exacto = cursor.fetchone()
    if exacto:
        return exacto[0]

    cursor.execute("SELECT Evento_Id, Nombre FROM Evento")
    nombre_buscado = normalizar_texto(evento_nombre)
    for evento_id_db, nombre_db in cursor.fetchall():
        nombre_db_norm = normalizar_texto(nombre_db)
        if nombre_buscado in nombre_db_norm or nombre_db_norm in nombre_buscado:
            return evento_id_db

    return 0


def resolver_funcion_id(cursor, datos, evento_id):
    funcion_id = datos.get("funcion_id") or datos.get("Funcion_Id")
    if funcion_id is not None:
        try:
            return int(funcion_id)
        except (TypeError, ValueError):
            pass

    fecha_evento = (datos.get("fecha") or datos.get("fecha_evento") or "").strip()
    if not fecha_evento:
        return 0

    cursor.execute("""
        SELECT DISTINCT F.Funcion_Id, F.Fecha
        FROM Evento_Boleta EB
        JOIN Boleta B ON EB.Boleta_Id = B.Boleta_Id
        JOIN Funcion_Localidad FL ON B.Funcion_Localidad_Id = FL.Funcion_Localidad_Id
        JOIN Funcion F ON FL.Funcion_Id = F.Funcion_Id
        WHERE EB.Evento_Id = ?
        ORDER BY F.Funcion_Id
    """, (evento_id,))

    fecha_norm = normalizar_texto(fecha_evento)
    for funcion_id_db, fecha_db in cursor.fetchall():
        fecha_db_norm = normalizar_texto(fecha_db)
        if fecha_db_norm and (fecha_db_norm in fecha_norm or fecha_norm in fecha_db_norm):
            return funcion_id_db

    return 0


def contexto_asientos(datos):
    conexion = conectar()
    cursor = conexion.cursor()
    asegurar_tabla_asientos(cursor)
    evento_id = resolver_evento_id(cursor, datos)
    funcion_id = resolver_funcion_id(cursor, datos, evento_id)
    conexion.commit()
    conexion.close()
    return evento_id, funcion_id


def consultar_asientos_ocupados(datos):
    conexion = conectar()
    cursor = conexion.cursor()
    asegurar_tabla_asientos(cursor)
    evento_id = resolver_evento_id(cursor, datos)
    funcion_id = resolver_funcion_id(cursor, datos, evento_id)

    cursor.execute("""
        SELECT Asiento
        FROM Asiento_Ocupado
        WHERE Evento_Id = ? AND Funcion_Id = ? AND Estado = 'Ocupado'
        ORDER BY Asiento
    """, (evento_id, funcion_id))

    asientos = [fila[0] for fila in cursor.fetchall()]
    conexion.commit()
    conexion.close()
    return {
        "evento_id": evento_id,
        "funcion_id": funcion_id,
        "asientos": asientos
    }


def registrar_asientos_ocupados(datos):
    asientos = datos.get("asientos") or []
    if not isinstance(asientos, list) or len(asientos) == 0:
        raise ValueError("Debe enviar al menos un asiento")

    conexion = conectar()
    cursor = conexion.cursor()
    asegurar_tabla_asientos(cursor)

    evento_id = resolver_evento_id(cursor, datos)
    funcion_id = resolver_funcion_id(cursor, datos, evento_id)
    evento_nombre = (datos.get("evento") or datos.get("nombre_evento") or "").strip()
    fecha_evento = (datos.get("fecha") or datos.get("fecha_evento") or "").strip()
    fecha_compra = datetime.now().isoformat(timespec="seconds")

    try:
        for asiento in asientos:
            cursor.execute("""
                INSERT OR IGNORE INTO Asiento_Ocupado
                    (Evento_Id, Funcion_Id, Asiento, Estado, Fecha_Compra, Evento_Nombre, Fecha_Evento)
                VALUES
                    (?, ?, ?, 'Ocupado', ?, ?, ?)
            """, (evento_id, funcion_id, str(asiento), fecha_compra, evento_nombre, fecha_evento))

        conexion.commit()
        return consultar_asientos_ocupados({
            "evento_id": evento_id,
            "funcion_id": funcion_id,
            "evento": evento_nombre,
            "fecha": fecha_evento
        })
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()