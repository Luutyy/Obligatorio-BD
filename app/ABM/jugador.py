from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import obtener_conexion
from datetime import date
from typing import Optional
from api import api

class Jugador(BaseModel):
    nombre: str
    apellido: str
    ci: str
    email: str
    id_facultad: int
    tipo: str

#POST PARA DAR DE ALTA UN JUGADOR
@app.post("/jugadores")
def registrar_jugador(jugador: Jugador, user=Depends(requiere_rol("administrador"))):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    sql = """
        INSERT INTO jugador
        (nombre, apellido, ci, fecha_nacimiento, id_equipo)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    valores = (jugador.nombre, jugador.apellido, jugador.ci, jugador.email, jugador.id_facultad, jugador.tipo)

    try:
        cursor.execute(sql, valores)
        conexion.commit()
        return {
            "mensaje": "Jugador registrado correctamente",
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
@app.delete("/jugadores/{ci}")
def eliminar_jugador(ci: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        sql = """
            DELETE FROM jugador
            WHERE ci = %s
        """
        cursor.execute(sql, (ci,))
        conexion.commit()
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Jugador no encontrado"
            )
        return {
            "mensaje": "Jugador eliminado correctamente"
        }

    finally:
        cursor.close()
        conexion.close()

#PUT PARA MODIFICAR JUGADORES
@app.delete("/jugadores/{ci}")
def modificar_jugador(ci: int,jugador: Jugador):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        sql = """
            UPDATE jugador
            SET nombre = %s,
                apellido = %s,
                ci = %s,
                email = %s,
                fecha_nacimiento= %s,
                id_facultad = %s,
                tipo = %s,
            WHERE ci = %s
        """
        cursor.execute(sql, (id_jugador,))
        conexion.commit()
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Jugador no encontrado"
            )
        return {
            "mensaje": "Jugador eliminado correctamente"
        }

    finally:
        cursor.close()
        conexion.close()