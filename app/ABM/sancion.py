from fastapi import Depends, HTTPException
from mysql.connector import IntegrityError
from pydantic import BaseModel
from app.app import app
from app.auth import SOLO_ADMIN, db_para_usuario


class Sancion(BaseModel):
    id_sancion: str
    ci_jugador: int
    id_torneo: int
    motivo: str
    numero_fecha: int



#POST PARA DAR DE ALTA UNA SANCION
@app.post("/sancion", status_code=201)
def registrar_CANCHA(
    sancion: Sancion,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):

    cursor = conexion.cursor()

    sql = """
        INSERT INTO sancion
        (id_sancion, ci_jugador, id_torneo, motivo, numero_fecha)
        VALUES (%s, %s, %s, %s, %s)
    """

    valores = (
        sancion.id_sancion,
        sancion.ci_jugador,
        sancion.id_torneo,
        sancion.motivo,
        sancion.numero_fecha
    )

    try:
        cursor.execute(sql, valores)
        conexion.commit()

        return {
            "mensaje": "sancion registrado correctamente",
            "id_sancion": cursor.lastrowid
        }

    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="Alguno de los atributos no es válido"
        )

    finally:
        cursor.close()

#DELETE PARA DAR DE BAJA UNA SANCION
@app.delete("/sancion/{id_sancion}")
def eliminar_sancion(
    id_sancion: int,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):

    cursor = conexion.cursor()

    sql = """
        DELETE FROM sancion
        WHERE id_sancion = %s
    """

    try:
        cursor.execute(sql, (id_sancion,))

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="sancion no encontrado"
            )

        conexion.commit()

        return {
            "mensaje": "sancion eliminado correctamente"
        }

    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar el sancion porque tiene registros relacionados"
        )

    finally:
        cursor.close()

#PUT PARA MODIFICAR UNA SANCION
@app.put("/sancion/{id_sancion}")
def modificar_sancion(
    id_sancion: int,
    sancion: Sancion,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):

    cursor = conexion.cursor()
    sql = """
        UPDATE sancion
        SET ci_jugador = %s,
            id_torneo = %s,
            motivo = %s,
            numero_fecha = %s
        WHERE id_sancion = %s
    """

    valores = (
        sancion.ci_jugador,
        sancion.id_torneo,
        sancion.motivo,
        sancion.numero_fecha,
        id_sancion
    )

    try:
        cursor.execute(sql, valores)

        if cursor.rowcount == 0:
            cursor.execute(
                "SELECT id_sancion FROM sancion WHERE id_sancion = %s",
                (id_sancion,)
            )

            if cursor.fetchone() is None:
                raise HTTPException(
                    status_code=404,
                    detail="sancion no encontrado"
                )

        conexion.commit()

        return {
            "mensaje": "sancion modificado correctamente"
        }

    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="Alguno de los atributos no es válido"
        )

    finally:
        cursor.close()