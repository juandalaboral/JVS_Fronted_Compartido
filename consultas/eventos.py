import sys
import os

# Asegurar que encuentre la carpeta 'utilidades'
ruta_consultas = os.path.dirname(os.path.abspath(__file__))
ruta_raiz = os.path.dirname(ruta_consultas)
if ruta_raiz not in sys.path:
    sys.path.append(ruta_raiz)

from utilidades.conexion import conectar

# 1. LISTAR EVENTOS
def listar_eventos():
    """Trae la lista básica de todos los eventos programados"""
    conexion = conectar()
    cursor = conexion.cursor()
    
    # Seleccionamos solo las columnas seguras que sí existen en tu Módulo 2
    cursor.execute("""
        SELECT Evento_Id, Nombre, Fecha, Descripcion
        FROM Evento
    """)
    
    datos = cursor.fetchall()
    conexion.close()
    return datos

# 2. BUSCAR EVENTO
def buscar_evento(evento_id):
    """Busca un evento específico por su ID"""
    conexion = conectar()
    cursor = conexion.cursor()
    
    cursor.execute("""
        SELECT Evento_Id, Nombre, Fecha, Descripcion
        FROM Evento 
        WHERE Evento_Id = ?
    """, (evento_id,))
    
    evento = cursor.fetchone()
    conexion.close()
    return evento

# 3. CREAR EVENTO
def crear_evento(evento_id, nombre, fecha):
    """Inserta un nuevo evento en la base de datos"""
    conexion = conectar()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            INSERT INTO Evento (Evento_Id, Nombre, Fecha) 
            VALUES (?, ?, ?)
        """, (evento_id, nombre, fecha))
        conexion.commit()
        return True
    except Exception as e:
        print(f"❌ Error al crear evento: {e}")
        return False
    finally:
        conexion.close()

# 4. ACTUALIZAR EVENTO
def actualizar_evento(evento_id, nuevo_nombre, nueva_fecha):
    """Modifica los datos de un evento existente"""
    conexion = conectar()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            UPDATE Evento 
            SET Nombre = ?, Fecha = ? 
            WHERE Evento_Id = ?
        """, (nuevo_nombre, nueva_fecha, evento_id))
        conexion.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"❌ Error al actualizar evento: {e}")
        return False
    finally:
        conexion.close()

# 5. ELIMINAR EVENTO
def eliminar_evento(evento_id):
    """Elimina un evento por su ID"""
    conexion = conectar()
    cursor = conexion.cursor()
    try:
        cursor.execute("DELETE FROM Evento WHERE Evento_Id = ?", (evento_id,))
        conexion.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"❌ Error al eliminar evento: {e}")
        return False
    finally:
        conexion.close()

# 6. CONSULTAR AFORO
def consultar_aforo():
    """
    Une las funciones y localidades para saber el stock total 
    de boletas planeadas/disponibles por cada evento en el sistema.
    """
    conexion = conectar()
    cursor = conexion.cursor()
    
    cursor.execute("""
        SELECT E.Nombre, F.Fecha, F.Hora, SUM(FL.Stock) as Aforo_Total
        FROM Evento E
        JOIN Evento_Boleta EB ON E.Evento_Id = EB.Evento_Id
        JOIN Boleta B ON EB.Boleta_Id = B.Boleta_Id
        JOIN Funcion_Localidad FL ON B.Funcion_Localidad_Id = FL.Funcion_Localidad_Id
        JOIN Funcion F ON FL.Funcion_Id = F.Funcion_Id
        GROUP BY E.Evento_Id, F.Funcion_Id
    """)
    
    datos = cursor.fetchall()
    conexion.close()
    return datos