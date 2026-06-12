import sys
import os

# Asegurar que encuentre la carpeta 'utilidades'
ruta_consultas = os.path.dirname(os.path.abspath(__file__))
ruta_raiz = os.path.dirname(ruta_consultas)
if ruta_raiz not in sys.path:
    sys.path.append(ruta_raiz)

from utilidades.conexion import conectar

def registrar_venta(boleta_id, usuario_id, pasarela_id=1):
    """
    Registra la venta en Detalle_Pago asegurando previamente 
    que existan los IDs en las tablas padres para evitar el IntegrityError.
    """
    conexion = conectar()
    cursor = conexion.cursor()
    
    try:
        # 1. Forzamos la creación del Usuario 1 si no existe
        cursor.execute("""
            INSERT OR IGNORE INTO Usuario (Usuario_Id, Nombre, Apellido, Correo, Contrasena) 
            VALUES (?, 'Usuario', 'Temporal', 'temp@correo.com', '123')
        """, (usuario_id,))
        
        # 2. Forzamos la creación de la Pasarela 1 si no existe
        cursor.execute("""
            INSERT OR IGNORE INTO Pasarela_Pago (Pasarela_Id, Nombre_Pasarela, Estado) 
            VALUES (?, 'Pasarela Global', 'Activo')
        """, (pasarela_id,))
        
        # 3. Forzamos la creación de la Boleta 1 si no existe
        # (Le pasamos 1 al campo de la función/localidad por si es obligatorio)
        cursor.execute("""
            INSERT OR IGNORE INTO Boleta (Boleta_Id, Funcion_Localidad_Id, Codigo_Barras, Estado) 
            VALUES (?, 1, 'TEMP-CODE-123', 'Vendido')
        """, (boleta_id,))
        
        # 4. Ahora que todos los padres existen sí o sí, metemos la venta de forma segura
        cursor.execute("""
            INSERT INTO Detalle_Pago 
            VALUES (NULL, ?, ?, ?)
        """, (boleta_id, usuario_id, pasarela_id))
        
        conexion.commit()
        return True
    except Exception as e:
        print(f"❌ Error interno en la transacción de venta: {e}")
        return False
    finally:
        conexion.close()

def listar_historial_ventas():
    """
    Historial inteligente: Trae los datos de los compradores uniendo 
    las tablas de forma limpia y directa.
    """
    conexion = conectar()
    cursor = conexion.cursor()
    
    try:
        cursor.execute("""
            SELECT U.Nombre || ' ' || U.Apellido as Cliente,
                   'Boleto ID: ' || DP.Boleta_Id as Item
            FROM Detalle_Pago DP
            JOIN Usuario U ON DP.Usuario_Id = U.Usuario_Id
        """)
        datos = cursor.fetchall()
        return datos
    except Exception as e:
        print(f"❌ Error al consultar historial: {e}")
        return []
    finally:
        conexion.close()