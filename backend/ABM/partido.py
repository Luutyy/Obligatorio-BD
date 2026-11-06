from fastapi import Depends, HTTPException
from mysql.connector import IntegrityError
from pydantic import BaseModel
from backend.app import app
from backend.auth import SOLO_ADMIN, db_para_usuario


class Partido(BaseModel):
    id_torneo: int
    numero_fecha: int
    id_equipo_local: int
    id_equipo_visitante: int
    dia: str
    id_turno: int
    nombre_cancha: str
    id_complejo: int
    estado: str

#POST PARA DAR DE ALTA UN PARTIDO
@app.post("/partidos", status_code=201)
def registrar_partido(
    partido: Partido,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):

    cursor = conexion.cursor()

    sql = """
        INSERT INTO partido
        (id_torneo, numero_fecha, id_equipo_local,
         id_equipo_visitante, dia, id_turno,
         nombre_cancha, id_complejo, estado)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    valores = (
        partido.id_torneo,
        partido.numero_fecha,
        partido.id_equipo_local,
        partido.id_equipo_visitante,
        partido.dia,
        partido.id_turno,
        partido.nombre_cancha,
        partido.id_complejo,
        partido.estado
    )

    try:
        cursor.execute(sql, valores)
        conexion.commit()

        return {
            "mensaje": "Partido registrado correctamente",
            "id_partido": cursor.lastrowid
        }

    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="Alguno de los datos relacionados no es válido"
        )

    finally:
        cursor.close()

#DELETE PARA DAR DE BAJA PARTIDOS
@app.delete("/partidos/{id_partido}")
def eliminar_partido(
    id_partido: int,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):
    cursor = conexion.cursor()
    sql = """
        DELETE FROM partido
        WHERE id_partido = %s
    """
    try:
        cursor.execute(sql, (id_partido,))

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Partido no encontrado"
            )
        conexion.commit()
        return {
            "mensaje": "Partido eliminado correctamente"
        }
    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar el partido porque tiene registros relacionados"
        )
    finally:
        cursor.close()

#PUT PARA MODIFICAR PARTIDOS
@app.put("/partidos/{id_partido}")
def modificar_partido(
    id_partido: int,
    partido: Partido,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):

    cursor = conexion.cursor()

    sql = """
        UPDATE partido
        SET id_torneo = %s,
            numero_fecha = %s,
            id_equipo_local = %s,
            id_equipo_visitante = %s,
            dia = %s,
            id_turno = %s,
            nombre_cancha = %s,
            id_complejo = %s,
            estado = %s
        WHERE id_partido = %s
    """

    valores = (
        partido.id_torneo,
        partido.numero_fecha,
        partido.id_equipo_local,
        partido.id_equipo_visitante,
        partido.dia,
        partido.id_turno,
        partido.nombre_cancha,
        partido.id_complejo,
        partido.estado,
        id_partido
    )

    try:
        cursor.execute(sql, valores)

        if cursor.rowcount == 0:
            cursor.execute(
                "SELECT id_partido FROM partido WHERE id_partido = %s",
                (id_partido,)
            )

            if cursor.fetchone() is None:
                raise HTTPException(
                    status_code=404,
                    detail="Partido no encontrado"
                )

        conexion.commit()

        return {
            "mensaje": "Partido modificado correctamente"
        }

    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="Alguno de los datos relacionados no es válido"
        )

    finally:
        cursor.close()