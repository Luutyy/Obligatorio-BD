from fastapi import Depends, HTTPException
from mysql.connector import IntegrityError
from pydantic import BaseModel
from app.app import app
from app.auth import SOLO_ADMIN, db_para_usuario


class Jugador(BaseModel):
    nombre: str
    apellido: str
    ci: str
    email: str
    id_facultad: int
    tipo: str


@app.post("/jugadores", status_code=201)
def registrar_jugador(
    jugador: Jugador,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):

    cursor = conexion.cursor()

    sql = """
        INSERT INTO jugador
        (nombre, apellido, ci, email, id_facultad, tipo)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    valores = (
        jugador.nombre,
        jugador.apellido,
        jugador.ci,
        jugador.email,
        jugador.id_facultad,
        jugador.tipo
    )

    try:
        cursor.execute(sql, valores)
        conexion.commit()

        return {
            "mensaje": "Jugador registrado correctamente"
        }

    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="El documento ya existe o la facultad no es válida"
        )

    finally:
        cursor.close()

#DELETE PARA DAR DE BAJA JUGADORES
@app.delete("/jugadores/{ci}")
def eliminar_jugador(
    ci: str,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):

    cursor = conexion.cursor()
    sql = """
        DELETE FROM jugador
        WHERE ci = %s

    """
    try:
        cursor.execute(sql, (ci,))
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Jugador no encontrado"
            )
        conexion.commit()
        return {
            "mensaje": "Jugador eliminado correctamente"
        }

    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar el jugador porque tiene registros relacionados"
        )

    finally:
        cursor.close()

#PUT PARA MODIFICAR JUGADORES
@app.put("/jugadores/{ci}")
def modificar_jugador(
    ci: str,
    jugador: Jugador,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):

    cursor = conexion.cursor()

    sql = """
        UPDATE jugador
        SET nombre = %s,
            apellido = %s,
            ci = %s,
            email = %s,
            id_facultad = %s,
            tipo = %s
        WHERE ci = %s
    """

    valores = (
        jugador.nombre,
        jugador.apellido,
        jugador.ci,
        jugador.email,
        jugador.id_facultad,
        jugador.tipo,
        ci
    )

    try:
        cursor.execute(sql, valores)

        if cursor.rowcount == 0:
            cursor.execute(
                "SELECT ci FROM jugador WHERE ci = %s",
                (ci,)
            )

            if cursor.fetchone() is None:
                raise HTTPException(
                    status_code=404,
                    detail="Jugador no encontrado"
                )

        conexion.commit()

        return {
            "mensaje": "Jugador modificado correctamente"
        }

    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="La cédula ya existe o la facultad no es válida"
        )

    finally:
        cursor.close()