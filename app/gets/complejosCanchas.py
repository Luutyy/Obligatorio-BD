from fastapi import Depends, HTTPException
from app.auth import SOLO_ADMIN, ADMIN_Y_PLANILLERO, db_para_usuario
from app.app import app

@app.get("/complejos")
def listar_complejos(
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):
    sql = """
        SELECT *
        FROM complejo
        ORDER BY nombre_complejo
    """

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql)
    resultado = cursor.fetchall()
    cursor.close()

    return resultado


@app.get("/complejos/{id_complejo}")
def obtener_complejo(
    id_complejo: int,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):
    sql = """
        SELECT *
        FROM complejo
        WHERE id_complejo = %s
    """

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql, (id_complejo,))
    resultado = cursor.fetchall()
    cursor.close()

    if not resultado:
        raise HTTPException(status_code=404, detail="Complejo no encontrado")

    return resultado[0]

@app.get("/complejos/{id_complejo}/canchas")
def listar_canchas(
    id_complejo: int,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):
    sql = """
        SELECT *
        FROM cancha
        WHERE id_complejo = %s
        ORDER BY nombre_cancha
    """

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql, (id_complejo,))
    resultado = cursor.fetchall()
    cursor.close()

    return resultado

@app.get("/complejos/{id_complejo}/canchas/{nombre_cancha}")
def obtener_cancha(
    id_complejo: int,
    nombre_cancha: str,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):
    sql = """
        SELECT *
        FROM cancha
        WHERE id_complejo = %s
          AND nombre_cancha = %s
    """

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql, (id_complejo, nombre_cancha))
    resultado = cursor.fetchall()
    cursor.close()

    if not resultado:
        raise HTTPException(status_code=404, detail="Cancha no encontrada")

    return resultado[0]