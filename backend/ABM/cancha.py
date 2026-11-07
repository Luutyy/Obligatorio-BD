from fastapi import Depends, HTTPException
from mysql.connector import IntegrityError
from pydantic import BaseModel
from backend.app import app
from backend.auth import SOLO_ADMIN, db_para_usuario

class Cancha(BaseModel):
    nombre_cancha: str
    id_complejo: int
    superficie: str
    techada: bool

# POST: REGISTRAR CANCHA
@app.post("/canchas", status_code=201)
def registrar_cancha(
    cancha: Cancha,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):
    cursor = conexion.cursor()
    sql = """
        INSERT INTO cancha
        (nombre_cancha, id_complejo, superficie, techada)
        VALUES (%s, %s, %s, %s)
    """
    valores = (
        cancha.nombre_cancha,
        cancha.id_complejo,
        cancha.superficie,
        cancha.techada
    )
    try:
        cursor.execute(sql, valores)
        conexion.commit()
        return {
            "mensaje": "Cancha registrada correctamente",
            "nombre_cancha": cancha.nombre_cancha,
            "id_complejo": cancha.id_complejo
        }
    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="La cancha ya existe o el complejo no es válido"
        )
    finally:
        cursor.close()


# DELETE: ELIMINAR CANCHA
@app.delete("/canchas/{id_complejo}/{nombre_cancha}")
def eliminar_cancha(
    id_complejo: int,
    nombre_cancha: str,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):
    cursor = conexion.cursor()
    try:
        cursor.execute(
            """
            DELETE FROM cancha
            WHERE nombre_cancha = %s AND id_complejo = %s
            """,
            (nombre_cancha, id_complejo)
        )
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Cancha no encontrada"
            )
        conexion.commit()
        return {
            "mensaje": "Cancha eliminada correctamente"
        }
    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar la cancha porque tiene registros relacionados"
        )
    finally:
        cursor.close()


# PUT: MODIFICAR CANCHA
@app.put("/canchas/{id_complejo}/{nombre_cancha}")
def modificar_cancha(
    id_complejo: int,
    nombre_cancha: str,
    cancha: Cancha,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):
    cursor = conexion.cursor()
    sql = """
        UPDATE cancha
        SET nombre_cancha = %s,
            id_complejo = %s,
            superficie = %s,
            techada = %s
        WHERE nombre_cancha = %s AND id_complejo = %s
    """
    valores = (
        cancha.nombre_cancha,
        cancha.id_complejo,
        cancha.superficie,
        cancha.techada,
        nombre_cancha,
        id_complejo
    )
    try:
        cursor.execute(sql, valores)
        if cursor.rowcount == 0:
            cursor.execute(
                """
                SELECT nombre_cancha
                FROM cancha
                WHERE nombre_cancha = %s AND id_complejo = %s
                """,
                (nombre_cancha, id_complejo)
            )
            if cursor.fetchone() is None:
                raise HTTPException(
                    status_code=404,
                    detail="Cancha no encontrada"
                )
        conexion.commit()
        return {
            "mensaje": "Cancha modificada correctamente"
        }
    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="El complejo no existe o la cancha ya está registrada"
        )
    finally:
        cursor.close()
