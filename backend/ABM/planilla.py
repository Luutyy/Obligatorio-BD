from fastapi import Depends, HTTPException
from mysql.connector import IntegrityError
from pydantic import BaseModel

from backend.app import app
from backend.auth import ADMIN_Y_PLANILLERO, db_para_usuario


# MODELO DE PLANILLA
class Planilla(BaseModel):
    id_partido: int
    ci_jugador: int
    id_equipo: int

# POST: REGISTRAR JUGADOR EN PLANILLA
@app.post("/planillas", status_code=201)
def registrar_planilla(
    planilla: Planilla,
    user=Depends(ADMIN_Y_PLANILLERO),
    conexion=Depends(db_para_usuario)
):
    cursor = conexion.cursor()
    sql = """
        INSERT INTO planilla_partido
        (id_partido, ci_jugador, id_equipo)
        VALUES (%s, %s, %s)
    """
    valores = (
        planilla.id_partido,
        planilla.ci_jugador,
        planilla.id_equipo
    )

    try:
        cursor.execute(sql, valores)
        conexion.commit()
        return {
            "mensaje": "Jugador agregado a la planilla correctamente"
        }
    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="El jugador ya está en la planilla o el partido, jugador o equipo no existen"
        )

    finally:
        cursor.close()


# GET: LISTAR TODAS LAS PLANILLAS
@app.get("/planillas")
def listar_planillas(
    user=Depends(ADMIN_Y_PLANILLERO),
    conexion=Depends(db_para_usuario)
):
    sql = """
        SELECT
            pp.id_partido,
            pp.ci_jugador,
            j.nombre,
            j.apellido,
            pp.id_equipo
        FROM planilla_partido pp
        JOIN jugador j ON j.ci = pp.ci_jugador
        ORDER BY pp.id_partido, j.apellido, j.nombre
    """
    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql)
    resultado = cursor.fetchall()
    cursor.close()

    return resultado


# GET: OBTENER PLANILLA DE UN PARTIDO
@app.get("/planillas/{id_partido}")
def obtener_planilla(
    id_partido: int,
    user=Depends(ADMIN_Y_PLANILLERO),
    conexion=Depends(db_para_usuario)
):
    sql = """
        SELECT
            pp.id_partido,
            pp.ci_jugador,
            j.nombre,
            j.apellido,
            pp.id_equipo
        FROM planilla_partido pp
        JOIN jugador j ON j.ci = pp.ci_jugador
        WHERE pp.id_partido = %s
        ORDER BY j.apellido, j.nombre
    """
    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql, (id_partido,))
    resultado = cursor.fetchall()
    cursor.close()

    if not resultado:
        raise HTTPException(
            status_code=404,
            detail="No se encontró una planilla para ese partido"
        )

    return resultado


# DELETE: ELIMINAR JUGADOR DE UNA PLANILLA
@app.delete("/planillas/{id_partido}/{ci_jugador}")
def eliminar_de_planilla(
    id_partido: int,
    ci_jugador: int,
    user=Depends(ADMIN_Y_PLANILLERO),
    conexion=Depends(db_para_usuario)
):
    cursor = conexion.cursor()
    sql = """
        DELETE FROM planilla_partido
        WHERE id_partido = %s
          AND ci_jugador = %s
    """

    try:
        cursor.execute(sql, (id_partido, ci_jugador))
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Jugador no encontrado en esa planilla"
            )
        conexion.commit()

        return {
            "mensaje": "Jugador eliminado de la planilla correctamente"
        }

    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar el registro de la planilla"
        )
    finally:
        cursor.close()
