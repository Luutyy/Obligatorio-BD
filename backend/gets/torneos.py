from fastapi import Depends, HTTPException
from backend.auth import SOLO_ADMIN, ADMIN_Y_PLANILLERO, db_para_usuario
from backend.app import app

# Admin y planillero
@app.get("/torneos")
def listar_torneos(
    user=Depends(ADMIN_Y_PLANILLERO),
    conexion=Depends(db_para_usuario)
):
    sql = """
        SELECT *
        FROM torneo
        ORDER BY anio DESC, semestre DESC
    """

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql)
    resultado = cursor.fetchall()
    cursor.close()

    return resultado

@app.get("/torneos/{id_torneo}")
def obtener_torneo(
    id_torneo: int,
    user=Depends(ADMIN_Y_PLANILLERO),
    conexion=Depends(db_para_usuario)
):
    sql = "SELECT * FROM torneo WHERE id_torneo = %s"

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql, (id_torneo,))
    resultado = cursor.fetchall()
    cursor.close()

    if not resultado:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")

    return resultado[0]