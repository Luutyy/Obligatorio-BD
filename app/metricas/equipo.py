from ..conexion import conexion

#@app.get('/metricas/cantidad_sanciones')
def cantidad_sanciones(id_torneo: int):
    sql = """
        SELECT
            e.nombre AS equipo,
            s.motivo AS motivo,
            COUNT(*) as cantidad_sanciones
        FROM sancion_jugador s
        JOIN equipo_jugador_torneo ejt
            ON ejt.ci_jugador = s.ci_jugador
            AND ejt.id_torneo = s.id_torneo
        JOIN equipo e 
            ON e.id_equipo = ejt.id_equipo
        WHERE s.id_torneo = %s
        GROUP BY e.id_equipo, e.nombre, s.motivo
        ORDER BY e.nombre, s.motivo
    """

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql, (id_torneo,))
    resultado = cursor.fetchall()
    cursor.close()

    return resultado


# Obtener una tabla con la cantidad de goles que el equipo hizo y recibio por torneo
#@app.get('/metricas/goles_favor')
def goles_a_favor(id_torneo: int):
    sql = """
        SELECT
            e.id_equipo,
            e.nombre,
            e.id_torneo,
            COALESCE(SUM(
                CASE
                    WHEN rp.id_equipo_local = e.id_equipo THEN rp.goles_local ELSE rp.goles_visitante END
                ), 0) AS goles_favor,
            COALESCE(SUM(
                CASE 
                    WHEN rp.id_equipo_local = e.id_equipo THEN rp.goles_visitante ELSE rp.goles_local END
            ), 0) as goles_contra
        FROM equipo e
        LEFT JOIN resultado_partido rp
            ON rp.id_equipo_local = e.id_equipo
            OR rp.id_equipo_visitante = e.id_equipo
        WHERE e.id_torneo = %s
        GROUP BY e.id_equipo, e.nombre, e.id_torneo
        ORDER BY goles_favor DESC
    """
    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql, (id_torneo,))
    resultado = cursor.fetchall()
    cursor.close()

    return resultado

#Metrica extra, promedio de goles por partido
#@app.get('/metricas/promedio_equipo')
def promedio_por_equipo(id_torneo:int):
    sql = """
        SELECT
            e.id_equipo,
            e.nombre,
            COALESCE(ROUND(AVG(
                CASE
                    WHEN rp.id_equipo_local = e.id_equipo THEN rp.goles_local ELSE rp.goles_visitante END
                ), 2), 0) AS promedio_goles
            FROM equipo e
            LEFT JOIN resultado_partido rp
                ON rp.id_equipo_local = e.id_equipo
                OR rp.id_equipo_visitante = e.id_equipo
            WHERE e.id_torneo = %s
            GROUP BY e.id_equipo, e.nombre
            ORDER BY promedio_goles DESC
    """

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql, (id_torneo,))
    resultado = cursor.fetchall()
    cursor.close()

    return resultado