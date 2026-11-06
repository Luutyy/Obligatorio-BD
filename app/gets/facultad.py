from fastapi import Depends, HTTPException
from app.auth import SOLO_ADMIN, ADMIN_Y_PLANILLERO, db_para_usuario
from app.app import app

#Admin y planillero
@app.get("/facultades")
def listar_facultades(
    user=Depends(ADMIN_Y_PLANILLERO),
    conexion=Depends(db_para_usuario)
):
    sql = """
        SELECT id_facultad, nombre
        FROM facultad
        ORDER BY nombre
    """

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql)
    resultado = cursor.fetchall()
    cursor.close()

    return resultado