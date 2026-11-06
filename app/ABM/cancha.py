from fastapi import Depends, HTTPException
from mysql.connector import IntegrityError
from pydantic import BaseModel
from app.app import app
from app.auth import SOLO_ADMIN, db_para_usuario


class Cancha(BaseModel):
    nombre_cancha: str
    id_complejo: int
    superficie: str
    techada: int


#POST PARA DAR DE ALTA UNA CANCHA
@app.post("/cancha", status_code=201)
def registrar_CANCHA(
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
            "mensaje": "cancha registrado correctamente",
            "id_cancha": cursor.lastrowid
        }

    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="Alguno de los atributos no es válido"
        )

    finally:
        cursor.close()

#DELETE PARA DAR DE BAJA canchaS
@app.delete("/cancha/{id_cancha}")
def eliminar_cancha(
    id_cancha: int,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):

    cursor = conexion.cursor()

    sql = """
        DELETE FROM cancha
        WHERE id_cancha = %s
    """

    try:
        cursor.execute(sql, (id_cancha,))

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="cancha no encontrado"
            )

        conexion.commit()

        return {
            "mensaje": "cancha eliminado correctamente"
        }

    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar el cancha porque tiene registros relacionados"
        )

    finally:
        cursor.close()

#PUT PARA MODIFICAR cancha
@app.put("/cancha/{id_cancha}")
def modificar_cancha(
    id_cancha: int,
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
        WHERE id_cancha = %s
    """

    valores = (
        cancha.nombre_cancha,
        cancha.id_complejo,
        cancha.superficie,
        cancha.techada,
        id_cancha
    )

    try:
        cursor.execute(sql, valores)

        if cursor.rowcount == 0:
            cursor.execute(
                "SELECT id_cancha FROM cancha WHERE id_cancha = %s",
                (id_cancha,)
            )

            if cursor.fetchone() is None:
                raise HTTPException(
                    status_code=404,
                    detail="cancha no encontrado"
                )

        conexion.commit()

        return {
            "mensaje": "cancha modificado correctamente"
        }

    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="Alguno de los atributos no es válido"
        )

    finally:
        cursor.close()