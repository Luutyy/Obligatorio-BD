
from fastapi import Depends, HTTPException
from mysql.connector import IntegrityError
from pydantic import BaseModel

from backend.app import app
from backend.auth import SOLO_ADMIN, db_para_usuario


class Tarjeta(BaseModel):
    id_partido: int
    ci_jugador: str
    minuto: int
    color: str


# POST: REGISTRAR TARJETA
@app.post("/tarjetas", status_code=201)
def registrar_tarjeta(
    tarjeta: Tarjeta,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):
    cursor = conexion.cursor()
    sql = """
        INSERT INTO tarjeta
        (id_partido, ci_jugador, minuto, color)
        VALUES (%s, %s, %s, %s)
    """
    valores = (
        tarjeta.id_partido,
        tarjeta.ci_jugador,
        tarjeta.minuto,
        tarjeta.color
    )
    try:
        cursor.execute(sql, valores)
        conexion.commit()
        return {
            "mensaje": "Tarjeta registrada correctamente",
            "id_tarjeta": cursor.lastrowid
        }
    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="El partido o el jugador no existen, o hay un conflicto con los datos"
        )
    finally:
        cursor.close()


# DELETE: ELIMINAR TARJETA
@app.delete("/tarjetas/{id_tarjeta}")
def eliminar_tarjeta(
    id_tarjeta: int,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "DELETE FROM tarjeta WHERE id_tarjeta = %s",
            (id_tarjeta,)
        )
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="No se encontró la tarjeta"
            )
        conexion.commit()
        return {
            "mensaje": "Tarjeta eliminada correctamente"
        }
    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar la tarjeta porque tiene registros relacionados"
        )
    finally:
        cursor.close()


# PUT: MODIFICAR TARJETA
@app.put("/tarjetas/{id_tarjeta}")
def modificar_tarjeta(
    id_tarjeta: int,
    tarjeta: Tarjeta,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):
    cursor = conexion.cursor()
    sql = """
        UPDATE tarjeta
        SET id_partido = %s,
            ci_jugador = %s,
            minuto = %s,
            color = %s
        WHERE id_tarjeta = %s
    """
    valores = (
        tarjeta.id_partido,
        tarjeta.ci_jugador,
        tarjeta.minuto,
        tarjeta.color,
        id_tarjeta
    )
    try:
        cursor.execute(sql, valores)
        if cursor.rowcount == 0:
            cursor.execute(
                "SELECT id_tarjeta FROM tarjeta WHERE id_tarjeta = %s",
                (id_tarjeta,)
            )
            if cursor.fetchone() is None:
                raise HTTPException(
                    status_code=404,
                    detail="No se encontró la tarjeta"
                )
        conexion.commit()
        return {
            "mensaje": "Tarjeta modificada correctamente"
        }
    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="El partido o el jugador no existen, o hay un conflicto con los datos"
        )
    finally:
        cursor.close()
