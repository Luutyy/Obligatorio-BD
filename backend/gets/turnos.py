from fastapi import Depends, HTTPException
from backend.auth import SOLO_ADMIN, ADMIN_Y_PLANILLERO, db_para_usuario
from backend.app import app

#Admin y planillero
@app.get("/turnos")
def listar_turnos(
    user=Depends(ADMIN_Y_PLANILLERO),
    conexion=Depends(db_para_usuario)
):
    sql = """
        SELECT id_turno,
               CAST(hora_inicio AS CHAR) AS hora_inicio,
               CAST(hora_fin AS CHAR) AS hora_fin
        FROM turno
        ORDER BY id_turno
    """

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql)
    resultado = cursor.fetchall()
    cursor.close()

    return resultado
