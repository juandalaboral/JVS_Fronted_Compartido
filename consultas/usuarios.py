import sys
import os

# Agregamos la carpeta raíz al sistema para que encuentre 'utilidades'
ruta_consultas = os.path.dirname(os.path.abspath(__file__))
ruta_raiz = os.path.dirname(ruta_consultas)
if ruta_raiz not in sys.path:
    sys.path.append(ruta_raiz)

# Ahora el import funcionará siempre, uses o no el botón de Play de VS Code
from utilidades.conexion import conectar

def listar_usuarios():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT *
    FROM Usuario
    """)

    datos = cursor.fetchall()
    conexion.close()
    return datos