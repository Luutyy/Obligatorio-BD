from fastapi import Depends, HTTPException
from mysql.connector import IntegrityError
from pydantic import BaseModel
from backend.app import app
from backend.auth import SOLO_ADMIN, db_para_usuario

class Complejo(BaseModel):
    id_complejo: int
    nombre_complejo: str
    direccion: str
    departamento: str

# POST: REGISTRAR COMPLEJO
@app.post("/complejos", status_code=201)
def registrar_complejo(
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
        complejo.nombre_complejo,
        complejo.direccion,
        complejo.departamento
    )
    try:
        cursor.execute(sql, valores)
        conexion.commit()
        return {
            "mensaje": "Complejo registrado correctamente",
            "id_complejo": complejo.id_complejo
        }
    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="El ID del complejo ya existe o alguno de los datos no es válido"
        )
    finally:
        cursor.close()


# DELETE: ELIMINAR COMPLEJO
@app.delete("/complejos/{id_complejo}")
def eliminar_complejo(
    id_complejo: int,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "DELETE FROM complejo WHERE id_complejo = %s",
            (id_complejo,)
        )
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Complejo no encontrado"
            )
        conexion.commit()
        return {
            "mensaje": "Complejo eliminado correctamente"
        }
    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar el complejo porque tiene canchas u otros registros relacionados"
        )
    finally:
        cursor.close()


# PUT: MODIFICAR COMPLEJO
@app.put("/complejos/{id_complejo}")
def modificar_complejo(
    id_complejo: int,
    complejo: Complejo,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):
    cursor = conexion.cursor()
    sql = """
        UPDATE complejo
        SET nombre_complejo = %s,
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
                    detail="Complejo no encontrado"
                )
        conexion.commit()
        return {
            "mensaje": "Complejo modificado correctamente"
        }
    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="Alguno de los datos no es válido"
        )
    finally:
        cursor.close()
