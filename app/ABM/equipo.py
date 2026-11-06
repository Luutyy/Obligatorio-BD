from fastapi import Depends, HTTPException
from mysql.connector import IntegrityError
from pydantic import BaseModel
from app.app import app
from app.auth import SOLO_ADMIN, db_para_usuario


class Equipo(BaseModel):
    nombre: str
    id_torneo: int
    id_facultad: int
    ci_capitan: str


#POST PARA DAR DE ALTA UN EQUIPO
@app.post("/equipo", status_code=201)
def registrar_equipo(
    equipo: Equipo,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):
    cursor = conexion.cursor()
    sql = """
        INSERT INTO equipo
        (nombre, id_torneo, id_facultad, ci_capitan)
        VALUES (%s, %s, %s, %s)
    """
    valores = (
        equipo.nombre,
        equipo.id_torneo,
        equipo.id_facultad,
        equipo.ci_capitan
    )
    try:
        cursor.execute(sql, valores)
        conexion.commit()
        return {
            "mensaje": "Equipo registrado correctamente",
            "id_equipo": cursor.lastrowid
        }
    
    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="El torneo, la facultad o el capitán no son válidos"
        )
    finally:
        cursor.close()

#DELETE PARA DAR DE BAJA EQUIPOS
@app.delete("/equipo/{id_equipo}")
def eliminar_equipo(
    id_equipo: int,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):
    cursor = conexion.cursor()
    sql = """
        DELETE FROM equipo
        WHERE id_equipo = %s
    """

    try:
        cursor.execute(sql, (id_equipo,))

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Equipo no encontrado"
            )
        conexion.commit()
        return {
            "mensaje": "Equipo eliminado correctamente"
        }

    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar el equipo porque tiene registros relacionados"
        )
    finally:
        cursor.close()

#PUT PARA MODIFICAR EQUIPO
@app.put("/equipo/{id_equipo}")
def modificar_equipo(
    id_equipo: int,
    equipo: Equipo,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):
    cursor = conexion.cursor()
    sql = """
        UPDATE equipo
        SET nombre = %s,
            id_torneo = %s,
            id_facultad = %s,
            ci_capitan = %s
        WHERE id_equipo = %s
    """
    valores = (
        equipo.nombre,
        equipo.id_torneo,
        equipo.id_facultad,
        equipo.ci_capitan,
        id_equipo
    )

    try:
        cursor.execute(sql, valores)

        if cursor.rowcount == 0:
            cursor.execute(
                "SELECT id_equipo FROM equipo WHERE id_equipo = %s",
                (id_equipo,)
            )
            if cursor.fetchone() is None:
                raise HTTPException(
                    status_code=404,
                    detail="Equipo no encontrado"
                )
        conexion.commit()
        return {
            "mensaje": "Equipo modificado correctamente"
        }

    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="El torneo, la facultad o el capitán no son válidos"
        )

    finally:
        cursor.close()