from fastapi import Depends, HTTPException
from mysql.connector import IntegrityError
from pydantic import BaseModel
from app.app import app
from app.auth import SOLO_ADMIN, db_para_usuario


class Gol(BaseModel):
    id_gol: int
    id_partido: int
    ci_jugador: int
    minuto: int
    autogol: int


#POST PARA DAR DE ALTA UN GOL
@app.post("/gol", status_code=201)
def registrar_gol(
    gol: Gol,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):

    cursor = conexion.cursor()

    sql = """
        INSERT INTO gol
        (id_partido, ci_jugador, minuto, autogol)
        VALUES (%s, %s, %s, %s)
    """

    valores = (
        gol.id_partido,
        gol.ci_jugador,
        gol.minuto,
        gol.autogol
    )

    try:
        cursor.execute(sql, valores)
        conexion.commit()

        return {
            "mensaje": "Gol registrado correctamente",
            "id_gol": cursor.lastrowid
        }

    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="Algun dato no es válido"
        )

    finally:
        cursor.close()

#DELETE PARA DAR DE BAJA GOLS
@app.delete("/gol/{id_gol}")
def eliminar_gol(
    id_gol: int,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):

    cursor = conexion.cursor()

    sql = """
        DELETE FROM gol
        WHERE id_gol = %s
    """

    try:
        cursor.execute(sql, (id_gol,))

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Gol no encontrado"
            )

        conexion.commit()

        return {
            "mensaje": "Gol eliminado correctamente"
        }

    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar el gol porque tiene registros relacionados"
        )

    finally:
        cursor.close()

#PUT PARA MODIFICAR GOL
@app.put("/gol/{id_gol}")
def modificar_gol(
    id_gol: int,
    gol: Gol,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):

    cursor = conexion.cursor()

    sql = """
        UPDATE gol
        SET ci_jugador = %s,
            minuto = %s,
            autogol = %s,
        WHERE id_gol = %s
    """
    
    valores = (
        gol.ci_jugador,
        gol.minuto,
        gol.autogol,
        id_gol
    )

    try:
        cursor.execute(sql, valores)

        if cursor.rowcount == 0:
            cursor.execute(
                "SELECT id_gol FROM gol WHERE id_gol = %s",
                (id_gol,)
            )

            if cursor.fetchone() is None:
                raise HTTPException(
                    status_code=404,
                    detail="Gol no encontrado"
                )

        conexion.commit()

        return {
            "mensaje": "Gol modificado correctamente"
        }

    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="El torneo, la facultad o el capitán no son válidos"
        )

    finally:
        cursor.close()