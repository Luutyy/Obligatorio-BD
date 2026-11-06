
from fastapi import Depends, HTTPException
from mysql.connector import IntegrityError
from pydantic import BaseModel
from app.app import app
from app.auth import SOLO_ADMIN, db_para_usuario


class EquipoJugadorTorneo(BaseModel):
    id_equipo: int
    ci_jugador: int
    id_torneo: int
    numero_camiseta: int


class ModificarEquipoJugador(BaseModel):
    id_equipo: int
    numero_camiseta: int


# REGISTRAR jugador en un equipo de un torneo
@app.post("/equipo-jugador-torneo", status_code=201)
def registrar_jugador_equipo(
    datos: EquipoJugadorTorneo,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):
    cursor = conexion.cursor()
    sql = """
        INSERT INTO equipo_jugador_torneo
        (id_equipo, ci_jugador, id_torneo, numero_camiseta)
        VALUES (%s, %s, %s, %s)
    """
    valores = (
        datos.id_equipo,
        datos.ci_jugador,
        datos.id_torneo,
        datos.numero_camiseta
    )

    try:
        cursor.execute(sql, valores)
        conexion.commit()
        return {"mensaje": "Jugador vinculado al equipo correctamente"}

    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="El jugador ya está registrado en ese torneo o alguno de los datos no existe"
        )
    finally:
        cursor.close()


# LISTAR todas las vinculaciones
@app.get("/equipo-jugador-torneo")
def listar_vinculaciones(
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):
    cursor = conexion.cursor(dictionary=True)
    sql = """
        SELECT
            ejt.id_equipo,
            e.nombre AS equipo,
            ejt.ci_jugador,
            j.nombre,
            j.apellido,
            ejt.id_torneo,
            ejt.numero_camiseta
        FROM equipo_jugador_torneo ejt
        JOIN equipo e ON e.id_equipo = ejt.id_equipo
        JOIN jugador j ON j.ci = ejt.ci_jugador
        ORDER BY ejt.id_torneo, e.nombre, j.apellido
    """
    cursor.execute(sql)
    resultado = cursor.fetchall()
    cursor.close()

    return resultado


# LISTAR jugadores de un equipo
@app.get("/equipos/{id_equipo}/jugadores")
def listar_jugadores_equipo(
    id_equipo: int,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):
    cursor = conexion.cursor(dictionary=True)

    sql = """
        SELECT
            ejt.id_equipo,
            e.nombre AS equipo,
            ejt.ci_jugador,
            j.nombre,
            j.apellido,
            ejt.id_torneo,
            ejt.numero_camiseta
        FROM equipo_jugador_torneo ejt
        JOIN equipo e ON e.id_equipo = ejt.id_equipo
        JOIN jugador j ON j.ci = ejt.ci_jugador
        WHERE ejt.id_equipo = %s
        ORDER BY j.apellido, j.nombre
    """
    cursor.execute(sql, (id_equipo,))
    resultado = cursor.fetchall()
    cursor.close()

    return resultado


# MODIFICAR equipo o número de camiseta
@app.put("/equipo-jugador-torneo/{id_torneo}/{ci_jugador}")
def modificar_vinculacion(
    id_torneo: int,
    ci_jugador: int,
    datos: ModificarEquipoJugador,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):
    cursor = conexion.cursor()
    sql = """
        UPDATE equipo_jugador_torneo
        SET id_equipo = %s,
            numero_camiseta = %s
        WHERE id_torneo = %s AND ci_jugador = %s
    """
    try:
        cursor.execute(sql, (
            datos.id_equipo,
            datos.numero_camiseta,
            id_torneo,
            ci_jugador
        ))
        if cursor.rowcount == 0:
            cursor.execute("""
                SELECT ci_jugador
                FROM equipo_jugador_torneo
                WHERE id_torneo = %s AND ci_jugador = %s
            """, (id_torneo, ci_jugador))

            if cursor.fetchone() is None:
                raise HTTPException(
                    status_code=404,
                    detail="No se encontró la vinculación"
                )

        conexion.commit()
        return {"mensaje": "Vinculación modificada correctamente"}
    except IntegrityError:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="El equipo indicado no existe o los datos no son válidos"
        )
    finally:
        cursor.close()


# ELIMINAR jugador de un equipo del torneo
@app.delete("/equipo-jugador-torneo/{id_torneo}/{ci_jugador}")
def eliminar_vinculacion(
    id_torneo: int,
    ci_jugador: int,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            DELETE FROM equipo_jugador_torneo
            WHERE id_torneo = %s AND ci_jugador = %s
        """, (id_torneo, ci_jugador))
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="No se encontró la vinculación"
            )
        conexion.commit()
        return {"mensaje": "Jugador desvinculado del equipo correctamente"}

    finally:
        cursor.close()
