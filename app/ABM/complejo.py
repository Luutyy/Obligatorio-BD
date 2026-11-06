from fastapi import Depends, HTTPException
from mysql.connector import IntegrityError
from pydantic import BaseModel
from app.app import app
from app.auth import SOLO_ADMIN, db_para_usuario


class Complejo(BaseModel):
    id_complejo: str
    nombre_complejo: str
    direccion: str
    departamento: str


#POST PARA DAR DE ALTA UNA COMPLEJO
@app.post("/complejo", status_code=201)
def registrar_CANCHA(
    complejo: Complejo,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):

    cursor = conexion.cursor()

    sql = """
        INSERT INTO complejo
        (id_complejo, nombre_complejo, direccion, departamento)
        VALUES (%s, %s, %s, %s)
    """

    valores = (
        complejo.id_complejo,
        complejo.id_complejo,
        complejo.direccion,
        complejo.departamento
    )

    try:
        cursor.execute(sql, valores)
        conexion.commit()

        return {
            "mensaje": "complejo registrado correctamente",
            "id_complejo": cursor.lastrowid
        }

    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="Alguno de los atributos no es válido"
        )

    finally:
        cursor.close()

#DELETE PARA DAR DE BAJA COMPLEJO
@app.delete("/complejo/{id_complejo}")
def eliminar_complejo(
    id_complejo: int,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):

    cursor = conexion.cursor()

    sql = """
        DELETE FROM complejo
        WHERE id_complejo = %s
    """

    try:
        cursor.execute(sql, (id_complejo,))

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="complejo no encontrado"
            )

        conexion.commit()

        return {
            "mensaje": "complejo eliminado correctamente"
        }

    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar el complejo porque tiene registros relacionados"
        )

    finally:
        cursor.close()

#PUT PARA MODIFICAR COMPLEJO
@app.put("/complejo/{id_complejo}")
def modificar_complejo(
    id_complejo: int,
    complejo: Complejo,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):

    cursor = conexion.cursor()

    sql = """
        UPDATE complejo
        SET id_complejo = %s,
            nombre_complejo = %s,
            direccion = %s,
            departamento = %s
        WHERE id_complejo = %s
    """

    valores = (
        complejo.nombre_complejo,
        complejo.direccion,
        complejo.departamento,
        id_complejo
    )

    try:
        cursor.execute(sql, valores)

        if cursor.rowcount == 0:
            cursor.execute(
                "SELECT id_complejo FROM complejo WHERE id_complejo = %s",
                (id_complejo,)
            )

            if cursor.fetchone() is None:
                raise HTTPException(
                    status_code=404,
                    detail="complejo no encontrado"
                )

        conexion.commit()

        return {
            "mensaje": "complejo modificado correctamente"
        }

    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="Alguno de los atributos no es válido"
        )

    finally:
        cursor.close()