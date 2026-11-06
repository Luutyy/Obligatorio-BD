from datetime import date
from fastapi import Depends, HTTPException
from mysql.connector import IntegrityError
from app.app import app
from app.auth import SOLO_ADMIN, db_para_usuario


class Tarjeta(BaseModel):
    id_tarjeta: int
    apellido: str
    ci: str
    email: str
    fecha_nacimiento: date
    id_facultad: int
    tipo: str


@app.post("/tarjetaes", status_code=201)
def registrar_tarjeta(
    tarjeta: Tarjeta,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):

    cursor = conexion.cursor()

    sql = """
        INSERT INTO tarjeta
        (nombre, apellido, ci, email, fecha_nacimiento, id_facultad, tipo)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    valores = (
        tarjeta.id_partida,
        tarjeta.ci_jugador,
        tarjeta.minuto,
        tarjeta.color,
        id_tarjeta
    )

    try:
        cursor.execute(sql, valores)
        conexion.commit()

        return {
            "mensaje": "Tarjeta registrado correctamente"
        }

    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="El documento ya existe o la facultad no es válida"
        )

    finally:
        cursor.close()

#DELETE PARA DAR DE BAJA TARJETAES
@app.delete("/tarjetaes/{ci}")
def eliminar_tarjeta(
    ci: str,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):

    cursor = conexion.cursor()
    sql = """
        DELETE FROM tarjeta
        WHERE ci = %s

    """
    try:
        cursor.execute(sql, (ci,))
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Tarjeta no encontrado"
            )
        conexion.commit()
        return {
            "mensaje": "Tarjeta eliminado correctamente"
        }

    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar el tarjeta porque tiene registros relacionados"
        )

    finally:
        cursor.close()

#PUT PARA MODIFICAR TARJETAES
@app.put("/tarjetaes/{ci}")
def modificar_tarjeta(
    ci: str,
    tarjeta: Tarjeta,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):

    cursor = conexion.cursor()

    sql = """
        UPDATE tarjeta
        SET nombre = %s,
            apellido = %s,
            ci = %s,
            email = %s,
            id_facultad = %s,
            tipo = %s
        WHERE ci = %s
    """

    valores = (
        tarjeta.nombre,
        tarjeta.apellido,
        tarjeta.ci,
        tarjeta.email,
        tarjeta.id_facultad,
        tarjeta.tipo,
        ci
    )

    try:
        cursor.execute(sql, valores)

        if cursor.rowcount == 0:
            cursor.execute(
                "SELECT ci FROM tarjeta WHERE ci = %s",
                (ci,)
            )

            if cursor.fetchone() is None:
                raise HTTPException(
                    status_code=404,
                    detail="Tarjeta no encontrado"
                )

        conexion.commit()

        return {
            "mensaje": "Tarjeta modificado correctamente"
        }

    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="La cédula ya existe o la facultad no es válida"
        )

    finally:
        cursor.close()