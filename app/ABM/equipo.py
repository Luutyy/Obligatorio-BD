from fastapi import Depends, HTTPException
from mysql.connector import Error as MySQLError, IntegrityError, errorcode
from pydantic import BaseModel, Field

from app.app import app
from app.auth import SOLO_ADMIN, db_para_usuario


class Equipo(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    id_torneo: int = Field(gt=0)
    id_facultad: int = Field(gt=0)
    ci_capitan: str = Field(min_length=1, max_length=20)


def _error_integridad(e: IntegrityError) -> HTTPException:
    """Traduce el error de MySQL a una respuesta HTTP según su causa real."""
    if e.errno == errorcode.ER_DUP_ENTRY:  # 1062
        return HTTPException(409, "Ya existe un equipo con esos datos")
    if e.errno == errorcode.ER_NO_REFERENCED_ROW_2:  # 1452
        return HTTPException(409, "El torneo, la facultad o el capitán no son válidos")
    if e.errno == errorcode.ER_ROW_IS_REFERENCED_2:  # 1451
        return HTTPException(
            409, "No se puede eliminar el equipo porque tiene registros relacionados"
        )
    return HTTPException(409, "Los datos violan una restricción de la base de datos")


# POST PARA DAR DE ALTA UN EQUIPO
@app.post("/equipo", status_code=201)
def registrar_equipo(
    equipo: Equipo,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario),
):
    cursor = conexion.cursor()
    sql = """
        INSERT INTO equipo (nombre, id_torneo, id_facultad, ci_capitan)
        VALUES (%s, %s, %s, %s)
    """
    valores = (equipo.nombre, equipo.id_torneo, equipo.id_facultad, equipo.ci_capitan)

    try:
        cursor.execute(sql, valores)
        conexion.commit()
        return {
            "mensaje": "Equipo registrado correctamente",
            "id_equipo": cursor.lastrowid,
        }
    except IntegrityError as e:
        conexion.rollback()
        raise _error_integridad(e)
    except MySQLError:
        conexion.rollback()
        raise HTTPException(500, "Error interno de base de datos")
    finally:
        cursor.close()


# DELETE PARA DAR DE BAJA EQUIPOS
@app.delete("/equipo/{id_equipo}")
def eliminar_equipo(
    id_equipo: int,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario),
):
    cursor = conexion.cursor()

    try:
        cursor.execute("DELETE FROM equipo WHERE id_equipo = %s", (id_equipo,))

        if cursor.rowcount == 0:
            conexion.rollback()
            raise HTTPException(404, "Equipo no encontrado")

        conexion.commit()
        return {"mensaje": "Equipo eliminado correctamente"}
    except IntegrityError as e:
        conexion.rollback()
        raise _error_integridad(e)
    except MySQLError:
        conexion.rollback()
        raise HTTPException(500, "Error interno de base de datos")
    finally:
        cursor.close()


# PUT PARA MODIFICAR EQUIPO
@app.put("/equipo/{id_equipo}")
def modificar_equipo(
    id_equipo: int,
    equipo: Equipo,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario),
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
        id_equipo,
    )

    try:
        cursor.execute(sql, valores)

        if cursor.rowcount == 0:
            cursor.execute(
                "SELECT 1 FROM equipo WHERE id_equipo = %s", (id_equipo,)
            )
            if cursor.fetchone() is None:
                conexion.rollback()
                raise HTTPException(404, "Equipo no encontrado")

        conexion.commit()
        return {"mensaje": "Equipo modificado correctamente"}
    except IntegrityError as e:
        conexion.rollback()
        raise _error_integridad(e)
    except MySQLError:
        conexion.rollback()
        raise HTTPException(500, "Error interno de base de datos")
    finally:
        cursor.close()