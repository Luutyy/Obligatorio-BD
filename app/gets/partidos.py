from typing import Optional

from fastapi import Depends, HTTPException
from app.auth import SOLO_ADMIN, ADMIN_Y_PLANILLERO, db_para_usuario
from app.app import app


# Admin y planillero
@app.get("/partidos")
def listar_partidos(
    id_torneo: int = None,
    user=Depends(ADMIN_Y_PLANILLERO),
    conexion=Depends(db_para_usuario)
):
    if id_torneo is None:
        sql = """
            SELECT *
            FROM partido
        """

        cursor = conexion.cursor(dictionary=True)
        cursor.execute(sql)

    else:
        sql = """
            SELECT *
            FROM partido
            WHERE id_torneo = %s
        """

        cursor = conexion.cursor(dictionary=True)
        cursor.execute(sql, (id_torneo,))

    resultado = cursor.fetchall()
    cursor.close()

    return resultado

@app.get("/partidos/{id_partido}")
def obtener_partido(
    id_partido: int,
    user=Depends(ADMIN_Y_PLANILLERO),
    conexion=Depends(db_para_usuario)
):
    sql = """
        SELECT p.id_partido, p.id_torneo, p.numero_fecha,
               p.dia, p.estado,
               p.id_equipo_local, el.nombre AS equipo_local,
               p.id_equipo_visitante, ev.nombre AS equipo_visitante,
               p.id_turno,
               CAST(t.hora_inicio AS CHAR) AS hora_inicio,
               CAST(t.hora_fin AS CHAR) AS hora_fin,
               p.nombre_cancha, p.id_complejo, c.nombre_complejo
        FROM partido p
        JOIN equipo el ON el.id_equipo = p.id_equipo_local
        JOIN equipo ev ON ev.id_equipo = p.id_equipo_visitante
        JOIN turno t ON t.id_turno = p.id_turno
        JOIN complejo c ON c.id_complejo = p.id_complejo
        WHERE p.id_partido = %s
    """

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql, (id_partido,))
    resultado = cursor.fetchall()
    cursor.close()

    if not resultado:
        raise HTTPException(status_code=404, detail="Partido no encontrado")

    return resultado[0]


@app.get("/partidos/{id_partido}/planilla")
def planilla_del_partido(
    id_partido: int,
    user=Depends(ADMIN_Y_PLANILLERO),
    conexion=Depends(db_para_usuario)
):
    sql = """
        SELECT pp.ci_jugador, j.nombre, j.apellido,
               pp.id_equipo, e.nombre AS equipo,
               ej.numero_camiseta
        FROM planilla_partido pp
        JOIN partido p ON p.id_partido = pp.id_partido
        JOIN jugador j ON j.ci = pp.ci_jugador
        JOIN equipo e ON e.id_equipo = pp.id_equipo
        JOIN equipo_jugador_torneo ej
          ON ej.ci_jugador = pp.ci_jugador
         AND ej.id_torneo = p.id_torneo
        WHERE pp.id_partido = %s
        ORDER BY e.nombre, ej.numero_camiseta
    """

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql, (id_partido,))
    resultado = cursor.fetchall()
    cursor.close()

    return resultado

@app.get("/partidos/{id_partido}/jugadores-habilitados")
def jugadores_habilitados(
    id_partido: int,
    user=Depends(ADMIN_Y_PLANILLERO),
    conexion=Depends(db_para_usuario)
):
    sql = """
        SELECT j.ci, j.nombre, j.apellido,
               ej.id_equipo, e.nombre AS equipo,
               ej.numero_camiseta
        FROM partido p
        JOIN equipo_jugador_torneo ej
          ON ej.id_equipo IN (p.id_equipo_local, p.id_equipo_visitante)
        JOIN jugador j ON j.ci = ej.ci_jugador
        JOIN equipo e ON e.id_equipo = ej.id_equipo
        WHERE p.id_partido = %s
          AND NOT EXISTS (
              SELECT 1
              FROM sancion_jugador s
              WHERE s.ci_jugador = ej.ci_jugador
                AND s.id_torneo = p.id_torneo
                AND p.numero_fecha >= s.numero_fecha_inicio
                AND p.numero_fecha < s.numero_fecha_inicio + s.cantidad_fechas
          )
        ORDER BY e.nombre, ej.numero_camiseta
    """

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql, (id_partido,))
    resultado = cursor.fetchall()
    cursor.close()

    return resultado


@app.get("/partidos/{id_partido}/goles")
def goles_del_partido(
    id_partido: int,
    user=Depends(ADMIN_Y_PLANILLERO),
    conexion=Depends(db_para_usuario)
):
    sql = """
        SELECT g.id_gol, g.ci_jugador, j.nombre, j.apellido,
               g.minuto, g.autogol, pp.id_equipo,
               e.nombre AS equipo
        FROM gol g
        JOIN jugador j ON j.ci = g.ci_jugador
        LEFT JOIN planilla_partido pp
          ON pp.id_partido = g.id_partido
         AND pp.ci_jugador = g.ci_jugador
        LEFT JOIN equipo e ON e.id_equipo = pp.id_equipo
        WHERE g.id_partido = %s
        ORDER BY g.minuto
    """

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql, (id_partido,))
    resultado = cursor.fetchall()
    cursor.close()

    return resultado

@app.get("/partidos/{id_partido}/tarjetas")
def tarjetas_del_partido(
    id_partido: int,
    user=Depends(ADMIN_Y_PLANILLERO),
    conexion=Depends(db_para_usuario)
):
    sql = """
        SELECT t.id_tarjeta, t.ci_jugador, j.nombre, j.apellido,
               t.minuto, t.color, pp.id_equipo,
               e.nombre AS equipo
        FROM tarjeta t
        JOIN jugador j ON j.ci = t.ci_jugador
        LEFT JOIN planilla_partido pp
          ON pp.id_partido = t.id_partido
         AND pp.ci_jugador = t.ci_jugador
        LEFT JOIN equipo e ON e.id_equipo = pp.id_equipo
        WHERE t.id_partido = %s
        ORDER BY t.minuto
    """

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql, (id_partido,))
    resultado = cursor.fetchall()
    cursor.close()

    return resultado

@app.get("/partidos/{id_partido}/resultado")
def resultado_del_partido(
    id_partido: int,
    user=Depends(ADMIN_Y_PLANILLERO),
    conexion=Depends(db_para_usuario)
):
    sql = """
        SELECT p.id_partido, p.estado,
               el.nombre AS equipo_local,
               COALESCE(gl.cantidad_goles, 0) AS goles_local,
               ev.nombre AS equipo_visitante,
               COALESCE(gv.cantidad_goles, 0) AS goles_visitante
        FROM partido p
        JOIN equipo el ON el.id_equipo = p.id_equipo_local
        JOIN equipo ev ON ev.id_equipo = p.id_equipo_visitante
        LEFT JOIN goles_partido gl
          ON gl.id_partido = p.id_partido
         AND gl.id_equipo = p.id_equipo_local
        LEFT JOIN goles_partido gv
          ON gv.id_partido = p.id_partido
         AND gv.id_equipo = p.id_equipo_visitante
        WHERE p.id_partido = %s
    """

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql, (id_partido,))
    resultado = cursor.fetchall()
    cursor.close()

    if not resultado:
        raise HTTPException(status_code=404, detail="Partido no encontrado")

    return resultado[0]

@app.get("/sanciones")
def listar_sanciones(
    id_torneo: Optional[int] = None,
    ci_jugador: Optional[int] = None,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):
    sql = """
        SELECT s.id_sancion, s.ci_jugador, j.nombre, j.apellido,
               s.id_torneo, s.motivo,
               s.numero_fecha_inicio, s.cantidad_fechas
        FROM sancion_jugador s
        JOIN jugador j ON j.ci = s.ci_jugador
    """

    condiciones = []
    parametros = []

    if id_torneo is not None:
        condiciones.append("s.id_torneo = %s")
        parametros.append(id_torneo)

    if ci_jugador is not None:
        condiciones.append("s.ci_jugador = %s")
        parametros.append(ci_jugador)

    if condiciones:
        sql += " WHERE " + " AND ".join(condiciones)

    sql += " ORDER BY s.id_torneo, s.numero_fecha_inicio"

    cursor = conexion.cursor(dictionary=True)

    if parametros:
        cursor.execute(sql, tuple(parametros))
    else:
        cursor.execute(sql)

    resultado = cursor.fetchall()
    cursor.close()

    return resultado


@app.get("/sanciones/{id_sancion}")
def obtener_sancion(
    id_sancion: int,
    user=Depends(SOLO_ADMIN),
    conexion=Depends(db_para_usuario)
):
    sql = """
        SELECT s.id_sancion, s.ci_jugador, j.nombre, j.apellido,
               s.id_torneo, s.motivo,
               s.numero_fecha_inicio, s.cantidad_fechas
        FROM sancion_jugador s
        JOIN jugador j ON j.ci = s.ci_jugador
        WHERE s.id_sancion = %s
    """

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql, (id_sancion,))
    resultado = cursor.fetchall()
    cursor.close()

    if not resultado:
        raise HTTPException(status_code=404, detail="Sanción no encontrada")

    return resultado[0]