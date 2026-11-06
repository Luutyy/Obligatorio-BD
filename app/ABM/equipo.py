from pydantic import BaseModel
from database import obtener_conexion
from datetime import date
from typing import Optional
from api import api

class Equipo(BaseModel):
    nombre: str
    id_torneo: int
    id_facultad: int
    ci_capitan: int

#POST PARA DAR DE ALTA UN EQUIPO
@app.post("/equipo")
def registrar_jugador(equipo: Equipo):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    sql = """
        INSERT INTO equipo
        (id_equipo, nombre, id_torneo, id_facultad, ci_capitan) VALUES
        (%s, %s, %s, %s, %s)
    """
    valores = (equipo.nombre, equipo.nombre, equipo.id_torneo, equipo.id_facultad, ci_capitan)

    try:
        cursor.execute(sql, valores)
        conexion.commit()

        id_generado = cursor.lastrowid

        return {
            "mensaje": "Equipo registrado correctamente",
            "id_equipo": id_generado
        }

    except mysql.connector.IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="El documento ya existe o el equipo no es válido"
        )

    finally:
        cursor.close()
        conexion.close()

#DELETE PARA DAR DE BAJA JUGADORES
@app.delete("/equipo/{id_equipo}")
def eliminar_equipo(id_equipo: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        sql = """
            DELETE FROM jugador
            WHERE id_equipo = %s
        """
        cursor.execute(sql, (id_equipo,))
        conexion.commit()
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Equipo no encontrado"
            )
        return {
            "mensaje": "Equipo eliminado correctamente"
        }

    finally:
        cursor.close()
        conexion.close()

#PUT PARA MODIFICAR EQUIPO
@app.delete("/equipo/{id_equipo}")
def modificar_equipo(id_equipo: int,equipo: Equipo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        sql = """
            UPDATE equipo
            SET nombre = %s,
                id_torneo = %s,
                id_facultad = %s,
                ci_capitan = %s,
        """
        cursor.execute(sql, (id_equipo,))
        conexion.commit()
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Equipo no encontrado"
            )
        return {
            "mensaje": "Equipo modificaso correctamente"
        }

    finally:
        cursor.close()
        conexion.close()