from fastapi import Depends, HTTPException
from mysql.connector import IntegrityError
from pydantic import BaseModel
from backend.app import app
from backend.auth import SOLO_ADMIN, db_para_usuario

class Sancion(BaseModel):
    ci_jugador: int
    id_torneo: int
    motivo: str
    numero_fecha_inicio: int
    cantidad_fechas: int

# POST: REGISTRAR UNA SANCION
@app.post("/sanciones", status_code=201)
def registrar_sancion(
    sancion: Sancion,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):
    cursor = conexion.cursor()
    sql = """
        INSERT INTO sancion_jugador
        (ci_jugador, id_torneo, motivo, numero_fecha_inicio, cantidad_fechas)
        VALUES (%s, %s, %s, %s, %s)
    """
    valores = (
        sancion.ci_jugador,
        sancion.id_torneo,
        sancion.motivo,
        sancion.numero_fecha_inicio,
        sancion.cantidad_fechas
    )
    try:
        cursor.execute(sql, valores)
        conexion.commit()
        return {
            "mensaje": "Sanción registrada correctamente",
            "id_sancion": cursor.lastrowid
        }
    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="El jugador o el torneo no existen, o alguno de los datos no es válido"
        )
    finally:
        cursor.close()


# DELETE: ELIMINAR UNA SANCION
@app.delete("/sanciones/{id_sancion}")
def eliminar_sancion(
    id_sancion: int,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "DELETE FROM sancion_jugador WHERE id_sancion = %s",
            (id_sancion,)
        )
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Sanción no encontrada"
            )
        conexion.commit()
        return {
            "mensaje": "Sanción eliminada correctamente"
        }
    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar la sanción porque tiene registros relacionados"
        )
    finally:
        cursor.close()


# PUT: MODIFICAR UNA SANCION
@app.put("/sanciones/{id_sancion}")
def modificar_sancion(
    id_sancion: int,
    sancion: Sancion,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):
    cursor = conexion.cursor()
    sql = """
        UPDATE sancion_jugador
        SET ci_jugador = %s,
            id_torneo = %s,
            motivo = %s,
            numero_fecha_inicio = %s,
            cantidad_fechas = %s
        WHERE id_sancion = %s
    """
    valores = (
        sancion.ci_jugador,
        sancion.id_torneo,
        sancion.motivo,
        sancion.numero_fecha_inicio,
        sancion.cantidad_fechas,
        id_sancion
    )
    try:
        cursor.execute(sql, valores)
        if cursor.rowcount == 0:
            cursor.execute(
                "SELECT id_sancion FROM sancion_jugador WHERE id_sancion = %s",
                (id_sancion,)
            )
            if cursor.fetchone() is None:
                raise HTTPException(
                    status_code=404,
                    detail="Sanción no encontrada"
                )
        conexion.commit()
        return {
            "mensaje": "Sanción modificada correctamente"
        }
    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="El jugador o el torneo no existen, o alguno de los datos no es válido"
        )
    finally:
        cursor.close()
